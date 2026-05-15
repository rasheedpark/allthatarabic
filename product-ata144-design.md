# 올댓아라빅 1.4.4 — 디자인 코드

ATA 1.4.4의 모든 산출물(인쇄 교재 + 3개 앱)에 일관되게 적용되는 디자인 시스템을 정의한다.

각 산출물의 디자인 코드는 **공통 기본값**(토큰 + 타이포그래피 규칙)을 표준으로 따르고, 산출물별 섹션에서는 **그 산출물 고유의 차이**(레이아웃·인터랙션·크기 조정 등)만 명시한다. 인쇄 교재(`ata144_textbook_original.html`)에서 정한 값을 1차 표준으로 삼고, 다른 앱들은 화면 크기·용도에 맞게 **사이즈만** 조정한다 (weight·정렬·색은 동일).

---

## 1. 공통 기본값 (Defaults)

### 1.1 디자인 토큰

```css
:root {
  --bg:          #F2F4F6;   /* 배경 (쿨그레이) */
  --surface:     #FFFFFF;   /* 카드/컨테이너 배경 */
  --accent:      #1D49FF;   /* 포인트 컬러 (브랜드 파랑) */
  --hl-text:     #3554C6;   /* 본문 강조 (*...* 마크업) */
  --text:        #1a1f29;   /* 본문 텍스트 — 부드러운 검정 (네이비 #12205A 폐기됨) */
  --sub:         #6E7591;   /* 보조 텍스트 (음가, 캡션, 라벨) */
  --border:      #D5DAE8;   /* 구분선 */
  --accent-soft: rgba(29,73,255,0.08);  /* 활성 상태 배경 */
  --accent-wash: #EAF0FF;               /* 옅은 액센트 */
  --shadow:      0 1px 3px rgba(29,73,255,0.06), 0 0 0 1px rgba(29,73,255,0.03);
}
```

> **컬러 규칙 (전체 적용)** — 본문 폰트 컬러는 모든 산출물에서 `--text: #1a1f29` (부드러운 검정 계열)로 통일한다. 옛 브랜드 네이비 `#12205A`는 폐기. 액센트(`--accent`, `--hl-text`)는 강조 라벨이나 마크업에만 제한적으로 사용.

### 1.2 폰트 패밀리

| 용도 | 폰트 |
|---|---|
| 한국어 UI / 본문 | Spoqa Han Sans Neo, Apple SD Gothic Neo, sans-serif |
| 아랍어 본문 | Noto Sans Arabic (weight 400 / 500 / 700) |
| 아랍어 쿠픽 / 쓰기 | Noto Kufi Arabic |
| 쓰기 애니메이션 | Dongol (로컬 — `assets/fonts/Dongol-Regular.otf`) |

---

## 2. 공통 타이포그래피 규칙

### 2.1 아랍어 weight

| 데이터 타입 | weight | 비고 |
|---|---|---|
| 패턴(ptn) 메인 헤드라인 | **700** | 헤드라인급 강조 |
| 표현(exp) 카드 메인 | **700** | 단순 표현은 굵게 |
| 레퍼토리(rep) · 드릴(drillA/B) 셀 | **500** | 그리드/표 안의 본문 — 통통하지 않게 |
| 나스(nass) 본문 지문 | **500** | 긴 호흡의 지문 — 가독성 우선 |
| 유닛 헤더 / UI 라벨 | **700** | 짧은 라벨류 |

> **원칙**: 짧고 강조되어야 하는 텍스트(헤드라인·라벨·핵심 표현)는 **700**, 표·셀·지문 등 본문성 텍스트는 **500**. 두 단계만 사용. `600`은 사용 금지.

### 2.2 한국어 weight

| 용도 | weight |
|---|---|
| 본문 한국어 (의미·해석) | **400** — 볼드 사용 안 함 |
| UI 라벨 / 헤더 | **700** |
| 강조 (`*...*` 마크업) | **700** + `--hl-text` 색 |

> **원칙**: 본문 한국어는 절대 볼드를 쓰지 않는다. `.m-card.exp .m-ko { font-weight:600 }` 같은 카드 타입별 override 패턴은 금지.

### 2.3 한국어 ↔ 아랍어 정렬 (좌우 페어 양식)

한국어와 아랍어가 좌우로 나란히 배치되는 카드(표현/나스 등):

```css
.m-pair { align-items: baseline; }   /* ✓ 표준 */
/* align-items: start;  ← 금지 — 디아크리틱이 위로 튀어나가 한국어가 떠 보임 */
/* align-items: center; ← 금지 — 두 언어 라인이 안 맞음 */
```

또한 아랍어 컨테이너에 `padding-top`을 두지 않는다 (한국어와 같은 Y 좌표에서 시작해야 베이스라인 정렬이 정확).

> **이유**: 아랍어는 발음 부호(ـَـ، ـُـ 등)가 글자 위로 튀어나오기 때문에, 박스 윗변(start) 기준으로 정렬하면 한국어가 시각적으로 위로 떠 보인다. 베이스라인 기준이 인쇄 교재와 동일한 자연스러운 정렬을 만든다.

---

## 3. 교재 (인쇄 B5) — `ata144_textbook_original.html`

**목적**: B5 인쇄용 마스터. 디자인 표준의 1차 출처. 다른 산출물은 이 값을 비례 조정해 사용.

### 3.1 페이지 / 레이아웃

- 페이지: B5 (176mm × 250mm)
- `body.book-view` 또는 단일 출력 모드
- 페이지 헤더(상단) + 본문 영역 + 페이지 푸터(하단 페이지 번호) 구조

### 3.2 폰트 사이즈 기준 (베이스)

| 용도 | 사이즈 |
|---|---|
| 패턴 아랍어 (헤드라인) | clamp(3rem, 9vw, 9rem) — 데스크 큰 화면 |
| 일반 카드 아랍어 | 본문 비례 |
| 본문 한국어 | 1rem 기준 |
| 음가 (note) | 0.78rem |

### 3.3 색·라인

