import json
import glob
import re
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 프로젝트 파라미터
project = sys.argv[1] if len(sys.argv) > 1 else "orchestration"

# 최근 세션 파일
session_files = glob.glob(r"C:\Users\pauls\.claude\projects\C--\*.jsonl")
if not session_files:
    exit()

latest_session = max(session_files, key=lambda x: Path(x).stat().st_mtime)

# 출력 경로 (새 구조: 03_evidence)
date = datetime.now().strftime('%Y-%m-%d')
output_dir = Path(rf"C:\dev\03_evidence\claude\{project}")
output_dir.mkdir(parents=True, exist_ok=True)
output = output_dir / f"{date}.md"

# Content 추출
pairs = []
current_user = None
current_timestamp = None
current_assistant_texts = []

with open(latest_session, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            role = msg.get('role')
            timestamp = obj.get('timestamp', '')

            if role == 'user':
                if current_user:
                    assistant_full = '\n\n'.join(current_assistant_texts)
                    pairs.append({
                        'time': current_timestamp,
                        'user': current_user,
                        'assistant': assistant_full
                    })

                content = msg.get('content', '')
                if isinstance(content, str):
                    current_user = content
                elif isinstance(content, list):
                    current_user = '\n\n'.join(
                        item.get('text', '') for item in content
                        if isinstance(item, dict) and item.get('type') == 'text'
                    )
                current_timestamp = timestamp
                current_assistant_texts = []

            elif role == 'assistant':
                content = msg.get('content', [])
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text = item.get('text', '')
                            if text:
                                current_assistant_texts.append(text)

        except:
            pass

if current_user:
    assistant_full = '\n\n'.join(current_assistant_texts)
    pairs.append({
        'time': current_timestamp,
        'user': current_user,
        'assistant': assistant_full
    })

def remove_code_blocks(text):
    text = re.sub(r'```\w*\n?', '', text)
    text = re.sub(r'```', '', text)
    text = re.sub(r'~~~\w*\n?', '', text)
    text = re.sub(r'~~~', '', text)
    return text

pairs.sort(key=lambda p: p['time'])

output_lines = [f"Session Log - {date}", ""]

for pair in pairs:
    try:
        dt_utc = datetime.fromisoformat(pair['time'].replace('Z', '+00:00'))
        dt_kst = dt_utc + timedelta(hours=9)
        time_str = dt_kst.strftime('%H:%M')
    except:
        time_str = ""

    user_clean = remove_code_blocks(pair['user'])
    assistant_clean = remove_code_blocks(pair['assistant']) if pair['assistant'] else ""

    output_lines.append(time_str)
    output_lines.append(f"Paul : {user_clean}")
    output_lines.append("")

    if assistant_clean:
        output_lines.append(f"claude : {assistant_clean}")
        output_lines.append("")

with open(output, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
