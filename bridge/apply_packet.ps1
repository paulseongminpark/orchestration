param(
    [switch]$FromClipboard,
    [switch]$Commit
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path $PSScriptRoot -Parent
Push-Location $repoRoot

try {
    # --- 1. Read PACKET ---
    if ($FromClipboard) {
        $raw = Get-Clipboard -Raw
        if (-not $raw) { Write-Error "Clipboard is empty."; exit 1 }
    } else {
        Write-Error "Usage: -FromClipboard required."; exit 1
    }

    # Save raw packet for debugging
    $raw | Out-File -FilePath "bridge/packet.txt" -Encoding utf8 -Force
    Write-Host "[OK] Saved raw packet to bridge/packet.txt"

    # --- 2. Validate PACKET markers ---
    if ($raw -notmatch '\[PACKET\]' -or $raw -notmatch '\[/PACKET\]') {
        Write-Error "PACKET markers [PACKET]...[/PACKET] not found."
        exit 1
    }

    # Extract content between markers
    $packetBody = ($raw -replace '(?s).*\[PACKET\]', '' -replace '(?s)\[/PACKET\].*', '').Trim()

    # --- 3. Extract COMMIT_MESSAGE ---
    $commitMsg = "packet: apply"
    if ($packetBody -match '(?m)^COMMIT_MESSAGE:\s*(.+)$') {
        $commitMsg = $Matches[1].Trim()
    }
    Write-Host "[OK] Commit message: $commitMsg"

    # --- 4. Extract diff block ---
    if ($packetBody -match '(?s)```diff\r?\n(.*?)```') {
        $patch = $Matches[1]
    } else {
        Write-Error "No ```diff ... ``` block found in PACKET."
        exit 1
    }

    $patch | Out-File -FilePath "bridge/packet.patch" -Encoding utf8 -Force -NoNewline
    Write-Host "[OK] Saved patch to bridge/packet.patch"

    # --- 5. Apply patch ---
    $check = git apply --check "bridge/packet.patch" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Patch check failed:`n$check"
        exit 1
    }
    Write-Host "[OK] Patch check passed."

    git apply --whitespace=nowarn "bridge/packet.patch"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "git apply failed."
        exit 1
    }
    Write-Host "[OK] Patch applied."

    # --- 6. Commit & push ---
    if ($Commit) {
        git add context/STATE.md context/EVENTS.log context/LATEST_CONTEXT.md
        git commit -m $commitMsg
        if ($LASTEXITCODE -ne 0) {
            Write-Error "git commit failed."
            exit 1
        }
        git push
        if ($LASTEXITCODE -ne 0) {
            Write-Error "git push failed."
            exit 1
        }
        Write-Host "[OK] Committed and pushed."
    } else {
        Write-Host "[SKIP] -Commit not set. Files changed but not committed."
    }

    Write-Host "`n=== DONE ==="
} finally {
    Pop-Location
}