- 카드 배경: `var(--surface)` 흰색
- 카드 그림자: 미세 (`var(--shadow)` 또는 인쇄용 단순 1px border)
- 구분선: `var(--border)` 또는 점선 회색

### 3.4 인쇄 출력 시 주의

- `@media print` 규칙으로 그림자/라운드 단순화
- 페이지 분할(`page-break-inside: avoid`)을 카드 단위로
- 자세한 인쇄 분할 로직은 `product-ata144.md`의 "드릴 페이지 분할" 섹션 참고

---

## 4. 교재용 앱 (모바일) — `ata144_textbook/ata144_textbook.html`

**목적**: 학생이 모바일 기기에서 교재 콘텐츠를 인터랙티브하게 학습. 스크롤 + 탭 재생 기반.

### 4.1 셸 구조

```
┌──────────────────────────┐
│ ☰  유닛 A01     1 / 6    │  ← 상단바 56px
├──────────────────────────┤
│ 표현 │ 패턴 │ 드릴 │ 지문 │  ← 섹션 탭 44px
├──────────────────────────┤
│  [현재 페이지 콘텐츠]      │  ← 스크롤
├──────────────────────────┤
│ ◀  01 / 06  ▶  해석 가리기 │  ← 하단바 64px
└──────────────────────────┘
```

- 컨테이너: `max-width: 640px` 중앙 정렬
- 데스크탑(660px+): 양쪽 28px 마진 + border-radius — 카드형
- 모바일: 100dvh 풀스크린

### 4.2 모바일 폰트 사이즈

| CSS 변수 | 값 | 용도 |
|---|---|---|
| `--ko-size` | `12px` | 본문 한국어 (모바일 뉴스 본문 수준) |
| `--trans-size` | `11px` | 음가 |
| `--script-size` | `12px` | 패턴 설명 텍스트 |
| `--ar-card-size` | `clamp(1.05rem, 4.3vw, 1.2rem)` | 표현 카드 아랍어 |
| `--ar-nass-size` | `clamp(1rem, 4vw, 1.15rem)` | 나스 아랍어 |
| `--ar-pattern-size` | `clamp(1.55rem, 6.8vw, 2.05rem)` | 패턴 메인 아랍어 |

### 4.3 카드 공통

```css
.m-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: var(--shadow);
  padding: 13px 14px;
  display: flex; flex-direction: column; gap: 6px;
}
.m-page { padding: 12px 14px 18px; gap: 10px; }
```

### 4.4 카드 타입별

**표현(exp)**: 좌(한국어) - 우(아랍어 + 음가) 페어. `.m-pair` 사용. 베이스라인 정렬.
**패턴(ptn)**: 큰 아랍어 헤드라인 + 한국어 + 음가 + 설명(`.m-summary`).
**드릴(drillA/B)**: 5열 그리드(좁은 화면 4열). 셀 아랍어 `font-size: 15px; font-weight: 500`. 데이터에 `css=five`가 명시된 경우 한 단계 더 작게 (`13px`) — `.css-five` 클래스가 자동 부여됨.
**나스(nass)**: 멀티라인 아랍어 + 한국어. `line-height: 1.75` (지문은 줄간격 약간 좁힘).

### 4.5 인터랙션

- 아랍어 탭 → 오디오 재생 (`.tap-audio`, 재생 중 `.playing` 액센트 색)
- 한국어 가리기 토글 → `.app.hide-meaning .m-ko { visibility: hidden }`
- 섹션 탭 → 해당 섹션 첫 페이지로 점프
- 하단 ◀▶ 페이지 이동
- 사이드바 (☰) → 유닛 픽커

### 4.6 페이지 매핑

표현/패턴/드릴/지문 4개 섹션. 한 유닛의 페이지를 글로벌 시퀀스로 평탄화. 페이지 단위는 인쇄 교재와 1:1 매핑(권장) 또는 느슨한 매핑(추후 결정).

---

## 5. 학생용 앱 (모바일) — `ata144_student/ata144_student.html`

**목적**: 1.4.3 양식 기반 모바일 학생앱 (운영 중). 슬라이드 1장씩 + 스와이프 이동. **장기적으로 교재용 앱(4.)으로 통합 예정**.

> **5.0 1.4.3 legacy 앱 (병행 운영 중)**
>
> | 구분 | 파일 | 배포 |
> |---|---|---|
> | 메인앱 (선생님용) | `ata143_teacher/ata143_teacher.html` | https://rasheedpark.github.io/allthatarabic/ata143_teacher/ata143_teacher.html |
> | 복습앱 (학생용) | `archive/app143s.html` (제목 "올댓아라빅 복습 · v1.43", summary 슬라이드 포함) | https://rasheedpark.github.io/allthatarabic/archive/app143s.html |
>
> 1.4.4가 모든 유닛을 따라잡을 때까지 병행 운영. 1.4.4 완비 시 폐기.  
> 신규 css 모드(`nom` §8.3.7, `baseline2` §8.2.5)는 1.4.4와 동일하게 적용되어 있음.

### 5.1 셸

- 풀스크린 슬라이드 (`position: fixed; overflow: hidden;`)
- 세로(모바일) 중심 레이아웃
- 하단 이전/다음 버튼 + 좌우 스와이프
- 사이드바 (M키 또는 햄버거)

### 5.2 아랍어 텍스트

```css
.arabic-text {
  font-family: var(--font-ar);
  font-size: clamp(2.5rem, 12vw, 6rem);  /* 화면 가득 차게 큼 */
  font-weight: 700; direction: rtl;
}
```

### 5.3 의미 토글

- 한국어(`.korean-text`): `display: none`
- 음가(`.note-text`): **항상 표시** — 토글 무관
- 패턴 카드의 음가 힌트(`.ptn-summary`): 한국어 가릴 때 표시

```css
.app.meaning-hidden .korean-text { display: none; }
.app.meaning-hidden .ptn-summary { display: flex !important; }
```

### 5.4 레퍼토리 슬라이드

학생용은 레퍼토리 **생략** (수업 중 선생님이 따로 설명. 학생 복습용은 패턴+드릴만).

