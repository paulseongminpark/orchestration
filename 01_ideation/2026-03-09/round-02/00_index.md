# Ideation Index — 2026-03-09 Round 2

> 주제: mcp-memory NDCG q051-q075 개선
> 상태: Round 2 완료

## 문서

| # | 파일 | 내용 |
|---|------|------|
| 01 | 01_goldset-corrections.md | goldset 오류 3건 + 쿼리 정규화 2건 + 검색 실패 2건 분석 |
| 02 | 02_typed-vector-design.md | typed vector 강화 3방안 (동적 가중치 / guarantee slot / query decomposition) |

## 핵심 발견

ZERO 9건 분류:
- **goldset 오류 3건** (q065, q069, q074): relevant_ids가 쿼리와 무관한 노드 지정
- **vocabulary mismatch 3건** (q057, q060, q061): 같은 개념, 다른 어휘
- **검색 실패 2건** (q059, q073): summary 거의 동일인데 벡터 검색 실패
- **한계 1건** (q061): 쿼리가 너무 구체적

## 수정 영향 예상

| 수정 | 대상 | NDCG@5 변화 |
|------|------|------------|
| goldset 수정 | 3건 | ZERO → 0.3-0.5 |
| 쿼리 정규화 | 2건 | LOW → 0.4-0.6 |
| typed vector 강화 | 2건 | 코드 수정 필요 |

goldset + 쿼리만으로 q051-q075 NDCG@5 0.227 → ~0.30-0.35 예상.

## 추천 실행순서

1. goldset 수정 3건 (Paul 검증)
2. 쿼리 정규화 2건 (Paul 검증)
3. 방안 A 동적 가중치 (코드 수정, 단순)
4. 방안 B guarantee slot (보완)
5. 방안 C query decomposition (Phase 5 통합)

## 다음

- Implementation Design: goldset.yaml 수정 + hybrid.py 동적 가중치
