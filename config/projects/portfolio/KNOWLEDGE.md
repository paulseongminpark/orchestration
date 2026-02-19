# KNOWLEDGE — Best Practices

포트폴리오 프로젝트 모범 사례, 규칙, 패턴.

---

## Git 규칙

### 브랜치
- **portfolio**: master 브랜치 (GitHub Pages 호환)
- ❌ main 브랜치 사용 금지 (이 프로젝트에서만)

### 커밋 메시지
```
형식: [portfolio] 한줄 설명

예시:
✅ [portfolio] 랜딩 페이지 반응형 개선
✅ [portfolio] About 섹션 콘텐츠 추가
❌ update
❌ fix
```

**필수**:
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 워크플로우
```bash
# 작업 완료 후
> /verify              # 검증
> /sync                # STATE.md 갱신 + 커밋+푸시 (향후)

# 전체 프로젝트 동기화
> /sync-all
```

---

## 파일 구조

### context/ (프로젝트 컨텍스트)
```
context/
├── STATE.md         # 지금 상태
├── PLANNING.md      # 아키텍처 결정
├── KNOWLEDGE.md     # 모범 사례 (이 파일)
└── logs/
    └── YYYY-MM-DD.md  # 시간순 로그
```

### STATE.md 형식
```markdown
## 현재 상태 (YYYY-MM-DD 기준)

**완료**
- 기능/섹션 설명

**진행 중**
- 작업 중인 항목

**다음 할 일**
- 우선순위 작업

**막힌 것**
- 없음 (또는 블로커)
```

---

## 프론트엔드 규칙

### 반응형
- Mobile First
- 브레이크포인트: 768px, 1024px, 1440px

### 접근성
- 시맨틱 HTML
- ARIA 레이블
- 키보드 내비게이션
- 색상 대비 (WCAG AA)

### 성능
- 이미지 최적화 (WebP)
- Lazy loading
- 코드 스플리팅
- LCP < 2.5s

---

## 배포

### GitHub Pages
- URL: https://paulseongminpark.github.io/portfolio_20260215
- 브랜치: master
- 자동 배포: push 시 자동

### 환경
- Production: GitHub Pages
- Development: 로컬 (npm run dev)

---

## 참고

- [PLANNING.md](./PLANNING.md): 아키텍처 결정 기록
- [STATE.md](./STATE.md): 현재 프로젝트 상태
- [GitHub: portfolio_20260215](https://github.com/paulseongminpark/portfolio_20260215)