---

## 6. 선생님용 앱 — `ata144_teacher/ata144_teacher.html`

**목적**: 오프라인·온라인 수업 현장. TV·모니터 등 대형 가로화면. 선생님이 직접 슬라이드 조작.

### 6.1 셸

- 전체: `position: fixed; overflow: hidden;` 풀스크린 슬라이드
- `#main`: 중앙 고정 컬럼 (`width: min(92vw, 1400px)`, flex column)
- `#arabic-area`: **반드시 `container-type: inline-size; width: 100%;`** (cqi 단위 사용)
- `#ui-tl`: 좌상단 — 유닛명 + 섹션 탭
- `#ui-tr`: 상단 우측 — 타입 레이블 + 라흐자 국기
- `#ui-bl`: 좌하단 — 저작권
- `#ui-br`: 우하단 — 로고
- `#toolbar`: 하단 중앙 — 단축키 바
- `#sidebar`: 좌측 슬라이드아웃 — 유닛 인덱스

### 6.2 아랍어 텍스트 (옵션 C — baseline과 격차 좁힘)

```css
.arabic {
  font-family: var(--font-ar);
  font-size: clamp(3.5rem, 10vw, 9rem);   /* baseline(.bl-letter)과 동일 크기 */
  font-weight: 700;
  direction: rtl;
  line-height: 1.6;
}
.arabic.arabic-sentence {
  font-size: clamp(2.5rem, 8vw, 8rem);    /* 문장형 유닛(A/G) — 일반의 80% */
}
```

> **격차 정책**: baseline 큰 글자(`.bl-letter`)와 일반 아랍어(`.arabic`)는 **동일 크기**(10vw / max 9rem). 1280px 화면에서 둘 다 128px. 큰 화면에서도 9rem(144px)으로 같이 도달. sentence 모드는 비-sentence의 80%.

### 6.3 한국어 / 노트

```css
.korean {
  font-size: clamp(1.4rem, 4vw, 4rem);
  transition: opacity 0.3s;
}
.note {
  font-size: clamp(1.05rem, 2.6vw, 2.5rem);
  color: var(--sub);
  opacity: 1; /* 항상 표시 — baseline 음가 라벨(.bl-label)과 동일 크기 */
}
```

### 6.4 섹션 탭 (`#section-tabs`)

```css
.sec-tab {
  background: #fff; border: 1.5px solid var(--border); border-radius: 6px;
  font-size: clamp(0.5rem, 0.85vw, 0.68rem); line-height: 1.3;
  padding: 2px 9px; white-space: nowrap;
}
.sec-tab small { display: block; font-size: 0.85em; opacity: 0.7; }
.sec-tab.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.sec-tab.disabled { opacity: 0.25; pointer-events: none; }
```

**탭 구성** (좌→우, 데이터 없는 섹션은 disabled):

| 위치 | 라벨 (한국어/영어) | 매칭 슬라이드 타입 |
|---|---|---|
| 동적 (패턴 수만큼) | `패턴 / ptn001` — 패턴 번호 형식 (`id_ptn(no)`에서 `ptn\d+` 추출) | `ptn` (각 패턴별 첫 슬라이드로 점프) |
| 고정 | `드릴 / Drill A` | `drilla` |
| 고정 | `연습 / Drill B` | `drillb` |
| 고정 | `심화 / Drill C` | `drillc` |
| 고정 | `표현 / Expression` | `exp` |
| 고정 | `지문 / Nass` | `nass` |
| 고정 | `단어 / Kalimat` | `kalimat` |

```js
const SEC_FIXED = [
  { key:'drilla',  ko:'드릴', en:'Drill A'    },
  { key:'drillb',  ko:'연습', en:'Drill B'    },
  { key:'drillc',  ko:'심화', en:'Drill C'    },
  { key:'exp',     ko:'표현', en:'Expression' },
  { key:'nass',    ko:'지문', en:'Nass'       },
  { key:'kalimat', ko:'단어', en:'Kalimat'    },
];
```

**활성 규칙**:
- 현재 슬라이드가 `ptn`/`repertory`/`writing` → 가장 가까운 이전 `ptn` 슬라이드의 동적 패턴 탭 활성
- 현재 슬라이드가 `drilla` 이상 → 해당 고정 탭 활성 (drilla는 별도 탭으로 분리됨)

### 6.5 상단 좌측 유닛 라벨 (`#ui-tl`)

A01 유닛코드(작게) / ptnA 대표 아랍어 / 한국어 — 3행. 줄간격을 충분히 벌려 가독성 확보:

```js
// 인라인 스타일 — 슬라이드 갱신 시 매번 set
ui-tl.innerHTML = `
  <div style="display:flex;align-items:center;gap:1.4rem;">
    <div>
      <div style="font-size:clamp(0.45rem,0.7vw,0.6rem); text-transform:uppercase;
                   letter-spacing:2px; color:var(--sub); opacity:0.6;
                   margin-bottom:0.5rem;">${unitCode}</div>
      <div style="font-family:var(--font-ar); direction:rtl;
                   font-size:clamp(0.9rem,1.8vw,1.4rem); font-weight:700;
                   line-height:1.4; margin-bottom:0.35rem;">${ptnArabic}</div>
      <div style="font-size:clamp(0.6rem,1vw,0.85rem); color:var(--sub);
                   font-weight:400; line-height:1.5;">${unitKorean}</div>
    </div>
    <div id="section-tabs"></div>
  </div>`;
```

### 6.6 단축키 / 도구바

**도구바 (`#toolbar`, 4 버튼)**:

| 버튼 | 키 | 동작 |
|---|---|---|
| 메뉴 | `M` | 사이드바 토글 |
| 오디오 | `S` | 오디오 재생/정지 |
| 한국어 가리기 | `Space` | 한국어 의미 토글 (`해석` 아닌 `한국어 가리기` 라벨) |
| 본문 | `A` | 아랍어 본문 가리기/보기 (opacity 0) |

**키바인딩만 (UI 버튼 없음)**:

