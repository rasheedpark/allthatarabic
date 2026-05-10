# 올댓아라빅 1.4.4 — 디자인 코드

각 앱의 목적과 용도에 맞게 디자인 시스템을 분리해 정의한다.

---

## 공통 디자인 토큰

```css
:root {
  --bg:          #F2F4F6;   /* 배경 */
  --surface:     #FFFFFF;   /* 카드/컨테이너 배경 */
  --accent:      #1D49FF;   /* 포인트 컬러 (파랑) */
  --text:        #12205A;   /* 본문 텍스트 */
  --sub:         #888FAC;   /* 보조 텍스트 */
  --border:      #D5DAE8;   /* 구분선 */
  --accent-soft: rgba(29,73,255,0.08);
  --accent-wash: #EAF0FF;
}
```

**공통 폰트**
| 용도 | 폰트 |
|---|---|
| 한국어 UI | Spoqa Han Sans Neo, Apple SD Gothic Neo |
| 아랍어 본문 | Noto Sans Arabic (weight 500/700) |
| 아랍어 쿠픽/쓰기 | Noto Kufi Arabic |
| 쓰기 애니메이션 | Dongol (로컬, `../assets/fonts/Dongol-Regular.otf`) |

---

## 선생님용 앱 (ata144_teacher)

**목적**: 오프라인/온라인 수업 현장, TV·모니터 등 대형 가로화면에서 선생님이 직접 조작하며 수업 진행.

### 레이아웃
- 전체: `position: fixed; overflow: hidden;` 풀스크린 슬라이드
- `#main`: 중앙 고정 컬럼 (`width: min(92vw, 1400px)`, flex column, 상하 패딩)
- `#arabic-area`: **반드시 `container-type: inline-size; width: 100%;`** (cqi 단위 사용)
- `#ui-tl`: 좌상단 고정 — 유닛명 + 섹션 탭
- `#ui-tr`: `#main` 내 상단 — 타입 레이블 + 라흐자 국기
- `#ui-bl`: 좌하단 고정 — 저작권
- `#ui-br`: 우하단 고정 — 로고
- `#toolbar`: 하단 중앙 — 단축키 바
- `#sidebar`: 좌측 슬라이드아웃 — 유닛 인덱스

### 아랍어 텍스트
```css
.arabic {
  font-family: 'Noto Sans Arabic', serif;
  font-size: clamp(3rem, 9vw, 9rem);
  font-weight: 700;
  direction: rtl;
  line-height: 1.6;
}
.arabic.arabic-sentence {
  font-size: clamp(2rem, 6vw, 6rem); /* 문장형 유닛(A/G) */
}
```

### 한국어/노트
```css
.korean {
  font-size: clamp(1.2rem, 3.5vw, 3.5rem);
  transition: opacity 0.3s;
}
.note {
  font-size: clamp(0.9rem, 2.2vw, 2.2rem);
  color: var(--sub);
  opacity: 1; /* 항상 표시 — 해석 토글 무관 */
}
```

### 섹션 탭 (`#section-tabs`)
```css
#section-tabs {
  display: flex; gap: 0.4rem; flex-wrap: nowrap; align-items: center;
}
.sec-tab {
  background: #fff; border: 1.5px solid var(--border); border-radius: 6px;
  font-size: clamp(0.5rem, 0.85vw, 0.68rem); line-height: 1.3;
  padding: 2px 9px; white-space: nowrap;
}
.sec-tab small { display: block; font-size: 0.85em; opacity: 0.7; }
.sec-tab.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.sec-tab.disabled { opacity: 0.25; pointer-events: none; }
```

탭 구성: `패턴<small>한국어명</small>` (패턴별 동적) + `연습/표현/지문/단어` (고정)

### Write 애니메이션 모드 (`css = 'write'`)
```css
#arabic-area {
  container-type: inline-size; /* ⚠️ cqi 단위 사용을 위해 필수 */
  width: 100%;
}
.write-pair-row {
  display: flex; flex-direction: row-reverse; align-items: baseline;
  gap: clamp(4px, calc(12cqi / var(--items, 4)), 20px);
}
.write-arabic-letter {
  font-family: 'Dongol', 'Noto Kufi Arabic', serif;
  font-weight: 400;
  font-size: clamp(3.5rem, calc(90cqi / var(--items, 3)), 10rem);
  color: var(--text); line-height: 1;
}
.write-token {
  display: inline-block; vertical-align: baseline;
  clip-path: inset(-40% 0% -40% 100%); /* 초기: 완전 숨김 */
  /* 애니메이션: clip-path inset(-40% 0% -40% 0%) 으로 전환 */
}
.write-pair-label {
  font-size: clamp(0.6rem, 1.2vw, 0.85rem);
  color: var(--sub); text-align: center;
}
```

