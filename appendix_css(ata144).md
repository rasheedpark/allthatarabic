# 부록: CSS 코드 정의 — ATA 1.4.4

> 이 문서는 `product(ata144).md`의 CSS 코드 섹션에 대한 부록이다.  
> 앱(`app144.html`, `app144s.html`)에서 사용되는 CSS 클래스를 타입별로 정리한다.  
> 색상·크기 변수는 `:root`에 정의된 디자인 토큰(`--bg`, `--accent` 등)을 공유한다.

---

## 디자인 토큰 (공통 변수)

```css
:root {
  --bg:        #F2F4F6;
  --surface:   #ffffff;
  --accent:    #1D49FF;
  --accent-bg: rgba(29,73,255,0.08);
  --text:      #12205A;
  --sub:       #888FAC;
  --border:    #D5DAE8;
  --r-sm: 8px; --r-md: 12px; --r-lg: 18px;
  --font-kr: 'Spoqa Han Sans Neo','Apple SD Gothic Neo',sans-serif;
  --font-ar: 'Noto Sans Arabic',serif;
}
```

---

## 슬라이드 공통 클래스

### 아랍어 본문
```css
.arabic-text {
  font-family: var(--font-ar);
  font-size: clamp(3rem, 9cqi, 8rem);
  font-weight: 700; line-height: 1.6;
  text-align: center; direction: rtl;
  color: var(--text);
}
```

### 한국어
```css
.korean-text {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  color: var(--text); line-height: 1.55; text-align: center;
}
```

### 노트
```css
.note-text {
  font-size: clamp(.85rem, 2vw, .95rem);
  color: var(--sub); line-height: 1.55; text-align: center;
}
```

### 인라인 강조

`_텍스트_` → 하이라이트 박스 / `*텍스트*` → 볼드 강조

```css
.hl-box {
  display: inline-block;
  border: 2.5px solid var(--accent);
  background: rgba(29,73,255,0.08);
  border-radius: 10px;
  padding: .15em .4em; margin: 0 .1em;
  vertical-align: middle; line-height: 1.3;
}
.hl-bold { font-weight: 700; color: var(--accent); }
```

---

## 타입별 고유 클래스

### ptn (패턴)

ptn 슬라이드는 아랍어 + 한국어 + 노트 위에 `summary` 열 내용을 산문/불릿으로 추가 렌더링한다.

```css
/* summary 본문 영역 */
.ptn-summary {
  display: flex; flex-direction: column; gap: 8px;
  max-width: 540px; width: 100%; align-self: center;
  direction: ltr; margin-top: 4px;
}

/* 산문 단락 */
.ptn-prose {
  font-size: clamp(.85rem, 2cqi, .95rem);
  line-height: 1.85; color: var(--sub);
  text-align: left; white-space: pre-line;
}

/* 불릿 항목 */
.ptn-bullet {
  display: flex; gap: 8px; align-items: flex-start;
  font-size: clamp(.82rem, 1.8cqi, .9rem);
  line-height: 1.7; color: var(--text); text-align: left;
}
.ptn-bullet-dot {
  color: var(--accent); font-size: 14px;
  flex-shrink: 0; margin-top: 2px;
}
.ptn-spacer { height: 8px; flex-shrink: 0; }
```

---

### nass (나스)

나스 슬라이드는 아랍어 지문 + 질문(sual) + 한국어 힌트 + 본문 토글 버튼으로 구성된다.

```css
/* 지문 아랍어 */
.nass-arabic {
  font-family: var(--font-ar);
  font-size: clamp(1rem, 3.5cqi, 1.65rem);
  font-weight: 400; line-height: 2;
  text-align: center; direction: rtl;
  color: var(--text);
}

/* 질문(sual) */
.nass-sual {
  font-family: var(--font-ar);
  font-size: clamp(.9rem, 3vw, 1.1rem);
  font-weight: 500; color: var(--sub);
  direction: rtl; text-align: center;
  line-height: 1.8; white-space: pre-line; opacity: .85;
}

/* 한국어 힌트 */
.nass-hint {
  font-size: clamp(.75rem, 2.5vw, .9rem);
  color: var(--sub); text-align: center; line-height: 1.6;
}

/* 본문 토글 버튼 */
.passage-btn {
  display: block; width: 100%; padding: 11px 16px;
  background: none; border: 1.5px solid var(--border);
  border-radius: var(--r-md); color: var(--sub);
  font-size: 14px; font-weight: 600; text-align: center;
}
.passage-btn.active { border-color: var(--accent); color: var(--accent); }

/* 본문 영역 */
.passage-wrap {
  padding: 16px; background: #f9fafc;
  border: 1px solid var(--border); border-radius: var(--r-md);
  text-align: center;
}
```

---

### repertory · mithāl · drillA · exp · kalimat

위 타입들은 공통 슬라이드 구조(`renderNormal`)를 사용한다.  
`.arabic-text` + `.korean-text` + `.note-text` 순으로 렌더링되며, 추가 고유 클래스 없음.

---

## 해석 토글 (사용자용 앱)

```css
/* 해석 가리기 상태일 때 한국어·노트 숨김 */
.app.meaning-hidden .korean-text,
.app.meaning-hidden .note-text { display: none; }

/* 해석 가리기 상태에서도 ptn summary는 항상 표시 */
.app.meaning-hidden .ptn-summary { display: flex !important; }
```

---

## UI 컴포넌트 (선생님용 앱)

### 로딩 화면
```css
#loading {
  position: fixed; inset: 0;
  background: var(--accent);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 1.4rem; z-index: 999;
}
#loading img { width: clamp(80px,12vw,140px); filter: brightness(0) invert(1); }
#loading .loading-label {
  font-size: clamp(0.7rem,1.2vw,0.95rem);
  color: rgba(255,255,255,0.75);
  letter-spacing: 2.5px; text-transform: lowercase;
}
```

### 섹션 탭
```css
.sec-tab {
  border: 1px solid var(--border); border-radius: 6px;
  font-size: clamp(0.5rem, 0.85vw, 0.68rem);
  padding: 2px 9px;
}
/* 활성 탭 */
.sec-tab.active { background: var(--accent); color: #fff; }
/* 해당 타입 없음 */
.sec-tab.disabled { opacity: 0.2; pointer-events: none; }
```

### 인덱스 항목 (사이드바)
```css
.idx-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px; font-size: 15px;
  color: var(--text); cursor: pointer;
  border-left: 3px solid transparent;
}
.idx-item.active {
  background: var(--accent-bg); color: var(--accent);
  border-left-color: var(--accent);
}
```