| 키 | 동작 |
|---|---|
| `←` `→` | 슬라이드 이동 |
| `T` | 나스 지문 토글 (T 버튼은 UI에서 제거됨 — 의미가 없어 생략, 키만 유지) |
| `B` | Book View 모드 토글 (인쇄 미리보기) |
| `Esc` | 사이드바 닫기 |

### 6.7 드릴 슬라이드 순서

선생님앱은 한 슬라이드에 한 행씩 표시. **드릴 순서**는:

1. **유닛 슬라이드**
2. **패턴 묶음** (각 패턴별로):
   - 패턴 본문
   - 예문 (repertory) — 옛 명칭 "레퍼토리"는 UI에서 "예문"으로 표기 (`TYPE_KO.repertory = '예문'`)
3. **모든 drillA 모음** — 패턴별 매칭(`ref_ptn`)을 먼저, 유닛 공통(`ref_ptn` 빈 행)을 마지막
4. **drillB → drillC**
5. **expression** (표현)
6. **nass** (지문)
7. **kalimat** (단어)

drillA가 패턴 묶음과 분리되어 모음으로 표시되는 점이 1.4.3과의 차이. 패턴 학습 후 "드릴" 탭 클릭 시 모든 drillA를 연속 학습 가능.

### 6.8 오디오 URL (1.4.4 신구조)

```js
function getAudioUrls(s) {
  if (s?.data?.url) return [s.data.url.trim()];
  const id = getRowId(s.data);
  const unit = (s.data?.u || s.pg || '').trim();
  if (!id || !unit) return [];
  const enc = encodeURIComponent(id.normalize('NFD')).replace(/%2C/gi, ',');
  const base = `https://storage.googleapis.com/all-that-arabic-14/audio/${unit}/${enc}`;
  return [base + '.mp3', base + '.wav'];  // mp3 우선 → wav 폴백
}
```

- 경로: `audio/{유닛코드}/{id}.{ext}` (옛 `listening144/` 구조 폐기)
- 확장자 우선순위: `.mp3` → 실패 시 `.wav` 시도 (audio-rules 규칙)
- `data.url` 컬럼이 있으면 그 값 우선

---

## 7. 산출물별 비교

| 항목 | 교재 (인쇄) | 교재용 앱 (모바일) | 학생용 앱 (모바일) | 선생님용 앱 | 1.4.3 복습용 (legacy) |
|---|---|---|---|---|---|
| 화면 | B5 종이 | 모바일 세로 | 모바일 세로 | 대형 가로 (TV) | 모바일 세로 |
| 이동 | (페이지 넘김) | 스크롤 + ◀▶ | 스와이프 + 버튼 | 키보드 ←→ | 스와이프 + 버튼 |
| 레퍼토리 | ✅ 표시 | ✅ 표시 | ❌ 생략 | ✅ 표시 | ✅ 표시 |
| Summary 슬라이드 | — | — | — | (B키 book view에 포함) | ✅ (패턴별 요약) |
| Write 애니메이션 | — | — | — | ✅ | ✅ |
| Book View | (자체) | — | — | ✅ (B키) | — |
| 라흐자 국기 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 의미 토글 | — | 버튼 | 버튼 | Space 키 | 버튼 |
| 음가 항상 표시 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 아랍어 탭 → 오디오 | — | ✅ | — | ✅ (S키) | — |
| `nom` / `baseline2` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `vlist` (어휘 2열) | — | — | — | — | ✅ (summary 슬라이드, §8.3.9) |

---

## 8. 커스터마이징 CSS 코드 (특수 마크업·렌더 모드)

데이터시트의 `arabic`/`korean`/`note`/`script` 컬럼에서 사용 가능한 인라인 마크업, 그리고 `css` 컬럼으로 활성화되는 특수 렌더 모드. 모든 산출물에서 동일한 의미로 처리한다 (다만 클래스명은 산출물마다 prefix가 다를 수 있음).

### 8.1 인라인 마크업

| 마크업 | 의미 | CSS |
|---|---|---|
| `*단어*` | 색 강조 (한국어·아랍어 공통) | `.hl-text` / `.hl-bold` — 700 + `--hl-text` |
| `_단어_` | 박스 강조 | `.hl-box` / `.hl-box-inline` — `border: 1.5px solid var(--accent)` + `border-radius: 6px` + `padding: .05em .35em` |
| `\n` 줄바꿈 | `<br>` 자동 변환 | (모든 컬럼) |
| `>` 줄 시작 | 인용 (`.quote`) | 패턴 `script`/`summary` 컬럼에서 |
| `- ` 줄 시작 | 불릿 (`.bullet`) | 패턴 `script`/`summary` 컬럼에서 |

> **주의**: `*` `_` 문자는 마크업 용도이므로 ID 슬러그 생성 시 제거된다 (`product-ata144.md`의 "ID 산출 규칙 v2" 참고).

### 8.2 `css = 'baseline'` (알파벳 페이지 전용 — 3행 표)

A01~A06, G 시리즈 등 알파벳/그룹 글자를 **3행 표**(글자 / 위치별 연결형 / 음가 라벨)로 표시. 둘째 줄 연결형이 비어있으면 2행만 렌더.

**데이터 형식 (`pattern.arabic`)**:
```
ب | ت | ث | ن | ي           ← 1줄: 단일 글자
ببب | تتت | ثثث | ننن | ييي  ← 2줄: 위치별 연결형 (옵션)
```
- `note` 컬럼 = 음가 라벨 (공백 또는 `|` 구분)
- 토큰 분리: `|` 있으면 `|`로, 없으면 공백으로

**렌더 구조**:
```html
<div class="bl-wrap">
  <div class="bl-line"></div>                     <!-- baseline 가로선 (JS 동적 위치) -->
  <div class="bl-grid has-triple" style="--items: 5">
    <!-- 행 1: 큰 글자 (.bl-letter)     × items -->
    <!-- 행 2: 연결형  (.bl-triple)     × items (옵션) -->
    <!-- 행 3: 음가    (.bl-label)      × items -->
  </div>
