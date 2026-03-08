```bash
#!/usr/bin/env bash
# governance-audit.sh
# PreToolUse hook: scan Bash commands for governance threats.
# High confidence => block (exit 2), medium => warn (exit 0).
# Logs JSONL records to governance-audit.jsonl.

set -u -o pipefail

command -v python3 >/dev/null 2>&1 || {
  echo "governance-audit: python3 is required" >&2
  exit 2
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${GOVERNANCE_AUDIT_LOG:-$SCRIPT_DIR/governance-audit.jsonl}"

INPUT="$(cat /dev/stdin 2>/dev/null || true)"
[ -z "$INPUT" ] && exit 0

PARSED="$(
  printf '%s' "$INPUT" | python3 - <<'PY'
import base64
import json
import sys

d = json.load(sys.stdin)
ti = d.get("tool_input") or {}
cmd = ti.get("command", "")
if not isinstance(cmd, str):
    cmd = str(cmd)

fields = [
    d.get("tool_name", ""),
    base64.b64encode(cmd.encode("utf-8")).decode("ascii"),
    d.get("session_id", ""),
    d.get("cwd", ""),
    d.get("hook_event_name", "PreToolUse"),
]
print("\t".join(str(x).replace("\t", " ") for x in fields))
PY
)"
PARSE_RC=$?
if [ $PARSE_RC -ne 0 ] || [ -z "$PARSED" ]; then
  echo "governance-audit: invalid hook payload" >&2
  exit 2
fi

IFS=$'\t' read -r TOOL_NAME CMD_B64 SESSION_ID CWD EVENT_NAME <<< "$PARSED"

CMD="$(
  python3 - "$CMD_B64" <<'PY'
import base64
import sys

raw = sys.argv[1] if len(sys.argv) > 1 else ""
try:
    out = base64.b64decode(raw.encode("ascii")).decode("utf-8", "replace")
except Exception:
    out = ""
print(out, end="")
PY
)"

[ "${TOOL_NAME:-}" != "Bash" ] && exit 0
[ -z "${CMD:-}" ] && exit 0

mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true

CMD_HASH="$(
  python3 - "$CMD" <<'PY'
import hashlib
import sys
print(hashlib.sha256(sys.argv[1].encode("utf-8")).hexdigest())
PY
)"

make_snippet() {
  local text="$1"
  local out
  out="$(printf '%s' "$text" | tr '\n' ' ' | sed -E 's/[[:space:]]+/ /g' | cut -c1-180)"
  out="$(printf '%s' "$out" | sed -E 's/(AKIA[0-9A-Z]{4})[0-9A-Z]{12}/\1[REDACTED]/g')"
  out="$(printf '%s' "$out" | sed -E 's/[A-Za-z0-9_\/+=.-]{32,}/[REDACTED]/g')"
  printf '%s' "$out"
}

append_log() {
  local decision="$1"
  local category="$2"
  local severity="$3"
  local confidence="$4"
  local rule_id="$5"
  local snippet="$6"

  python3 - "$LOG_FILE" "$decision" "$category" "$severity" "$confidence" "$rule_id" "$snippet" "$CMD_HASH" "$EVENT_NAME" "$SESSION_ID" "$TOOL_NAME" "$CWD" <<'PY'
import datetime
import json
import os
import sys

log_file, decision, category, severity, confidence, rule_id, snippet, cmd_hash, event_name, session_id, tool_name, cwd = sys.argv[1:]

record = {
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "event": event_name or "PreToolUse",
    "decision": decision,
    "category": category,
    "severity": severity,
    "confidence": float(confidence),
    "rule_id": rule_id,
    "snippet": snippet,
    "command_sha256": cmd_hash,
    "session_id": session_id,
    "tool_name": tool_name,
    "cwd": cwd,
}
os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
with open(log_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")
PY
}

HIGH_REASONS=()
MEDIUM_REASONS=()

while IFS= read -r line; do
  [ -z "$line" ] && continue
  case "$line" in
    \#*) continue ;;
  esac

  category="${line%%::*}"
  rest="${line#*::}"
  severity="${rest%%::*}"
  rest="${rest#*::}"
  confidence="${rest%%::*}"
  rest="${rest#*::}"
  rule_id="${rest%%::*}"
  regex="${rest#*::}"

  if printf '%s' "$CMD" | grep -Eiq -- "$regex"; then
    match="$(printf '%s' "$CMD" | grep -Eio -- "$regex" | head -n 1 || true)"
    [ -z "$match" ] && match="$CMD"
    snippet="$(make_snippet "$match")"

    append_log "match" "$category" "$severity" "$confidence" "$rule_id" "$snippet"

    if [ "$severity" = "high" ]; then
      HIGH_REASONS+=("${category}:${rule_id}:${confidence}")
    else
      MEDIUM_REASONS+=("${category}:${rule_id}:${confidence}")
    fi
  fi
done <<'RULES'
# category::severity::confidence::rule_id::regex
data_exfiltration::high::0.95::exfil_http_upload::(curl|wget|httpie)[[:space:]].*(--data|-d[[:space:]]|--form|-F[[:space:]]|--upload-file|@[^[:space:]]+)
data_exfiltration::medium::0.82::exfil_remote_copy::(scp|rsync|sftp|ftp|nc|ncat|socat)[[:space:]].*(\.env|id_rsa|id_ed25519|\.ssh/|/etc/passwd|/etc/shadow|credentials?)
data_exfiltration::medium::0.76::exfil_encoded_pipe::(base64|xxd|openssl[[:space:]]+enc).*\|[[:space:]]*(curl|wget|nc|ncat|socat)

privilege_escalation::high::0.95::priv_sudo_shell::(sudo[[:space:]]+-S|sudo[[:space:]]+su([[:space:]]|$)|su[[:space:]]+-|doas[[:space:]])
privilege_escalation::high::0.92::priv_suid_set::(chmod[[:space:]]+[0-7]*4[0-7]{2}|chmod[[:space:]]+\+s|setcap[[:space:]]+cap_setuid\+ep)
privilege_escalation::medium::0.83::priv_account_mod::(useradd|usermod|groupadd|passwd|visudo)

system_destruction::high::0.95::destroy_root_rm::(^|[[:space:];|&])rm[[:space:]]+-rf[[:space:]]+/([[:space:]]|$)
system_destruction::high::0.94::destroy_disk_wipe::(dd[[:space:]]+if=/dev/(zero|urandom).*(of=/dev/(sd[a-z]|nvme[0-9]+n[0-9]+|vd[a-z]|xvd[a-z]))|mkfs\.[a-z0-9]+|wipefs[[:space:]]+-a|shred[[:space:]].*/dev/)
system_destruction::high::0.93::destroy_fork_bomb:::[[:space:]]*\([[:space:]]*\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:[[:space:]]*&[[:space:]]*\};[[:space:]]*:
system_destruction::medium::0.84::destroy_bulk_delete::(find[[:space:]]+/[^;|&]*-delete|git[[:space:]]+clean[[:space:]]+-fdx)

prompt_injection::high::0.90::prompt_override_payload::(ignore[[:space:]]+(all[[:space:]]+)?(previous|prior)[[:space:]]+instructions|reveal[[:space:]]+(the[[:space:]]+)?(system|developer)[[:space:]]+prompt|bypass[[:space:]]+(safety|policy|guardrails))
prompt_injection::medium::0.78::prompt_jailbreak_fetch::(curl|wget)[[:space:]].*(jailbreak|prompt[-_ ]?inject|ignore[-_ ]?instructions|system[-_ ]?prompt)
prompt_injection::medium::0.68::prompt_policy_scrape::(cat|sed|awk|grep)[[:space:]].*(AGENTS\.md|CLAUDE\.md|SYSTEM_PROMPT|developer[[:space:]]+message)

credential_exposure::high::0.95::cred_aws_access_key::AKIA[0-9A-Z]{16}
credential_exposure::high::0.95::cred_private_key::-----BEGIN[[:space:]]+(RSA|OPENSSH|EC|DSA)[[:space:]]+PRIVATE[[:space:]]+KEY-----
credential_exposure::high::0.92::cred_secret_dump::(cat|sed|awk|grep|printenv|env)[[:space:]].*(\.env|id_rsa|id_ed25519|AWS_SECRET_ACCESS_KEY|OPENAI_API_KEY|GITHUB_TOKEN|SECRET_KEY|DB_PASSWORD)
credential_exposure::medium::0.80::cred_secret_paths::(ls|find)[[:space:]].*(\.aws/credentials|\.ssh/|\.kube/config|/run/secrets|/etc/secrets)
RULES

if [ "${#HIGH_REASONS[@]}" -gt 0 ]; then
  reason_text="$(IFS=', '; echo "${HIGH_REASONS[*]}")"
  append_log "block" "summary" "high" "1.00" "decision" "$(make_snippet "$reason_text")"
  echo "governance-audit: blocked (high confidence) -> $reason_text" >&2
  exit 2
fi

if [ "${#MEDIUM_REASONS[@]}" -gt 0 ]; then
  reason_text="$(IFS=', '; echo "${MEDIUM_REASONS[*]}")"
  append_log "warn" "summary" "medium" "0.75" "decision" "$(make_snippet "$reason_text")"
  echo "governance-audit: warning (medium confidence) -> $reason_text" >&2
  exit 0
fi

append_log "allow" "summary" "none" "0.00" "decision" "no_match"
exit 0
```