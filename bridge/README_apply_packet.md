# apply_packet.ps1

PACKET을 클립보드에서 읽어 context-repo에 적용하고 커밋/푸시하는 스크립트.

## 사용법

1. ChatGPT에서 PACKET 전체(`[PACKET]`~`[/PACKET]`)를 복사
2. 실행:

```powershell
powershell -ExecutionPolicy Bypass -File bridge/apply_packet.ps1 -FromClipboard -Commit
```

`-Commit` 생략 시 파일만 변경하고 커밋하지 않음.

## 실패 시 확인

| 파일 | 내용 |
|---|---|
| `bridge/packet.txt` | 클립보드에서 읽은 PACKET 원본 |
| `bridge/packet.patch` | 추출된 diff 패치 |

- **"PACKET markers not found"** → 클립보드에 `[PACKET]`/`[/PACKET]` 마커가 없음
- **"No diff block found"** → PACKET 안에 ` ```diff ``` ` 블록이 없음
- **"Patch check failed"** → diff가 현재 파일 상태와 맞지 않음. `packet.patch` 확인