</div>
```

```css
.bl-wrap { position: relative; width: 100%; }
.bl-line { position: absolute; left: 0; right: 0; height: 1.5px; background: rgba(29,73,255,0.3); }
.bl-grid {
  display: grid;
  grid-template-columns: repeat(var(--items, 5), 1fr);
  direction: rtl;
  column-gap: clamp(6px, 3vw, 28px);
  row-gap: clamp(28px, 3vw, 48px);
}
.bl-letter {
  font-family: var(--font-ar);
  font-size: clamp(3.5rem, 10vw, 9rem);  /* 일반 .arabic과 동일 크기 (items 무관 고정) */
  font-weight: 700;
}
.bl-triple {
  font-family: var(--font-ar);
  font-size: clamp(1.1rem, 4vw, 3.5rem);  /* letter의 약 40% */
  font-weight: 500; line-height: 1.2; white-space: nowrap;
}
.bl-label {
  font-size: clamp(1.05rem, 2.6vw, 2.5rem);  /* 일반 .note와 동일 크기 */
  font-weight: 500; color: var(--sub);
}
```

**baseline 가로선 동적 정렬**: 폰트 로드 후(`document.fonts.ready`) 첫 `.bl-letter`에 `vertical-align: baseline` 프로브를 일시 삽입해 baseline y좌표 측정 → `.bl-line.style.top` 동적 설정. 폭 오버플로 시 `transform: scale()` 자동 축소.

### 8.2.5 `css = 'baseline2'` — 기준선 없는 표

`baseline`과 **완전히 동일한 3행 표** (글자 / 위치별 연결형 / 음가 라벨)이되 **가로 기준선(`.bl-line`)만 그리지 않는다**. 기준선이 시각적으로 부담스럽거나 학습 목적상 baseline 정렬을 강조하지 않는 페이지에서 사용 (예: 단순 글자 나열, 모음/하라카 조합 표, 후반 챕터의 단어 그룹 등).

**데이터 형식**: `baseline`과 동일 (`pattern.arabic`에 `|` 또는 공백으로 토큰 분리, `note` 컬럼은 음가).

**구현 옵션 (둘 다 허용)**:
1. **마커 클래스 방식**: 동일한 `renderBaseline()` 함수 호출 + `wrap`에 `.no-line` 클래스 부여 → CSS로 `.bl-line` 숨김
   ```css
   .bl-wrap.no-line .bl-line { display: none; }
   ```
2. **조건부 div 생성**: `renderBaseline(s, { noLine: true })`로 `.bl-line` div 자체를 안 만들고 `top` 측정 로직도 스킵 (성능 살짝 유리)

선택은 산출물별 자유 — 시각 결과는 동일. 선생님앱·교재앱은 보통 (1) 마커 방식이 간단.

**렌더 결과** (예: `baseline2` 5칸):
```html
<div class="bl-wrap no-line">
  <!-- .bl-line 없음 -->
  <div class="bl-grid has-triple" style="--items: 5">
    <!-- 글자 / 연결형 / 라벨 — baseline과 동일 -->
  </div>
</div>
```

**baseline ↔ baseline2 선택 기준**:
- `baseline`: 알파벳 입문, baseline 정렬 자체가 학습 포인트일 때 (예: A01~A06 챕터 0)
- `baseline2`: 글자가 이미 익숙해진 단계, 또는 표가 다른 메인 콘텐츠 옆에 부수적으로 들어가 가로선이 시각 노이즈가 될 때

### 8.3 `css = 'write'` (쓰기 애니메이션 — 선생님용 전용)

획 단위 와이프 애니메이션으로 글자가 그려지는 효과. Dongol 폰트 사용.

```css
#arabic-area {
  container-type: inline-size; /* ⚠️ cqi 단위 사용 필수 */
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
}
.write-token {
  display: inline-block;
  clip-path: inset(-40% 0% -40% 100%); /* 초기: 완전 숨김 */
  /* 애니메이션: clip-path inset(-40% 0% -40% 0%) 으로 전환 */
}
```

JS 와이프 타이밍:
```javascript
const wipeDuration = 0.5 + charCount * 0.5;  // 글자 수 비례 속도
setTimeout(() => {
  token.style.transition = `clip-path ${wipeDuration}s linear`;
  requestAnimationFrame(() => {
    token.style.clipPath = 'inset(-40% 0% -40% 0%)';  // 등장
  });
}, 400 + i * (wipeDuration * 1000 + 600));  // 순차 지연
```

### 8.3.5 드릴 빈칸 (`*...*` 마크업 → `.drill-blank`)

drillB 등에서 학생이 채워야 할 부분을 빈칸으로 표시. **글자는 보존하되 색만 투명**으로 만들고, 배경은 `::before` 의사 요소에 깐다.

```css
.drill-blank {
  display: inline;
  position: relative;
  color: transparent;
  padding: 0 3px;
}
.drill-blank::before {
  content: '';
  position: absolute;
  left: 0; right: 0;
  top: 50%;
  height: 1em;                        /* 글자 em 크기와 동일 */
  transform: translateY(-50%);
  background: rgba(18,32,90,0.08);
  border-radius: 3px;
  pointer-events: none;
}
```

> **왜 `::before`인가** — 인라인 요소에 `background`를 직접 주면 ascender/descender 영역까지 덮여 박스가 부풀고, **iOS Safari에서 인접 아랍어의 셰이핑(자간 연결)이 끊긴다**. ::before로 박스 높이를 `1em`으로 정확히 잡으면 본문 흐름은 그대로 유지되면서 시각적 빈칸만 표시.

> **글자를 보존하는 이유** — (1) Arabic shaping 연결 유지 (2) 박스 폭이 정답 글자만큼 자연스럽게 잡힘 (3) 학생이 답을 떠올리는 단서가 됨. 정답 표시는 `.drill-blank { color: var(--text) }`로 색만 풀면 됨.

> **금지** — `color: transparent` + `background: #E7EBF2` 직접 적용 + `padding: 0 3px` 패턴은 데스크탑에서 OK처럼 보여도 iOS에서 깨짐.

