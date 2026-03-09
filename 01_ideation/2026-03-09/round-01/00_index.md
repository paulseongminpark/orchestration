# Ideation Index — 2026-03-09 Round 1

> 주제: mcp-memory NDCG q051-q075 개선
> 상태: Round 1 완료

## 문서

| # | 파일 | 내용 |
|---|------|------|
| 01 | 01_ndcg-q051-q075-analysis.md | 병목 분석 + 개선 방향 4가지 |

## 핵심 발견

- q051-q075 NDCG@5=0.227 (전체 병목), q001-q025=0.604 (양호)
- 근본 원인 3가지: FTS trigram 한계, vocabulary mismatch, RRF 후보풀
- ZERO 쿼리 9건 (36%)

## 추천 실행순서

1. 파라미터 튜닝 (high_thresh, 후보풀)
2. goldset 쿼리 정규화 (Paul 검증)
3. typed vector 강화
4. query expansion (Phase 5 통합)

## 실험 결과

- 방향 1 (top_k 2배 확장): **역효과** — 전체 NDCG@5 -0.051. 노이즈 증가.
- 단순 파라미터 튜닝 불가. 알고리즘 수정 필요.

## 다음

- Round 2: 방향 2 goldset 쿼리 정규화 초안 + 방향 4 typed vector 설계