JS 와이프 타이밍:
```javascript
const wipeDuration = 0.5 + charCount * 0.5; // 글자 수 비례 속도
setTimeout(() => {
  token.style.transition = `clip-path ${wipeDuration}s linear`;
  requestAnimationFrame(() => {
    token.style.clipPath = 'inset(-40% 0% -40% 0%)'; // 등장
  });
}, 400 + i * (wipeDuration * 1000 + 600)); // 순차 지연
```

### Baseline 모드 (`css = 'baseline'`)
```css
.bl-wrap { position: relative; width: 100%; }
.bl-line { position: absolute; left: 0; right: 0; height: 1.5px; background: rgba(29,73,255,0.3); }
.bl-grid {
  display: grid;
  grid-template-columns: repeat(var(--items, 5), 1fr);
  direction: rtl;
  column-gap: clamp(6px, 3vw, 28px);
}
.bl-letter {
  font-family: 'Noto Sans Arabic', serif;
  font-size: clamp(3rem, calc(56vw / var(--items, 4)), 9rem);
  font-weight: 700;
}
.bl-label {
  font-size: clamp(0.6rem, 1.2vw, 1rem); color: var(--sub);
}
```

### Book View 모드 (`B` 키)
`body.book-view` 클래스 토글로 동작.
- 슬라이드 UI 전체 숨김 (`#main`, `#sidebar`, `#toolbar`, `#ui-*` → `display: none !important`)
- `#book-root` 표시 → B5 비율 페이지 카드 렌더링
- 용도: 교재 초안 PDF 출력을 위한 미리보기

```css
body.book-view { overflow: auto; height: auto; }
#book-root { display: none; }
body.book-view #book-root { display: flex; flex-direction: column; align-items: center; }
.book-page {
  width: min(92vw, 860px);
  aspect-ratio: 176 / 250;
  min-height: 1220px;
  background: var(--surface);
  box-shadow: 0 22px 70px rgba(18,32,90,0.16);
}
```

### 라흐자(방언) 국기 표시
타입 레이블 옆에 원형 국기 아이콘.
```javascript
const LAHJA_FLAG = {
  EGY: '../assets/icons/icon-egypt.png',
  LEV: '../assets/icons/icon-lebanon.png',
  GLF: '../assets/icons/icon-saudi.png',
};
// 렌더: <img src="..." style="width:1.1em;height:1.1em;border-radius:50%;">
```

### 하이라이트 마크업 규칙
시트 `arabic`/`korean`/`note` 컬럼에서 사용 가능한 인라인 마크업:
- `_단어_` → `.highlight-box` (파란 테두리 상자)
- `*단어*` → `.highlight-text` (파란 강조 텍스트)

---

## 학생용 앱 (ata144_student)

**목적**: 모바일에서 혼자 복습. 배운 패턴 반복 연습. 레퍼토리 슬라이드 생략.

### 레이아웃
- 전체: `position: fixed; overflow: hidden;` 풀스크린 슬라이드
- 세로(모바일) 중심 레이아웃
- 하단: 이전/다음 버튼 (터치 스와이프 + 버튼)
- 사이드바: 유닛 인덱스 (M키 또는 버튼)

### 아랍어 텍스트
```css
.arabic-text {
  font-family: 'Noto Sans Arabic', serif;
  font-size: clamp(2.5rem, 12vw, 6rem);
  font-weight: 700; direction: rtl;
}
```

### 의미 토글
- 한국어(`.korean-text`): 토글 시 `display: none`
- 음가(`.note-text`, romanization): **항상 표시** — 토글 무관
```css
.app.meaning-hidden .korean-text { display: none; }
.app.meaning-hidden .ptn-summary { display: flex !important; }
/* .note-text는 토글 영향 없음 — opacity: 1 고정 */
```

### 패턴 요약 (ptn summary)
패턴 슬라이드에서 한국어 의미 가릴 때 표시되는 음가 힌트 영역.
```css
.ptn-summary { display: none; /* 기본 숨김 */ }
.app.meaning-hidden .ptn-summary { display: flex !important; }
```