### 8.3.7 `css = 'nom'` (명사문 — 주어 ‖ 서술어 구분)

명사문(الجملة الاسمية, nominal sentence) 구조 — 동사 없이 **시작어(주어, مبتدأ)** + **서술어(خبر)** 로 이루어진 문장에서 두 구분을 시각적으로 미세하게 분리.

**데이터 형식**: 시트 `arabic` 컬럼(필요 시 `note`/한국어도)에 **`|`** 문자로 두 구분 사이를 표시.

```
أَنَا | طَالِب              ← arabic
anā | ṭālib                 ← note (선택)
나는 | 학생입니다              ← korean (선택)
```

`css = 'nom'`이면 렌더 시 `|`가 옅은 회색 세로 분리자로 치환된다 — 강한 시각 단절을 피하면서 두 구분의 경계를 인지할 수 있게.

**렌더 결과**:
```html
أَنَا<span class="nom-divider">|</span>طَالِب
```

```css
.nom-divider {
  display: inline-block;
  color: var(--sub);
  opacity: 0.4;
  font-size: 0.55em;     /* 부모 폰트의 55% — 세로 길이 작게 */
  font-weight: 200;      /* 얇게 (Extra Light) */
  margin: 0 0.5em;
  vertical-align: 0.2em; /* 살짝 위로 — 글자 중앙 부근 */
  user-select: none;
}
```

**적용 산출물**: 모든 산출물 (교재 인쇄·교재앱·학생앱·선생님앱)에 동일 처리. 인쇄 교재에서는 `|`가 잘 보이도록 `opacity: 0.5`로 살짝 진하게 가능.

**구현 패턴**:
```js
function applyNomDivider(html) {
  return html.replace(/\s*\|\s*/g, '<span class="nom-divider">|</span>');
}
// 슬라이드 렌더 시
let arHtml = parseText(d.arabic || '');
if (cssMode === 'nom') arHtml = applyNomDivider(arHtml);
```

**baseline과의 충돌 없음**: baseline 데이터의 `|`(토큰 구분자)는 `css = 'baseline'` 분기에서 별도 splitter로 처리되어 `nom-divider`와 만나지 않는다.

### 8.3.9 `css = 'vlist'` (어휘·동사 2열 목록 — summary 슬라이드)

**도입 배경 (2026-05-15)**: 1.4.3 복습앱 A06 같은 동사 변화 요약 슬라이드에서, 줄바꿈으로 구분된 여러 단어쌍(아랍어 + 번역)을 슬라이드 한 장에 정돈된 2열 테이블로 표시할 필요가 생김. 이름은 vocabulary list의 약자.

**데이터 형식**:
- `arabic`: 각 항목을 `\n`으로 구분. 예: `أَدْرُسُ\nأَذْهَبُ\nأَرْجِعُ`
- `korean` (또는 `note`): 같은 줄 수, 같은 순서로 번역. 예: `I study.\nI go.\nI return.`

**렌더 구조**:
```html
<div class="summary-vlist">          <!-- grid 2열 -->
  <div class="summary-vlist-ar">أَدْرُسُ</div>
  <div class="summary-vlist-tr">I study.</div>
  <div class="summary-vlist-ar">أَذْهَبُ</div>
  <div class="summary-vlist-tr">I go.</div>
  ...
</div>
```

```css
.summary-vlist {
  display: grid;
  grid-template-columns: minmax(0,1fr) minmax(0,1fr);
  column-gap: clamp(20px, 6cqi, 40px);
  row-gap: clamp(10px, 2.5cqi, 18px);
  align-items: baseline;
  max-width: 360px;
  margin: 0 auto;
}
.summary-vlist-ar { font-family: var(--font-ar); direction: rtl; text-align: right;
                    font-size: clamp(1.25rem, 3.4cqi, 1.85rem); font-weight: 700; }
.summary-vlist-tr { direction: ltr; text-align: left;
                    font-size: clamp(0.95rem, 2.4cqi, 1.15rem); }
```

**적용 범위**: 현재 1.4.3 복습앱(`archive/app143s.html`) summary 슬라이드 전용. 1.4.4에 확장하려면 해당 앱의 summary 렌더에 동일 분기 추가 필요.

### 8.3.10 RTL 자동 판정 — 산문·불릿·강조 마크업 (summary 스크립트)

**문제 (2026-05-15, 1.4.3 복습앱 A07)**:
1. RTL 문장 안에 `*…*` 강조가 끝부분에 오면 인접 문장부호(`.`)가 엉뚱한 위치로 재배치 — 인라인 강조 span에 bidi 격리가 없어 RTL 런이 끊김.
2. summary 스크립트의 불릿/산문이 아랍어로 시작해도 `direction: ltr` 하드코딩이라 LTR로 흐름.

**해결**:
- `.hl-bold` / `.hl-box`에 `unicode-bidi: isolate` — 강조를 독립 bidi 런으로 격리, 주변 중립문자 재배치 방지.
- `firstStrongDir(raw)` 헬퍼: 마크업(`* _ <tag>`) 제거 후 **첫 강한 방향 문자**를 검사 (Arabic 블록 → `rtl`, Latin/한글 → `ltr`). 산문 `<p>`·불릿 `<div>`에 결과를 `dir` 속성으로 부여.
- `dir="auto"`는 **부모 flex 컨테이너에서 비신뢰** — 안쪽 자식이 자체 `dir`을 가지면 부모 auto 계산이 그 서브트리를 건너뛰어 LTR로 떨어진다. 그래서 JS 명시 판정을 쓴다.
- 불릿 row가 `dir="rtl"`이면 flex 주축이 반전되어 점(•)이 자동으로 오른쪽.
- 산문/불릿 폰트: `font-family: var(--font-kr), var(--font-ar)` — 한국어=Spoqa, 아랍어=Noto Sans Arabic(글자별 폴백), 크기 ~0.82–1rem 소형.

