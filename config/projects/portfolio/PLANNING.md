# PLANNING — Architecture Decisions

포트폴리오 프로젝트의 아키텍처 결정 기록 (ADR).

---

## D-003: 리포지토리 재생성 (2026-02-15)

**문제**: portfolio_ui_test_v2 이름이 불명확, 테스트용 느낌

**결정**: portfolio_20260215로 리포지토리 이름 변경
- 구 portfolio는 아카이브
- 새 리포: portfolio_20260215

**이유**:
- 명확성: 날짜 기반 버전 관리
- 정리: 테스트 레거시 제거
- 프로페셔널: 포트폴리오 용도 명확화

**영향**:
- GitHub 리포 rename
- 로컬 remote URL 업데이트
- STATE.md URL 변경

---

## D-002: master 브랜치 유지 (2026-02-15)

**문제**: GitHub Pages 기본 브랜치 전환 이슈

**결정**: master 브랜치 계속 사용
- orchestration: main
- portfolio: master (유지)

**이유**:
- 안정성: GitHub Pages 기존 설정 유지
- 레거시: 기존 히스토리 보존
- 충돌 방지: 브랜치 전환 리스크 회피

**영향**:
- Git 워크플로우에서 master 브랜치 명시
- /sync-all에서 브랜치 구분

---

## D-001: 3-Layer 로깅 채택 (2026-02-16)

**문제**: 포트폴리오도 STATE.md만 있고 로그 누락

**결정**: orchestration과 동일한 3-Layer 구조
- Layer 1: STATE.md
- Layer 2: logs/날짜.md
- Layer 3: 03_evidence/

**이유**:
- 일관성: 모든 프로젝트 동일 구조
- 추적성: 변경 이력 보존
- 토큰 효율: 고수준만 읽기

**영향**:
- context/logs/ 디렉토리 생성
- /sync 스킬 적용 (향후)

---

## 템플릿

### D-XXX: 결정 제목 (YYYY-MM-DD)

**문제**: 무엇이 문제였는가

**결정**: 어떻게 해결했는가

**이유**:
- 왜 이 방법을 선택했는가
- 어떤 이점이 있는가

**영향**:
- 시스템에 어떤 변화가 생겼는가
- 어떤 파일/워크플로우가 변경되었는가

**대안 고려** (선택):
- 고려했지만 채택하지 않은 방법
- 왜 기각했는가
