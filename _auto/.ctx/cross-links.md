# Cross-Project Links
> 자동 관리. 프로젝트 간 변경 영향도 추적.

## Active Relations (2026-03-08 23:27)

### tech-review ↔ portfolio
| 파일 | 변경 | 영향 | 상태 |
|------|------|------|------|
| sources.json | build-sources-feed.js 재실행 | TechReviewMultiSource.tsx fetch | active |
| youtube.html | TOC, 섹션번호, blue quote 렌더링 | sources.json 스키마 → portfolio 수신 | active |
| analyze-youtube.py | validate_quotes, key schema 갱신 | youtube.html apply_points {text, key} | active |
| TechReviewMultiSource.tsx | sources.json fetch URL 통합 | 3소스(Blog/YT/Twitter) 동기화 | active |

### portfolio → monet-lab
| 파일 | 변경 | 영향 | 상태 |
|------|------|------|------|
| deploy.yml | Vercel gh-pages 차단 해결 | CI/CD 동작 검증 | pending |
| aiWorkflowData.ts | 로컬 미커밋 변경 | AiWorkflowSection.tsx TS에러 | blocker |

### portfolio → tech-review
| 파일 | 변경 | 영향 | 상태 |
|------|------|------|------|
| STATE.md | v1.0-clean 반영 | 블로그 구조 검토 | review |

### monet-lab → portfolio
| 파일 | 변경 | 영향 | 상태 |
|------|------|------|------|
| AI_WORKFLOW_KO.md | 업데이트 | aiWorkflowData.ts 연쇄 | active |

## Pending Actions
1. **tech-review 세션 2**: sources.json 첫 실행 → portfolio fetch 동작 검증
2. **portfolio**: TechReviewMultiSource 자동 반영 확인 (sources.json 스키마 호환성)
3. **build-sources-feed**: bookmarks.json 갱신 시 sources.json 재생성 자동화 검증
4. **E2E 검증**: analyze-youtube → youtube.html → build-sources → portfolio 전체 파이프라인
5. **Vercel**: deploy.yml 변경 후 빌드 결과 모니터링
6. **monet-lab**: 44개 미커밋 파일 정리 스케줄