**방향 판정 규칙 (최종, 2026-05-15)**:
- **산문 `<p>`: 항상 `dir="ltr"`** — 산문은 한국어 설명 텍스트. 방향 판정 안 함.
- **불릿 `row`: `firstStrongDir(첫 줄)` — 아랍어로 시작하면 RTL**(점 오른쪽), 한국어/라틴 시작이면 LTR. 방향 판정은 **불릿에서만**.
- 불릿 이어지는/안쪽 줄: `lineDir` — **로마자(음가) 유무**로 판정.
  - **로마자 있으면 → LTR**: 음가/설명 줄. 예 `دَرَسَ., darasa. 그가 공부했다 (남)` → 좌→우 자연 배치.
  - **로마자 없으면 → 첫 강한문자**: 아랍어 시작이면 RTL. 예 `عِنْدِي — 나에게` → 아랍어 오른쪽(점 옆) 먼저, 짧은 한국어 뜻 왼쪽.
  - (이전엔 "한글 유무"로 판정했으나 A09 `عِنْدِي — 나에게`가 한글 때문에 LTR로 깔려 아랍어가 왼쪽으로 가던 문제 → "로마자 유무"가 A04(음가 설명)·A09(아랍어 뜻풀이)를 모두 일관 처리)
- text-align은 불릿 방향(첫 줄 firstStrongDir)에 맞춤.
- 인라인 강조(`.hl-bold`/`.hl-box`)의 `unicode-bidi: isolate`는 **제거** — `دَرَ*سَ*`처럼 단어 중간 강조 시 아랍어 글자를 쪼갬. 강조는 bidi 투명, 방향은 컨테이너 dir로만 제어.
- `.app.meaning-hidden .summary-always { display:block !important }`가 불릿 flex를 덮어써 점이 본문 위로 튀던 버그(=빈칸 불릿) → `.summary-bullet.summary-always { display:flex !important }`로 우선 복원.

**다중 줄 불릿 (아랍어 + 한국어 번역 묶음)**:
- 스크립트에서 `- ` 불릿 다음 줄이 **빈 줄 없이** 이어지면 그 줄은 같은 불릿에 부착된다 (한국어 번역 등). 빈 줄(엔터)이 나오면 불릿 종료 → 이후는 산문.
- 불릿 전체 방향은 첫 줄 기준 (아랍어면 RTL, 점 오른쪽).
- 이어지는 각 줄은 **자체 방향(`firstStrongDir`)으로 `dir`** 부여 (한국어 줄은 내부 LTR이라 마침표 정상) + 불릿 방향에 맞춰 `text-align`(아랍어 불릿이면 우측)으로 정렬 → 아랍어 밑에 한국어가 우측 정렬로 붙어 한 블록처럼 보임.

```
script 예:
- شَرِبْتُ الْقَهْوَة فِي الْمَكْتَب صَبَاحًا
저는 사무실에서 커피를 마셨어요, 아침에.
            ← 빈 줄: 다음은 산문/새 불릿
```

**적용 범위**: 1.4.3 복습앱 `archive/app143s.html` 의 `renderSummaryDesc`. 다른 앱의 산문/불릿 렌더에도 동일 패턴 권장.

### 8.4 `css = 'five'` (5열 모드 — 드릴·레퍼토리)

좁은 5열 셀 레이아웃. 모바일에서는 4열로 자동 전환.

```css
.drill-five .cell { padding: 6px 2px; gap: 4px; }
@media (max-width: 480px) {
  .drill-grid { grid-template-columns: repeat(4, 1fr); }
}
```

라흐자 국기 표시 시 `.css-five .ar-line .lahja-flag { width: 10px; height: 10px }`로 축소.

> **선생님앱은 `five` 무시** — 슬라이드 한 장에 한 행씩 표시하는 형식이라 표·격자 모드는 의미 없음. 한 행씩 일반 슬라이드(아랍어 + 한국어 + 음가)로 떨어진다. `two`, `ab`, `c` 등 다른 css 값도 동일하게 무시 (선생님앱 분기는 `baseline` / `write`만).

### 8.5 라흐자(방언) 국기

매핑 (PNG 사용 — SVG는 외부 `<image>` 참조 시 `<img>` 태그에서 차단됨):

```javascript
const LAHJA_FLAG = {
  EGY: 'assets/icons/icon-egypt.png',
  EGP: 'assets/icons/icon-egypt.png',
  LEV: 'assets/icons/icon-lebanon.png',
  GLF: 'assets/icons/icon-saudi.png',
};
```

**CSS 표준 (전체 산출물 공통)**:

```css
.lahja-flag {
  width: 12px; height: 12px;       /* 모바일 기본. 인쇄 교재는 14px */
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  display: inline-block;
  vertical-align: middle;
  margin-inline-end: 4px;           /* 아랍어와 살짝 띄움 */
  background: rgba(18,32,90,0.06);
}
.lahja-flag img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
}
.lahja-flags {                      /* 다중 라하 컨테이너 */
  display: inline-flex;
  gap: 3px;
  align-items: center;
  vertical-align: middle;
  margin-inline-end: 4px;
}
.lahja-flags .lahja-flag { margin-inline-end: 0; }
.css-five .lahja-flag { width: 9px; height: 9px; }    /* 5열 셀에서 더 작게 */
```

**위치 규칙 (배치)**:

| 카드 타입 | 배치 |
|---|---|
| **표현·패턴 카드** | 아랍어 텍스트의 **앞**에 인라인으로 삽입 (`.m-ar` 안에 `${flag}${아랍어}`). 12px 원형 |
| **레퍼토리·드릴 그리드 셀** | 셀 안 인라인. `css=five` 모드면 9px |
| **나스 카드** | 한국어 칸 **하단** (`.m-pair-left .lahja-flag { margin-top: 6px }`). 인라인이면 두 줄 짜리 지문에서 화자 분리 오해 위험 |

**구현 원칙**: 별도 wrapper(`<div class="m-ar-line">`)를 만들지 말고 `.m-ar` 안에 직접 인라인 삽입. 플렉스 컨테이너 wrapper는 `.m-pair { align-items: baseline }` 정렬을 깨뜨림.

