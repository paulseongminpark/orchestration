# 세션 요약

> compressor 에이전트가 자동 업데이트합니다.
> /catchup 스킬로 읽습니다.

=== 컨텍스트 압축 요약 ===

세션 목표: monet-lab — PMCC 케이스 스터디 상세 페이지 CSS/MD 정비 + SurveyViz/SurveyTable 컴포넌트 구현

완료:
  - [CSS] wd-eyebrow/wd-title/wd-lede/wd-heading/wd-paragraph 타이포 클래스 정의
  - [CSS] 섹션 구분 padding 48px + borderBottom 1px #ccc, callout last-child border-bottom none
  - [EMPTY_HOUSE_CPS_DETAIL_KO.md] Overview/Approach/Results/Takeaways 섹션 분리, 이미지 포맷 수정
  - [SKIN_DIARY_DETAIL_KO.md] product_demo.mp4 → Overview 상단 배치, 섹션 정리
  - [PMCC_DETAIL_KO.md] Shift/Visual Cues → 독립 섹션(## 5, ## 6), 번호 재조정
  - [이미지] portfolio → /public/work/{empty-house-cps, skin-diary-ai, pmcc}/ 복사, 렌더링 확인
  - [SurveyViz.tsx] IntersectionObserver 수평 바 애니메이션 + 카운터 (94%, N=43) + Key Insight 박스
  - [SurveyTable.tsx] pmcc_survey.csv + pmcc_survey2.csv 병합 (N=43), 필터/페이지네이션/행 펼침
  - [파서] survey-viz, survey-table 블록 타입 추가 (`**[survey-viz]**`, `**[survey-table]**`)
  - 커밋 미완 (monet-lab 전체 변경사항 미커밋)

현재 상태: SurveyViz + SurveyTable 구현 완료, PMCC Instagram 이미지 개선 작업 남음. 미커밋 상태.

다음 할 것:
  1. monet-lab 변경사항 커밋 (commit-writer 호출)
  2. PMCC Instagram 이미지 — full-width 너무 큼, 그리드/캐러셀 형태로 개선
  3. tech-review: EN 번역 [1][2] 인용 마커 잔류 이슈 수정
  4. portfolio: 07~10 스크린샷 → lab.md 이미지 링크 추가
  5. portfolio: Obsidian 섹션 모바일 반응형 확인 (375px)

열린 결정:
  - PMCC Instagram 이미지 표시 방식 (그리드 vs 캐러셀)
  - SurveyTable Survey 1/2 필드 매핑 최종 검증 (N=43 맞는지)

주의사항:
  - monet-lab: master 브랜치
  - SurveyTable: Survey 1(38명) col5=rating, Survey 2(5명) col6=rating — 필드 오프셋 다름
  - SurveyViz: IntersectionObserver threshold 0.3 — 스크롤 진입 시 1회만 발동
  - 파서 블록: `**[survey-viz]**`, `**[survey-table]**` — MD에서 이 문자열 그대로 사용
  - decisions.md 미반영: pf 2건(07~10 스크린샷, Obsidian 모바일), tr 1건(EN 인용 마커)

=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===