### 하이라이트 마크업
선생님용과 동일하나 클래스명 다름:
- `_단어_` → `.hl-box` (파란 테두리)
- `*단어*` → `.hl-bold` (볼드 강조), 아랍어면 `.hl-ar` 추가

---

## 교재용 앱 (ata144_textbook)

**목적**: 모바일 기기에서 교재를 읽는 경험. 스크롤 기반. 실험 버전.

별도 디자인 시스템 — `product-ata144-design(mobile).md` 참고.

---

## 교재 인쇄 원본 (ata144_original)

**목적**: B5 인쇄용 교재 원본. 데스크톱 미리보기 = 인쇄물 1:1 매칭. PDF 생성용.

**파일**: `ata144_original/ata144_original.html`

**페이지 사이즈**: B5 (182mm × 257mm). CSS `width: 182mm; height: 257mm`로 화면-인쇄 매칭. 표현·드릴·나쓰는 콘텐츠 양에 따라 `min-height: 257mm; overflow: visible` 허용, 패턴 페이지는 고정 B5.

**디자인 토큰**: 공통 디자인 토큰을 그대로 사용. 카드형 본문(표현·나쓰·디폴트 드릴)은 공용 변수로 통일:
- `--textbook-card-ar-size: 1.18rem` (아랍어 본문)
- `--textbook-card-trans-size: 0.74rem` (음가 라인)

`css = 'five'` 좁은 5열 셀은 위 공용 토큰에 연동하지 않고 별도 크기 유지.

**구조 / 페이지 분할 / 안내문 규칙 / 박스 그룹핑** 등 교재 양식 본문 규칙은 `product-ata144.md`의 "교재양식 Textbook Layout" 절 참고.

---

## 앱별 비교 요약

| 항목 | 선생님용 | 학생용 | 교재용 앱 | 교재 원본 (인쇄) |
|---|---|---|---|---|
| 화면 | 대형 가로 (TV/모니터) | 모바일 세로 | 모바일 세로 | B5 데스크톱·인쇄 |
| 이동 방식 | 키보드 ←→ | 스와이프 + 버튼 | 스크롤 | 스크롤 (페이지 단위) |
| 레퍼토리 | ✅ 표시 | ❌ 생략 | ✅ 표시 | ✅ 표시 |
| Write 애니메이션 | ✅ | — | — | — |
| Book View | ✅ (B키) | — | — | — (그 자체가 book) |
| 라흐자 국기 | ✅ | ✅ | — | ✅ |
| 의미 토글 | Space 키 | 버튼 | — | — |
| 음가 항상 표시 | ✅ | ✅ | — | ✅ |

---

## CSS 코드 (시트 `css` 컬럼)

각 데이터 행의 `css` 값으로 표시 양식·노출 범위를 제어한다.

### `ab` — 앱 전용 스크립트 (App-only script)

`css = 'ab'` 으로 지정된 행은 **행 자체는 양쪽 모두 노출**되지만, **`script`(설명) 컬럼만 인쇄 교재(`ata144_original`)에서 숨겨지고**, **앱(`ata144_textbook` 등)에서는 정상 노출**된다.

| 적용 대상 | arabic / korean / note | script (설명) |
|---|---|---|
| 교재 인쇄 원본 (`ata144_original`) | 정상 노출 | **숨김** |
| 교재용 앱 (`ata144_textbook`) | 정상 노출 | 정상 노출 |
| (선생님용 / 학생용) | — | 현재 미적용 |

**용도**: 어휘·문장 자체는 인쇄 교재에도 들어가야 하지만, 부가 설명(`script`)은 인쇄에 넣기엔 분량 과다 / 인터랙션 전제 / 모바일 확장 의도일 때.

**적용 대상 필드**: 현재는 `script` 컬럼만. (다른 필드 확장 시 본 표 갱신)

**구현 위치 (인쇄 교재)**: `isAppOnly(row)` 헬퍼 + 두 렌더 지점:
- `renderPatternPage()` — `pattern.script` 출력 분기
- `renderExpressionPage()` 카드 빌더 — `exp.script` 출력 분기

```javascript
function isAppOnly(row) {
  return (row?.css || '').trim().toLowerCase() === 'ab';
}
// 렌더 지점:
${pattern.script && !isAppOnly(pattern) ? `<div class="pattern-script">…</div>` : ''}
const script = exp.script && !isAppOnly(exp) ? `<div class="exp-script">…</div>` : '';
```