**금지 패턴** (이전 시도에서 폐기):
- ❌ `.m-card .m-flag { position: absolute; top: 10px; right: 10px; width: 18px; height: 18px }` — 절대 배치는 카드 내용과 겹치고 교재와 다름
- ❌ `.m-flag` / `.m-flags` 자체 클래스명 — 교재의 `.lahja-flag` / `.lahja-flags`로 통일
- ❌ `.m-ar-line { display: flex }` 별도 wrapper — 베이스라인 정렬 깨짐

### 8.6 Book View 모드 (선생님용 전용 — `B` 키)

`body.book-view` 클래스 토글로 슬라이드 UI 숨기고 B5 비율 페이지 카드 렌더링. PDF 출력 미리보기.

```css
body.book-view #main,
body.book-view #sidebar,
body.book-view #toolbar { display: none !important; }
body.book-view #book-root { display: flex; flex-direction: column; align-items: center; }
.book-page {
  width: min(92vw, 860px);
  aspect-ratio: 176 / 250;
  min-height: 1220px;
  background: var(--surface);
  box-shadow: 0 22px 70px rgba(18,32,90,0.16);
}
```

---

## 변경 이력

- **2026-05-10**: 초기 통합 — `product-ata144-design(mobile).md` 폐기 후 본 문서로 통합. 8개 섹션 구조로 재편 (기본값 / 타이포 / 4개 산출물 / 비교 / 커스텀 CSS).
- 컬러 표준 변경: `--text` 네이비 `#12205A` → 부드러운 검정 `#1a1f29`
- 배경 표준 정리: `--bg: #F2F4F6` (쿨그레이) — 모바일 앱의 녹색 끼 `#F3F5F1` 폐기
- 아랍어 weight 규칙 통일: 헤드라인 700 / 본문성 500. 600 사용 금지
- 한국어 본문 weight 400 고정. 카드 타입별 override 금지
- 좌우 페어 카드 정렬 표준: `align-items: baseline` (start/center 금지)
- 나스 아랍어 line-height: `2` → `1.75`
- 라하 국기 표준 통일: `.lahja-flag` 14px 원형 인라인 (교재 기준). 자체 `.m-flag` 클래스/절대배치 패턴 폐기. PNG 사용 (SVG의 nested `<image>` 차단 이슈)

- **2026-05-12**: 선생님앱 옵션 C 적용 (baseline·일반 아랍어 격차 좁힘) + UI 다듬기
  - 선생님앱 폰트 옵션 C: `.arabic` `9vw/9rem` → `10vw/9rem`, sentence `6vw/6rem` → `8vw/8rem`, `.korean` `3.5vw/3.5rem` → `4vw/4rem`, `.note` `2.2vw/2.2rem` → `2.6vw/2.5rem`
  - **baseline 3행 표 신규**: `.bl-letter`는 일반 `.arabic`과 동일 크기 `10vw/9rem`, `.bl-triple`(연결형) 신규 `4vw/3.5rem`, `.bl-label`은 일반 `.note`와 동일 크기 (이전 `1.4vw/1.15rem`에서 대폭 키움)
  - 섹션 탭: `Drill A` 별도 탭 신설 (이전엔 패턴 하위로 동작), 패턴 탭 라벨 한국어 이름 → 패턴 번호(`ptn001`) 형식, SEC_FIXED 6개로 확장
  - 드릴 슬라이드 순서 재편: 패턴+예문 묶음 → 모든 drillA → drillB/C → exp → nass → kalimat
  - `TYPE_KO.repertory`: '레퍼토리' → **'예문'**
  - 좌상단 `#ui-tl`: 유닛코드/아랍어/한국어 3행 줄간격 확대 (margin-bottom 0.2→0.5rem, line-height 1.3→1.4/1.5)
  - 도구바: `T 지문` 버튼 제거 (T 키바인딩은 유지), `Space 해석` → `Space 한국어 가리기` 라벨 변경
  - 오디오 신구조: `listening144/{id}.mp3` 폐기 → `audio/{유닛코드}/{id}.{mp3|wav}`, mp3 우선 → wav 폴백
  - 드릴B `*X*` 가리기: 선생님앱(슬라이드 형식)에서 `color: transparent` + `-webkit-text-fill-color: transparent` + 박스 alpha 0.14 (기존 0.08 대비 진하기 강화 — 글자 윤곽이 비치던 문제 해결)
  - `css` 코드 처리: 선생님앱은 `baseline`/`write`만 분기, `five`/`two`/`ab`/`c` 등은 무시 (일반 슬라이드로)

- **2026-05-13**: 새 `css` 값 정의 — `nom` (명사문 — 주어 ‖ 서술어 구분)
  - 8.3.7 절 신규 — 데이터 형식(`|`로 두 구분), `.nom-divider` CSS, `applyNomDivider` 헬퍼 패턴
  - 1.4.3에서 먼저 정의, 1.4.4에 동일 적용 (모든 산출물 — 교재 인쇄·교재앱·학생앱·선생님앱)
  - 선생님앱 추가 fix: 라하 깃발을 ui-tr에서 메인 콘텐츠 음가 밑으로 옮김(멀티 라하 지원), `getRowId`에 `id_rep` 추가(예문 오디오 살림), 나스 한국어/음가 사이즈 키움(`.nass-korean-hint` 0.65~0.9rem → 0.9~1.6rem, `.nass-note` 0.65~0.82rem → 0.85~1.4rem)

- **2026-05-13 (추가)**: 새 `css` 값 정의 — `baseline2` (기준선 없는 baseline)
  - 8.2.5 절 신규 — baseline과 동일 구조 (3행 표), 가로선만 숨김. `.bl-wrap.no-line .bl-line { display: none }` 또는 line div 자체 생성 안 함
  - 1.4.3 / 1.4.4 양쪽에 적용 — 모든 산출물 (교재 인쇄·교재앱·학생앱·선생님앱)
  - 사용 케이스: 후반 챕터, 모음/하라카 조합 표 등 baseline 정렬 강조가 불필요한 페이지
