# 올댓아라빅 1.4.4 — 디자인 코드

올댓아라빅 1.4.4의 디자인 시스템을 단일 출처로 관리한다. 4가지 산출물(**교재 / 교재앱 / 사용자앱 / 선생님앱**)이 공통 토큰을 공유하면서 각자 목적에 맞는 시각 언어를 갖는다.

> 본 문서는 디자인 코드의 단일 출처(SSoT)다. `product-ata144.md`는 이론·데이터 구조·인프라만 다루며, 시각적·UI 규칙은 모두 여기에 통합되어 있다.

---

## 공통 디자인 토큰

> **컬러 톤 정책**: 본문/보조/구분선은 **부드러운 검은색 계열(soft black / neutral gray)** 을 사용한다. 차가운 네이비(#12205A 등)는 사용하지 않으며, **파란색은 액센트(`--accent`, `--hl-text`)에만** 한정한다.

```css
:root {
  --bg:        #F3F5F1;   /* 페이지 배경 — 중립/약간 따뜻한 light gray */
  --surface:   #FFFFFF;   /* 카드/패널 배경 */
  --accent:    #1D49FF;   /* 포인트 컬러 (파랑, 브랜드) */
  --accent-bg: rgba(29,73,255,0.08);  /* 액센트 옅은 배경 (하이라이트 박스, 활성 탭) */
  --text:      #1a1f29;   /* 본문 — soft black charcoal */
  --sub:       #6E7591;   /* 보조 — 중립 gray (음가, 인덱스, 비활성) */
  --border:    #DDE2EE;   /* 구분선 / 카드 테두리 — 매우 옅은 light gray */
  --hl-text:   #3554C6;   /* `*…*` 색 강조 — 액센트 계열, 파랑 유지 */
  --gray-pill: #C7CDD9;   /* 헤더 우측 박스 등 회색 알약 (교재 전용) */
}
```

> **앱 정합성 추적**: `ata144_textbook.html`(교재앱)에 본 팔레트 적용 완료. `ata144_student.html`·`ata144_teacher.html`는 아직 옛 네이비 토큰(`--text: #12205A`, `--sub: #888FAC`, `--border: #D5DAE8`)을 사용 — 별도 작업으로 본 팔레트로 통일 필요.

> **명명 통일 작업 진행 중**: 일부 코드(teacher.html)에서 `--accent-soft`라는 동일 의미 변수를 사용한다. 향후 `--accent-bg`로 통일 예정.

### 공통 폰트

| 용도 | 폰트 | weight |
|---|---|---|
| 한국어 UI | Spoqa Han Sans Neo, Apple SD Gothic Neo, sans-serif | 400~700 |
| 아랍어 본문 | Noto Sans Arabic, serif | 500/700 |
| 아랍어 쿠픽 (선생님앱 일부) | Noto Kufi Arabic | 400 |
| 쓰기 애니메이션 (선생님앱 write 모드) | Dongol (`../assets/fonts/Dongol-Regular.otf`) | 400 |

### 하이라이트 마크업 공통 규칙

시트 `arabic`/`korean`/`note`/`script` 컬럼에서 사용 가능한 인라인 마크업.

| 마크업 | 본문(패턴/한국어/스크립트) | 셀(레퍼토리/드릴/음가) |
|---|---|---|
| `_..._` (박스 강조) | `<span class="hl-box-inline">` 박스 | **제거** (다이아크리틱 클립 회피) |
| `*...*` (색 강조) | `<span class="hl-text">` 색 강조 | `<span class="hl-text">` 색 강조 (유지) |
| `\n` (줄바꿈) | `<br>`로 변환 | (셀에는 거의 등장 안 함) |

⚠️ **Arabic shaping 주의**: `.hl-text`에 부모와 다른 `font-weight`를 지정하면 Safari/CoreText에서 weight 경계로 텍스트 런이 분리되어 **글자 연결이 끊긴다**. 따라서:

| 컨텍스트 | weight 처리 |
|---|---|
| 아랍어 (`.ar-text`, `.pattern-arabic`, `.drill-arabic`, `.nass-arabic`, `.exp-arabic`) | **부모 weight 상속** (지정 안 함). 색만 다르게 (`var(--hl-text)`) |
| 라틴 음가 (`.trans`, `.drill-trans`, `.exp-trans`, `.nass-trans`, `.pattern-trans`) | **font-weight: 700** + 색. Latin은 셰이핑 없음 |
| 한국어 (`.pattern-korean` 등) | **font-weight: 700** + 색 |

> **앱별 클래스명 차이** (통일 필요): 사용자앱은 `.hl-bold` + `.hl-box`, 교재/교재앱은 `.hl-text` + `.hl-box-inline`, 선생님앱은 `.hl-text` + `.hl-box`. 향후 `.hl-text`/`.hl-box-inline`으로 통일 예정.

### 라하(방언) 깃발 공통 매핑

```js
const LAHJA_FLAG = {
  EGY: '../assets/icons/icon-egypt.png',
  EGP: '../assets/icons/icon-egypt.png',
  LEV: '../assets/icons/icon-lebanon.png',
  GLF: '../assets/icons/icon-saudi.png',
};
// MSA 등 매핑 없는 값은 미표시
```

`lahja` 컬럼에 `GLF, LEV` 또는 `GLF LEV`처럼 콤마/공백으로 두 개 이상 입력하면 모두 표시. 원형(`border-radius: 50%`).

> ⚠️ **PNG 사용 강제**: `assets/icons/icon-*.svg`는 외부 파일(`source-flags/flag-*.svg`)을 wrapper SVG의 `<image href>`로 참조하는 구조. `<img>` 태그로 SVG를 로드할 때 브라우저는 보안 정책상 SVG 내부의 외부 리소스 참조를 차단해 빈 원형만 그려진다. PNG는 자체 완결 비트맵이라 이 제약 없음. SVG로 다시 가려면 wrapper에 외부 SVG를 inline하거나 `<object data="...">`/`<embed>`로 로드해야 한다.

---

## 교재 인쇄 원본 (ata144_original)

**구현 파일**: `ata144_original/ata144_original.html`

**목적**: B5 인쇄용 교재 원본. 데스크톱 미리보기 = 인쇄물 1:1 매칭. PDF 생성용. 모바일 미디어쿼리는 fallback 수준.

### 페이지 사이즈
- B5 (182mm × 257mm)
- CSS: `width: 182mm; height: 257mm` — 미리보기 = 인쇄 1:1
- 표현/드릴/나쓰 페이지: 콘텐츠 양에 따라 세로로 늘어남 (`min-height: 257mm; overflow: visible`)
- 패턴 페이지: 고정 B5

### 디자인 토큰 (교재 전용)
공통 토큰 + 다음:
```css
--textbook-card-ar-size: 1.18rem    /* 표현·나쓰·디폴트 드릴 카드 아랍어 공통 크기 */
--textbook-card-trans-size: 0.74rem /* 음가 공통 크기 */
```

회색 영역(헤더·푸터)과 흰색 카드(본문/래퍼토리/표현/드릴/나쓰) 교대 구성으로 시각적 리듬.

기본 카드형 콘텐츠(`.exp-arabic`, `.nass-arabic`, `.drill-arabic`)와 음가 라인은 위 두 토큰으로 통일. `css = 'five'`는 좁은 5열 셀을 위한 별도 예외값.

### 폰트 weight 규칙

**아랍어**

| 요소 | 셀렉터 | weight |
|---|---|---|
| 패턴 메인 데이터 | `.pattern-arabic` | **700** |
| 패턴 알파벳 큰 글자 | `.pattern-arabic.baseline .blch .l` | **700** |
| 패턴 알파벳 연결형 | `.pattern-arabic.baseline .blch .l-triple` | **500** |
| 표현 카드 | `.exp-arabic` | **500** |
| 나쓰 카드 | `.nass-arabic` | **500** |
| 드릴 카드 (non-five) | `.drill-arabic` | **500** |
| 드릴 5열 셀 | `.drill-five td.ar` | **500** |
| 래퍼토리 셀 | `.repertory td.ar` | **500** |
| 패턴 스크립트 인라인 토큰 | `.pattern-script .ar-tok` | **600** |

**원칙**
- 패턴(학습 대상 데이터)은 700으로 가장 강조
- 그 외 본문/예문/드릴/나쓰는 500
- 스크립트 안 인라인 아랍어 토큰만 600 — 한국어 본문 사이에서 가독성 보장

**한국어 / 음가**
- 음가(trans 류) 본문: **400** italic
- 한국어 본문(`.exp-korean`, 카드 한국어 등): **500**
- 한국어 강조(`.pattern-korean` 패턴 한국어): **600**

### 유닛 페이지 구성

| 순서 | 페이지 종류 | 분량 |
|---|---|---|
| 1 | 표현 (EXPRESSION) | 1장 |
| 2~ | 패턴 (PATTERN 001, 002, …) | 패턴 수만큼 |
| 마지막-1 | 드릴 (DrillA + DrillB) | 1장 (분량 따라 자동 분할) |
| 마지막 | 나쓰 (nass + nass+) | 1장 |

예: A01 (패턴 3개) → **6 페이지**. 페이지 번호는 유닛 안에서 01부터 시작.

### 모든 페이지 공통

**헤더 (회색 영역, 위→아래)**
1. **카테고리 라벨** — `올댓아라빅 표현/패턴/드릴/지문` (작은 회색 텍스트)
2. **분할 박스** — 좌(파랑): UNIT + 유닛번호 / 우(회색 알약): 페이지 종류
   - 패턴 페이지: `PATTERN 001` (3자리, `id_ptn(no)`에서 추출)
   - 표현/드릴/나쓰: 단어만 (숫자 없음)
3. (드릴/나쓰만) **안내문** — 박스 아래 18px 여백 후 콘텐츠 시작

**푸터 (회색 영역, 좌우 분할)**
- 좌: `assets/ata-logo2.png` + **MARKAZARABIC** + © 2026
- 우: `| NN` 페이지 번호 (유닛 내부 인덱스)

### 페이지 종류별 상세

#### 표현 페이지

**구성**: 헤더 → (그림 있으면 16:9 일러스트) → 표현 카드 N개 → 푸터.

표현 카드 (흰색 박스, 카드당 1 표현):
- **2열 그리드: 좌측 한국어 (LTR) / 우측 아랍어+음가 (RTL)**
- 우측: 큰 아랍어 → 작은 회색 italic 음가
- 좌측: 한국어 (아랍어보다 작게)
- `expression.script` 있으면 카드 하단에 가로 구분선 + 좌측 정렬 추가
- 라하 깃발: 우측 아랍어 옆 인라인 14×14

#### 패턴 페이지 (한 패턴 = 한 페이지)

**구성**: 헤더 → (첫 패턴이면 16:9 일러스트) → 본문 카드 → 래퍼토리 카드 → 푸터.

**본문 카드** (흰색 박스):
- 일반 패턴: 큰 아랍어 (RTL) → 음가 (챕터 0 한정) → 한국어 (가운데) → 스크립트 (좌측)
- baseline 패턴 (`pattern.css = 'baseline'`): 아래 baseline CSS 섹션 참고
- 스크립트 시맨틱 마크업: 단락은 `<p>`, 불릿(`-`)은 `<ul><li>`, 인라인 아랍어 토큰은 `.ar-tok` (폰트/방향 자동 처리)

**래퍼토리 카드** (본문과 가로 폭 동일):
- 표 자체 `direction: rtl` — 첫 DOM 셀이 시각적으로 가장 오른쪽
- 모드 결정 (우선순위):
  - 항목 중 하나라도 `repertory.css = 'two'` → **2열 박스 모드** (드릴 `css = 'two'`와 동일 — 박스 좌→우 2개씩, 박스 안 아랍어 RTL + 음가 + 한국어 LTR + 깃발)
  - 그 다음 `repertory.css = 'five'` → **5열 아랍어 모드** (한국어 무시, 챕터 0이면 음가 작게)
  - 한국어 모두 빔 → 5열 모드 (fallback)
  - 그 외 → **2 페어 모드** (DOM: ar–ko–ar–ko, 시각: [한국어 아랍어][한국어 아랍어] 우→좌)
- 라하 깃발: 아랍어 옆 인라인 14×14 (5열은 10×10, 2열은 14×14)

#### 드릴 페이지

**구성**: 헤더 → DrillA 안내문 + 표 → DrillB 안내문 + 표 → 푸터. 위→아래 스택.

**css = 'five'** (5열 모드):
1. 안내문: `다음을 듣고 따라 읽어 보세요`
2. **DrillA 5열 표** — drillA 항목들 한 줄 5개씩
3. 안내문: `다음을 듣고 빈 칸에 들어갈 말을 유추해 보세요` (챕터 0은 `글자` override)
4. **DrillB 5열 표** — drillB 항목들. `*X*` 마스크 처리는 아래 참고

**css = 'two'** (2열 박스 모드) — 5열은 좁고 디폴트 카드는 너무 큰 항목을 위한 중간 밀도:
1. 박스(흰 카드) 형태가 **좌→우 한 행에 2개씩** 정렬 (LTR 배치)
2. 각 박스 안 (위→아래 스택):
   - 아랍어 라인 (RTL, 우측 정렬) + 깃발 인라인
   - 음가 (RTL, italic, 우측 정렬)
   - 점선 구분선 + 한국어 (LTR, 좌측 정렬, sub 톤)
3. 박스 사이즈: 디폴트 카드보다 좁음 (한 행 폭의 절반)
4. 깃발 표시 ✓ (5열은 미표시지만 2열은 폭 충분)
5. 우선순위: `two` > `five` > 디폴트 — 한 그룹 안에 `two` 행이 하나라도 있으면 그 그룹 전체가 2열로

**css 비어있음 (디폴트)** — 항목별 카드 (한 드릴 = 한 박스):
1. 각 드릴 항목이 자기 흰 카드(`.drill-row`)를 가짐
2. 카드 안 2열: 좌 한국어 (LTR, 보조 톤) / 우 아랍어+음가 (RTL, 학습 대상)
3. 수직 정렬: top-align (`align-items: start`) — 한국어가 길어 줄 넘어가도 윗부분 라인 일치
4. ref_ptn 그룹 내 카드 사이: **12px** (`.drill-row-gap`)
5. 그룹 사이: **14px** (`.drill-box-gap`)
6. 카드 외곽: 둥근 모서리 + `1px solid rgba(18,32,90,0.06)` + 옅은 그림자 `0 1px 2px rgba(18,32,90,0.04)`, padding `12px 18px`
7. 한국어 폰트: 0.82rem, color `var(--sub)`, line-height 1.5
8. 아랍어 1.08rem weight 500 / 음가 0.68rem italic
9. 페이지네이션 atom = ref_ptn 그룹 (그룹 중간 자르지 않음)

**드릴 그룹핑 (ref_ptn)**
- 디폴트: ref_ptn 비어있으면 유닛 전체를 한 박스
- 패턴별 분리: ref_ptn 값 있으면 패턴 단위로 별도 표 생성, 위→아래 쌓음. 빈 ref_ptn 그룹은 가장 마지막
- 같은 type 박스끼리는 14px 간격(`.drill-box-gap`)
- `ref_unit` = 유닛 매칭 키(필수, 자동), `ref_ptn` = 옵션. 두 컬럼은 독립적

**드릴 페이지 자동 분할** (`renderDrillPagesAsync`)
- 박스(=ref_ptn 그룹) 1개가 atomic 단위. 박스 중간 절대 자르지 않음
- off-screen 측정으로 박스 높이 측정 → B5 budget 안에서 빈 패킹
- 안 들어가는 박스는 다음 `.page page-drill`로 밀어 새 페이지
- 같은 섹션 박스끼리 14px gap, DrillA→DrillB 섹션 전환은 36px gap
- 단일 박스가 페이지 가용 높이를 단독 초과: 콘솔 경고 + 단독 페이지. 시트에서 ref_ptn 더 잘게 쪼개거나 행 수 줄여 해결
- 페이지 번호: 드릴이 N페이지로 늘어나면 후속 페이지(나쓰 등) 번호가 자동으로 N-1만큼 밀림
- **측정 안정성**:
  - ① 측정 전 `document.fonts.ready` 대기 — 폰트 로딩 전 측정 시 fallback 메트릭으로 잘못 계산
  - ② `PAGE_BUDGET = 740px` (측정값이 아닌 B5 고정 기하 하드코딩) — 측정 컨테이너 flex 레이아웃이 브라우저별로 다르게 계산되는 이슈 회피 (Chrome ↔ Safari)

**DrillB 빈칸 처리**
```css
.drill-blank {
  color: rgba(18,32,90,0.08);
  background-color: rgba(18,32,90,0.08);
  display: inline; /* ⚠️ inline-block 금지 — 새 formatting context 생성으로 셰이핑 끊김 */
  padding: 0 3px;
}
.trans .drill-blank,
.drill-trans .drill-blank { background-color: rgba(18,32,90,0.06); }
```
- `*X*` → 글자를 보존 + 색만 배경과 동일하게 숨김 (학생이 빈칸 위에 답 쓸 수 있음)
- 채점/해답지: `.drill-blank { color: var(--text) }` 한 줄로 정답 노출
- tatweel 임의 삽입 로직 없음

**안내문 양식**
- `.drill-instruction` / `.nass-instruction` (가운데, 본문 색, 0.86rem 정도)
- 첫 등장의 첫 박스 위에만 1회 (atomic — 첫 박스가 다음 페이지로 밀리면 안내문도 같이)
- 같은 섹션 후속 박스/페이지에는 안내문 없음
- `.drill-instruction { margin-bottom: 28px }`. 부모 `.drill-section { gap: 0 }`로 둬서 모든 자식 간 간격은 명시 div(`.drill-row-gap`, `.drill-box-gap`) 또는 margin으로만 제어 (flex gap 자동 누적 버그 방지)

**안내문 멘트 일람**

디폴트 (모든 챕터 공통):

| 페이지 | 섹션 | 멘트 |
|---|---|---|
| 드릴 | DrillA | `다음을 듣고 따라 읽어 보세요` |
| 드릴 | DrillB | `다음을 듣고 빈 칸에 들어갈 말을 유추해 보세요` |
| 나쓰 | type=`nass` | `다음을 들으면서 소리로 의미를 이해하고 같이 따라 읽어 보세요` |
| 나쓰 | type=`nass+` | `다음을 듣고 다음에 나올 말이 무엇인지 유추해 보세요` |

챕터 0 override (유닛 A01~A06):
- DrillB: `다음을 듣고 빈 칸에 들어갈 **글자**를 유추해 보세요` (`말` → `글자`)

#### 나쓰(지문) 페이지

**구성**: 헤더 → (nass 안내문 + 카드들) → (nass+ 안내문 + 카드들) → 푸터. 위→아래 스택.

나쓰 카드:
- **2열 그리드: 좌측 한국어 (LTR) / 우측 아랍어+음가 (RTL)**
- 글자 크기 표현 카드보다 살짝 작게, line-height 여유 (대화 2~3줄 들어가도 답답하지 않게)
- 데이터의 `\n` 줄바꿈 → `<br>`로 자동 변환 (화자 분리)
- 라하 깃발: **좌측 한국어 칸 하단** 14×14 (특정 줄에 매여 보이지 않도록 카드 메타로 분리)

### 일러스트 (GCS 호스팅)

**노출 위치 (임시 규칙)**

- **표현 페이지**: 헤더 바로 아래, 첫 표현 카드 위
- **첫 패턴 페이지**: 헤더 아래, 본문 카드 위 (한 유닛에서 가장 첫 패턴 페이지에만)
- 두 위치 모두 16:9 비율, 박스/라운드 없는 직사각형, 회색 페이지 배경 위
- 다른 페이지(드릴, 나쓰)에는 일러스트 없음

**파일명 컨벤션**

| 위치 | 파일명 패턴 | 예 |
|---|---|---|
| 표현 페이지 | `img/{유닛U}_exp1.png` | `A01_exp1.png` |
| 첫 패턴 페이지 | `img/{유닛U}_ptn1.png` | `A01_ptn1.png` |

URL: `https://storage.googleapis.com/all-that-arabic-14/img/{파일명}`

- 시트의 `img` 컬럼 사용 안 함 — 유닛 U값에서 자동 생성
- 접미사 `_exp1` / `_ptn1`의 `1`은 추후 베리에이션을 위한 자리 (현재 1번만 사용)
- 없을 때(404): `<img onerror>`로 영역을 DOM에서 제거 — placeholder 없음
- GCS 공개 읽기 권한 필요
- 캐시 무력화: `<img src="…?v=Date.now()">` (초안 단계)

### 페이지별 깃발 위치 통합 표

| 페이지 | 위치 | 크기 |
|---|---|---|
| 표현 카드 | 우측 아랍어 옆 인라인 | 14×14 |
| 래퍼토리 페어 | 셀 내 아랍어 옆 인라인 | 14×14 |
| 드릴 카드 (non-five) | 아랍어 옆 인라인 | 14×14 |
| 드릴/래퍼토리 5열 (`.css-five`) | 아랍어 옆 인라인 | **10×10** |
| 나쓰 카드 | 좌측 한국어 칸 하단 | 14×14 |

**5열 모드 공통 CSS**
```css
.css-five .ar-line { gap: 4px; }
.css-five .ar-line .lahja-flag { width: 10px; height: 10px; }
.css-five .ar-line .lahja-flags { gap: 2px; }
```

**5열 박스/셀 사이즈 통일** — 드릴 5열과 래퍼토리 5열의 시각 일치:

| 항목 | 값 |
|---|---|
| 외곽 박스 패딩 | `14px 16px` |
| 셀 패딩 | `7px 6px` |
| 셀 폰트 크기 | `1.08rem` |
| 셀 폰트 weight | `500` |
| 트랜스 폰트 크기 | `0.68rem` |
| 트랜스 margin-top | `1px` |
| 트랜스 letter-spacing | `0.2px` |

### 챕터 0 (음가 노출 기준)
- `u`가 `A`로 시작하는 유닛 → 챕터 0(알파벳 입문). 음가(`note`/`transliteration` 컬럼) 자동 노출
- URL 파라미터로 강제: `?trans=1` 노출, `?trans=0` 숨김
- 다른 시리즈(추후 G/B 등)에는 음가 자동 노출 안 함

### baseline (알파벳 그룹) CSS 코드

알파벳 그룹 페이지(A01-A05의 ptn001 등). **6칸 고정 그리드** + 유닛별 글자 크기 일관 + 토큰이 6 미만이면 가운데 정렬.

데이터 형식 (`pattern.arabic`):
- 1줄: 단일 글자 (`|`로 구분) — 예: `ب | ت | ث | ن | ي`
- 2줄: 위치별 연결형 — 예: `ببب | تتت | ثثث | ننن | ييي`

`note` 컬럼 = 음가 라벨 (공백 구분).

```html
<div class="pattern-arabic baseline has-triple">
  <div class="bl-line"></div>
  <span class="blch">
    <span class="l">ب</span>          <!-- 1행: 단일 글자 -->
    <span class="l-triple">ببب</span>  <!-- 2행: 연결형 -->
    <span class="lbl">bā</span>       <!-- 3행: 음가 -->
  </span>
  ...
</div>
```

```css
.pattern-arabic.baseline {
  position: relative; display: flex;
  direction: rtl; justify-content: center;
  flex-wrap: nowrap; width: 100%;
  padding: 22px 0 18px;
}
.pattern-arabic.baseline .bl-line {
  position: absolute; left: 4%; right: 4%;
  height: 1.5px; background: rgba(29,73,255,0.3);
  pointer-events: none; z-index: 0;
}
.pattern-arabic.baseline .blch {
  flex: 0 0 calc(100% / 6);  /* 1/6 셀 폭 */
  display: flex; flex-direction: column;
  align-items: center; gap: 14px;
  z-index: 1;
}
.pattern-arabic.baseline .blch .l {
  font-family: var(--font-ar); font-weight: 700;
  font-size: 2.1rem; line-height: 1;
}
.pattern-arabic.baseline .blch .l-triple {
  font-family: var(--font-ar); font-weight: 600;
  font-size: 0.95rem; line-height: 1.2;
  white-space: nowrap; text-align: center;
}
.pattern-arabic.baseline .blch .lbl {
  font-family: var(--font-kr);
  font-size: 0.72rem; font-weight: 400;
  color: var(--sub); direction: ltr;
}
```

토큰 분리 로직 (`renderBaseline`):
```js
const splitTokens = (line) => {
  const sep = line.includes('|') ? /\s*\|\s*/ : /\s+/;
  return line.split(sep).map(t => t.trim()).filter(Boolean);
};
```

기준선(`bl-line`) 위치는 폰트 로드 후 첫 글자(`.l`)의 baseline을 JS probe로 측정해 `top` 동적 설정 (`adjustBaselines()`).

### c (가운데 정렬) CSS 코드

`pattern.css = 'c'` 으로 지정한 패턴은 **baseline과 동일한 6칸 그리드 구조**를 쓰지만 다음이 다르다:
- **기준선(.bl-line) 없음** — `<div class="bl-line">` DOM 미생성
- **음가 라벨(.lbl) 표시 안 함** — `note` 컬럼이 있어도 출력하지 않음
- **수직 가운데 정렬** — baseline이 글자 밑선을 기준으로 정렬하는 반면, `c`는 셀 내 콘텐츠를 vertical center에 배치 (글자 크기가 다른 토큰들도 시각적 가운데 라인에 모임)

`pattern.arabic` 데이터 형식은 baseline과 동일 (1줄 또는 2줄, `|` 구분자 지원).

```html
<div class="pattern-arabic c">
  <span class="blch"><span class="l">…</span></span>
  ...
</div>
<!-- 2줄(has-triple) 케이스: -->
<div class="pattern-arabic c has-triple">
  <span class="blch">
    <span class="l">…</span>
    <span class="l-triple">…</span>
  </span>
  ...
</div>
```

```css
.pattern-arabic.c {
  position: relative; display: flex;
  direction: rtl;
  justify-content: center; align-items: center;  /* 수직·수평 가운데 */
  flex-wrap: nowrap; width: 100%;
  padding: 22px 0 18px;
}
.pattern-arabic.c .blch {
  flex: 0 0 calc(100% / 6);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 8px;
}
/* .l, .l-triple 폰트 사이즈는 baseline과 동일. .lbl 규칙 없음 (DOM 미생성). */
```

**구현 위치 (인쇄 교재)**: `renderC(arabic)` 함수 + `renderPatternPage()`에서 `cssMode === 'c'` 분기.

### 인쇄 스타일

```css
@media print {
  /* 배경 단순화, 그림자/라운드 제거 */
  /* 유닛 픽커 숨김 */
  /* 각 페이지마다 page-break-after: always */
}
```

### 알려진 이슈 / 추적

진행 중 발견된 시각·레이아웃 이슈. 본문 규칙으로 흡수되기 전까지 여기에 기록.

**라하 국기 위치 / 사이즈 시도 이력**

| # | 이슈 | 페이지 | 처리 |
|---|---|---|---|
| 1 | 5열 모드 셀에서 깃발-아랍어 충돌 / 좁은 셀 줄바꿈 | 드릴 + 래퍼토리 5열 | (최종) `.css-five` 마커 + 깃발 10×10 + `gap:4px`. 텍스트 폭 손실 ~12px |
| 2 | 나쓰 카드에서 깃발이 아랍어 옆 인라인이면 두 번째 줄(다른 화자)에만 방언 적용된 것처럼 보임 | 나쓰 | 깃발을 좌측 한국어 칸 **하단**으로 분리 (정착) |
| 3 | 다중 라하(`GLF, LEV`) 표시 시 깃발 두 개라 가로 폭 더 잡아먹음 | 표현·래퍼토리·드릴 | 16×16 → 14×14 + 깃발 사이 4px 간격 |

**드릴 페이지 분할 / 안내문 이슈 이력**

| # | 이슈 | 처리 |
|---|---|---|
| 4 | 드릴 박스 합이 B5 한 페이지 초과 시 잘림 | `renderDrillPagesAsync` 도입 — 박스 atomic + off-screen 측정 + 빈 패킹 |
| 4-1 | 페이지 분할 결과가 Chrome ↔ Safari 다름 | ① `document.fonts.ready` 대기 ② `PAGE_BUDGET = 740px` 하드코딩 |
| 4-2 | DrillA와 DrillB가 같은 페이지에 섞여 학습 흐름이 한 묶음으로 보임 | **조건부 분리** — 합쳐서 한 페이지(`PAGE_BUDGET`) 안에 들어가면 같이(예: 1과), 넘으면 A → B 전환 시 강제로 새 페이지(예: 2과). 빈 패킹 전 `combinedTotalHeight ≤ PAGE_BUDGET` 사전 계산해 `allFitsInOnePage` 플래그로 분기. 모바일 앱(`ata144_textbook`)은 스크롤 기반이라 overflow 개념이 없어 항상 한 페이지로 묶음 (단일 '드릴' 페이지) |
| 5 | 안내문이 박스 없이 페이지 끝에 외롭게 남거나 두 번 반복 | 첫 등장의 첫 박스에만 1회, atomic — 첫 박스 이동 시 함께 이동 |
| 5-1 | 안내문이 박스에 너무 붙어 박스 헤더처럼 읽힘 | `.drill-instruction { margin-bottom: 28px }` |
| 5-2 | 디폴트 드릴 카드 사이 간격이 의도(2px)보다 12px씩 부풀어 보임 — 부모 `gap: 12px` 자동 누적 | `.drill-section { gap: 0 }` + 명시 div(`.drill-row-gap`/`.drill-box-gap`)로만 제어 |
| 7 | 5열 모드 `*X*` 빈칸 처리 시 tatweel/`&nbsp;`로 셰이핑 끊김 | 글자 보존 + 색만 배경과 동일. `display: inline` 필수 |

**미해결 / 추적 중**

| # | 이슈 | 비고 |
|---|---|---|
| 8 | **유닛 2의 페이지 넘김이 데이터/렌더 로직에 암시적으로 묻혀 있음** — 어떤 박스가 왜 다음 페이지로 밀리는지 시트 행을 봐도 즉시 파악 불가. 명시적 표기 방식 필요(예: `pagebreak` 마커 컬럼 또는 ref_ptn 단위로 가시화) | 샘플링 단계라 우선 본 표에 기록. 추후 시트 컬럼 또는 css 코드로 명시 가능성 검토 |

**폰트 크기 통일**

| # | 이슈 | 처리 |
|---|---|---|
| 7 | 표현·나쓰·디폴트 드릴 카드 아랍어 크기가 서로 달라 위계 흔들림 | 공통 토큰 도입: `--textbook-card-ar-size: 1.18rem`, `--textbook-card-trans-size: 0.74rem` |

---

## 교재앱 (모바일 textbook)

**구현 파일**: `ata144_textbook/ata144_textbook.html`

**목적**: 모바일 기기에서 교재를 읽는 경험. 스크롤 기반.

> 데이터/렌더 로직은 교재(B5)의 페이지 단위 렌더 함수(`renderExpressionPage`, `renderPatternPage`, `renderDrillPage`, `renderNassPage`)를 모바일용으로 포팅한다. 카드 구조·깃발 규칙·하이라이트 등 시각 언어는 교재와 동일하게 유지하되, 페이지 셸(헤더·푸터)만 모바일용 미니 셸로 교체.

### 배경 / 옛 이름 매핑

본 앱은 1.4.3 학생앱과 별개로, 새로 만든 교재 양식을 모바일 인터랙티브 앱으로 옮길 수 있을지 실험하기 위해 시작됐다. 결과가 충분히 좋으면 학생앱(`ata144_student`)을 본 교재앱으로 통합/대체하는 검토가 진행된다 — 보류 시 사내 시연/검토용으로 유지하고 인쇄 교재는 정상 운영.

옛 실험 단계 파일명이 본 문서·기존 코드 주석에 남아 있을 수 있다. 매핑:

| 옛 이름 | 현재 경로 |
|---|---|
| `app144s.html` | `ata144_student/ata144_student.html` |
| `textbook144.html` (인쇄 교재) | `ata144_original/ata144_original.html` |
| `textbook144m.html` (모바일 실험) | `ata144_textbook/ata144_textbook.html` |

**학생앱과의 통합 검토 조건** (만족 시 `ata144_student` → 본 교재앱으로 통합):
1. 모든 페이지 종류(표현/패턴/드릴/지문)에서 인터랙션 자연스러움
2. 모바일 가독성이 학생앱보다 좋거나 동등
3. 오디오 재생 흐름이 슬라이드형(현재 학생앱)보다 직관적
4. 학습 보조 기능(진도/북마크) 구현 완료

### 디자인 토큰 (모바일 스케일, 1.4.4 최신)

공통 토큰 + 모바일 사이즈 토큰:
```css
--ar-card-size:    clamp(0.98rem, 4vw, 1.12rem);   /* 표현/나쓰/디폴트 드릴 카드 아랍어 */
--ar-nass-size:    clamp(0.84rem, 3.4vw, 0.95rem); /* 지문 — 표현보다 작게 */
--ar-pattern-size: clamp(1.2rem, 5.2vw, 1.55rem);  /* 패턴 본문 아랍어 (강조) */
--trans-size:      10px;   /* 음가 italic */
--ko-size:         11px;   /* 한국어 기본 (표현/나쓰) */
--script-size:     11px;   /* 스크립트/요약 — 한국어 보조 설명 */
--max-w:           640px;
```

660px 이상 태블릿/데스크톱 오버라이드:
```css
--ar-card-size: 1.3rem;
--ar-nass-size: 1.1rem;
--ar-pattern-size: 2rem;
--trans-size: .74rem;
--ko-size: .8rem;
```

660px 이상에서 카드형 레이아웃(상하 28px 여백, border-radius, box-shadow). 660px 미만은 풀스크린.

### 한국어 사이즈 위계

```
패턴 한국어 (.m-card.pattern .m-ko)         12px / weight 600  ← 가장 강조 (학습 대상 패턴 의미)
드릴/래퍼토리 페어 한국어 (.m-row-ko)         12px / weight 400  ← 카드 보조 (sub 톤)
표현/나쓰 카드 한국어 (.m-card .m-ko)         11px / weight 500 (나쓰는 400)  ← 본문
스크립트/요약 (.m-summary, .m-script)        11px / weight 400  ← 한국어 보조 설명 (본문과 동급, sub 톤으로 구분)
음가 (.m-trans)                              10px / weight 400 italic
```

> **원칙**: 같은 한국어 텍스트 안에서 _학습 대상 정보 > 본문 > 보조 설명_ 순으로 사이즈가 작아진다. 표현·나쓰의 한국어는 본문으로 11px이 적정선.

### 폰트 weight 규칙 (모바일)

| 요소 | 셀렉터 | size | weight |
|---|---|---|---|
| 패턴 본문 아랍어 | `.m-card.pattern .m-ar` | `--ar-pattern-size` | **600** |
| baseline 큰 글자 | `.m-bl-letter` | `clamp(1.7rem, 8vw, 2.5rem)` | **600** |
| baseline 연결형 | `.m-bl-triple` | `clamp(0.82rem, 4.1vw, 1.15rem)` | 500 |
| 표현 카드 아랍어 | `.m-card.exp .m-ar` (default `.m-card .m-ar`) | `--ar-card-size` | **500** |
| 나쓰 카드 아랍어 | `.m-card.nass .m-ar` | `--ar-nass-size` (line-height 1.6) | **500** |
| 드릴/래퍼토리 페어 아랍어 | `.m-row-ar` | **17px** | **400** (얇음) |
| 5열 셀 아랍어 | `.drill-cell .dc-ar` | **16px** | **500** |
| 5열 셀 음가 | `.drill-cell .dc-trans` | **10px** | 400 italic |
| 패턴 한국어 | `.m-card.pattern .m-ko` | **12px** | **600** |
| 페어 한국어 | `.m-row-ko` | **12px** | 400 |
| 표현/나쓰 한국어 | `.m-card .m-ko` | `--ko-size` (11px) | 500 (나쓰만 **400** — 볼드 없음) |

> **원칙**: 패턴(학습 대상)은 600으로 가장 강조. 그 외 카드 본문 500. 페어 셀(드릴/래퍼토리)의 아랍어는 400(얇게) — 5열 모드는 좁은 칸에서 가독성을 위해 500. 나스 한국어는 대화 가독성을 위해 볼드 미적용(400).

### 모바일 앱 UI 구조

```
┌──────────────────────────┐
│ ☰  유닛 A01      1 / 6   │  ← 상단바 56px
├──────────────────────────┤
│ 표현 │ 패턴 │ 드릴 │ 지문 │  ← 섹션 탭 44px
├──────────────────────────┤
│   [현재 페이지 콘텐츠]    │  ← 스크롤 영역
├──────────────────────────┤
│ ◀  01 / 06  ▶  해석 가리기│  ← 하단바 64px
└──────────────────────────┘
```

**상단바 (56px)** — ☰ 햄버거(사이드바 열기) + 유닛 표시 + 페이지 카운터

**섹션 탭 (44px)** — 4개: 표현 / 패턴 / 드릴 / 지문
- 활성 탭은 액센트 색 + 하단 라인
- 데이터 없는 탭은 disabled (`opacity: 0.32`)
- 탭하면 해당 섹션 첫 페이지로 점프

**페이지 콘텐츠 (스크롤)** — 교재 페이지 1장씩 표시. 모바일 폰트/패딩으로 조정.
- **카드 레이아웃은 교재와 동일 2열 유지** (좌 한국어 LTR / 우 아랍어 RTL)
- 모바일 폰트 크기는 교재보다 작게 (위 토큰 참조)
- baseline 6칸 비례 그대로 (1/6 폭) — 글자 크기만 모바일 폭에 맞춰 축소

**드릴 5열 표** — 모바일(≤480px)에서는 자동으로 **4열로 전환** (`window.matchMedia` 런타임 분기). 좁은 폭 가독성 회피.

**하단바 (64px)** — ◀ prev / 페이지 인디케이터 / ▶ next / 해석 가리기 토글
- 한국어 + 음가 동시 토글 (한 번에 둘 다)
- 텍스트 변환: 보임 = "해석 가리기", 가림 = "해석 보기"
- 상태 영구 저장: `localStorage('m.hide-meaning')`

**사이드바 (유닛 픽커)** — 좌측 슬라이드 아웃, 마스크 클릭 닫기
- 유닛 리스트 (`u` 값 + 한국어 라벨 일부)
- 현재 유닛은 액센트 강조

### 깃발 (모바일 — 1.4.4 갱신)

**파일 형식**: PNG 사용 (`../assets/icons/icon-{egypt,lebanon,saudi}.png`)

> ⚠️ SVG 사용 불가: `assets/icons/icon-*.svg`는 외부 파일(`source-flags/flag-*.svg`)을 `<image href>`로 참조하는 wrapper인데, `<img>` 태그로 SVG를 로드할 때 브라우저 보안 정책으로 SVG 내부의 외부 리소스 참조가 차단되어 빈 원만 보임. 자체 완결된 PNG 사용.

**사이즈 (모바일)**

| 위치 | 사이즈 |
|---|---|
| 표현 카드 / 페어 모드 / 나스 카드 | **12×12** (모바일 컴팩트, 교재 14×14보다 작음) |
| 5열 모드 (`.m-rep-grid`, `.m-drill-grid`) | **표시 안 함** (`display:none`) — 좁은 셀에서 wrap 회피 |

```css
.m-flag {
  display:inline-block;
  width:12px; height:12px;
  border-radius:50%;
  vertical-align:middle;
  flex-shrink:0;
}
.m-rep-grid .m-flags,
.m-drill-grid .m-flags { display:none; }  /* 5열 미표시 */
```

**위치** (교재와 동일):
- 표현/페어 모드: `.m-ar-line` flex 컨테이너 안 아랍어 옆 인라인 (RTL — 깃발이 아랍어 왼쪽에 위치)
- 나스 카드: 좌측 한국어 칸 하단 (`.m-pair-left .m-flags { margin-top:8px }`)

```css
.m-ar-line {
  display:flex;
  align-items:center;
  justify-content:flex-start;  /* RTL에서 start = 오른쪽 */
  gap:6px;
  direction:rtl;
}
```

### baseline 기준선 동적 측정

baseline 모드(알파벳 그룹)의 기준선은 **JS로 첫 글자의 baseline 위치를 측정**해서 동적 정렬 — 폰트 사이즈가 clamp이라 화면 폭에 따라 변하므로 하드코딩 불가.

```js
function adjustBaselines() {
  document.querySelectorAll('.m-bl-grid').forEach(grid => {
    const letter = grid.querySelector('.m-bl-letter');
    if (!letter) return;
    // height:0 + vertical-align:baseline 프로브 — 프로브의 top이 곧 baseline 위치
    const probe = document.createElement('span');
    probe.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline;';
    letter.appendChild(probe);
    const probeRect = probe.getBoundingClientRect();
    const gridRect = grid.getBoundingClientRect();
    probe.remove();
    const baselineFromTop = probeRect.top - gridRect.top;
    if (baselineFromTop > 0) grid.style.setProperty('--bl-top', baselineFromTop + 'px');
  });
}
```

```css
.m-bl-grid::after {
  content:''; position:absolute;
  left:7%; right:7%;
  top:var(--bl-top, 36px);  /* JS가 측정값 주입, fallback 36px */
  height:1.5px; background:rgba(29,73,255,.22);
  pointer-events:none;
}
```

호출 타이밍:
- `paintCurrent()` 끝 — 페이지 렌더 완료 후
- `document.fonts.ready` 후 — 폰트 로드 전 측정하면 fallback 메트릭으로 잘못 계산
- 윈도 리사이즈 시 (디바운스 120ms)

### 드릴/래퍼토리 모드 — `css` 컬럼 값에 따른 분기

| `css` 값 | 모드 | 박스 배치 | 박스 안 구성 | 깃발 |
|---|---|---|---|---|
| `two` | 2열 박스 | **좌→우 2개씩** (LTR 배치) | 아랍어(RTL) + 음가(italic) + 점선 + 한국어(LTR, sub) | 12×12 인라인 ✓ |
| `five` | 5열 셀 | 우→좌 5개씩 (모바일 ≤480px = 4열) | 아랍어(RTL) + 음가만 | 미표시 (좁음) |
| (비어있음) | 디폴트 페어 | 1행 1박스 (스택) | 좌 한국어(LTR) / 우 아랍어(RTL) + 음가 | 12×12 인라인 ✓ |

**우선순위**: `two` > `five` > 디폴트 — 한 그룹 안에 `two` 행이 하나라도 있으면 그 그룹 전체가 2열.

```css
/* 2열 박스 모드 */
.m-rep-grid.cols-two,
.m-drill-grid.cols-two {
  grid-template-columns:1fr 1fr;
  gap:10px;
  direction:ltr;
}
.cols-two .drill-cell {
  background:var(--surface);
  border:1px solid rgba(18,32,90,0.07);
  border-radius:10px;
  padding:10px 12px 11px;
  box-shadow:0 1px 2px rgba(18,32,90,0.035);
  gap:3px;
}
.cols-two .m-ar-line { justify-content:flex-start; direction:rtl; }  /* RTL start = 오른쪽 */
.cols-two .dc-ar, .cols-two .dc-trans { text-align:right; direction:rtl; }
.cols-two .dc-ko {
  font-size:var(--ko-size); color:var(--sub);
  text-align:left; direction:ltr;
  margin-top:5px; padding-top:5px;
  border-top:1px dashed var(--border-soft);
}
```

**깃발 표시 규칙**:
```css
/* 5열 모드만 깃발 미표시. 2열은 표시 */
.m-rep-grid:not(.cols-two) .m-flags,
.m-drill-grid:not(.cols-two) .m-flags { display:none; }
/* 모바일 ≤480px: 5열 → 4열 (2열은 그대로) */
@media (max-width:480px) {
  .m-rep-grid:not(.cols-two),
  .m-drill-grid:not(.cols-two) { grid-template-columns:repeat(4, 1fr); }
}
```

### 인터랙션

**탭 → 오디오 재생**

모든 아랍어 텍스트 요소에 `.tap-audio` 클래스 부여:
- 탭하면 오디오 재생, 재생 중 해당 요소만 액센트 색(`var(--accent)`) 하이라이트 (`.playing` 클래스)
- 같은 항목 재탭 → 정지
- 다른 항목 탭 → 이전 정지 후 새로 재생

**오디오 URL 우선순위 (1.4.4)**:
1. 시트 `url` 컬럼 (있으면 우선)
2. `https://storage.googleapis.com/all-that-arabic-14/audio/{유닛U}/{id}.wav` 자동 생성, .mp3 폴백
   - id는 행의 `id_*` 컬럼 (드릴은 `id_drill`, 표현은 `id_kalimat`, 나쓰는 `id_nass`, 패턴은 `id_ptn(no)` 등)

**페이지 네비게이션**
- 하단 ◀ ▶ 버튼
- 섹션 탭으로 점프
- **좌우 스와이프 제스처** — `touchstart` 좌표와 `touchend` 좌표 차이로 판정:
  - 가로 이동 ≥ **40px** AND 가로 ≥ 세로 × **1.2배** → 페이지 이동
  - dx < 0 (왼쪽 스와이프) → 다음 / dx > 0 (오른쪽) → 이전
- **iOS Safari swipe-back 가로 가로채기 차단**: 스크롤 영역(`.m-body`)에 `touch-action: pan-y` + `overscroll-behavior-x: none` 적용. 가로 동작은 앱이 처리, 세로만 브라우저에 위임

**해석 토글**
- 하단바 단일 버튼 — 한국어와 음가를 함께 토글 (`.hide-ko` + `.hide-trans` 동시 적용)
- 상태 영구 저장 (localStorage)

### 알려진 이슈 / 추후 작업

- [ ] **진도 표시** — 읽은 페이지/유닛 (localStorage)
- [ ] **북마크** — 즐겨찾기 페이지
- [ ] **검색** — 표현/지문
- [ ] **오디오 자동재생 큐** — 페이지의 모든 오디오 순차 재생
- [ ] **다크 모드** — 디자인 토큰 다크 변형
- [ ] **다운로드/오프라인** — PWA 가능성

>(통합 검토 조건은 본 섹션 상단 "배경 / 옛 이름 매핑" 참고)

---

## 사용자앱 (학생용 모바일)

**구현 파일**: `ata144_student/ata144_student.html`

**목적**: 모바일에서 혼자 복습. 배운 패턴 반복 연습. 레퍼토리 슬라이드 생략.

### 레이아웃
- 전체: `position: fixed; overflow: hidden;` 풀스크린 슬라이드
- 세로(모바일) 중심 레이아웃, `max-width: 640px`
- `flex column, height: 100dvh`
- 660px 이상에서 카드형(상하 28px 여백 + border-radius)
- 하단: 이전/다음 버튼 (터치 스와이프 + 버튼)
- 사이드바: 유닛 인덱스 (M키 또는 메뉴 버튼)

```css
.app {
  display: flex; flex-direction: column;
  height: 100dvh; max-width: 640px;
  margin: 0 auto; background: var(--surface);
}
```

### 노출 타입 (SHOW_TYPES)

ptn, mithāl, drillA, exp, kalimat, nass

레퍼토리(`repertory`)는 **사용자앱에서 제외**. 나머지 로직(status=confirmed 필터, 유닛 순서, 나쓰 포함)은 선생님앱과 동일.

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
- 음가(`.note-text`): **항상 표시** — 토글 무관

```css
.app.meaning-hidden .korean-text { display: none; }
.app.meaning-hidden .ptn-summary { display: flex !important; }
/* .note-text는 토글 영향 없음 — opacity: 1 고정 */
```

### 패턴 슬라이드 렌더링 (ptn-summary)

ptn 타입은 드릴탭의 `summary` 컬럼 내용을 설명 영역으로 표시. 없으면 `scriptA` fallback.

- 아랍어(`arabic`)가 있으면 상단에 작게
- summary/scriptA 텍스트를 줄 단위 파싱:
  - `- `로 시작 → 불릿 (점 + 텍스트)
  - 일반 줄 → 산문(prose) 단락
- 줄바꿈, 인라인 스타일(`**bold**`, `*italic*`, `[[arabic]]`) 지원

```css
.ptn-summary {
  display: none;  /* 기본 숨김 */
  flex-direction: column; gap: 8px;
  max-width: 540px; width: 100%; align-self: center;
  direction: ltr; margin-top: 4px;
}
.app.meaning-hidden .ptn-summary { display: flex !important; }

.ptn-prose {
  font-size: clamp(.85rem, 2cqi, .95rem);
  line-height: 1.85; color: var(--sub);
  text-align: left; white-space: pre-line;
}
.ptn-bullet {
  display: flex; gap: 8px; align-items: flex-start;
  font-size: clamp(.82rem, 1.8cqi, .9rem);
  line-height: 1.7; color: var(--text);
}
.ptn-bullet-dot { color: var(--accent); font-size: 14px; }
```

### 스와이프 제스처
- `touchstart`와 `touchend` 좌표 차이로 슬라이드 이동 감지
- 수평 이동 **42px 이상** + 수직 이동의 **1.5배 이상** → 슬라이드 이동
- 왼쪽 스와이프 → 다음 / 오른쪽 → 이전

### 컴포넌트
- **상단 바** — 유닛·슬라이드 번호 + 해석 토글 버튼
- **슬라이드 카드** — 스크롤 가능, 중앙 정렬, 하단 스와이프 힌트
- **하단 버튼** — 이전(`‹`) / 다음(`›`)
- **사이드바** — 유닛 인덱스 (선생님앱과 동일 구조)
- **해석 토글 버튼** — 한국어·노트 가리기/보기

### 로딩 화면
선생님앱과 동일: `--accent`(#1D49FF) 배경, 중앙 흰색 로고, 하단 `markazarabic 1.4.4 beta` 라벨.

### 첫 방문 온보딩
`localStorage` 플래그(`ata144s_onboarded`)로 첫 방문 여부 확인. 첫 방문 시 조작법 안내 화면, 이후 건너뜀.

### 하이라이트 마크업 (앱 고유 클래스명)
- `_단어_` → `.hl-box` (파란 테두리)
- `*단어*` → `.hl-bold` (볼드 강조), 아랍어면 `.hl-ar` 추가

> 통일 작업 진행 중 — 향후 `.hl-text` / `.hl-box-inline`으로 통일 예정.

---

## 선생님앱 (수업용 가로 대형)

**구현 파일**: `ata144_teacher/ata144_teacher.html`

**목적**: 오프라인/온라인 수업 현장. TV·모니터 등 대형 가로화면. 선생님이 직접 조작.

### 레이아웃
- 전체: `position: fixed; overflow: hidden;` 풀스크린 슬라이드
- `#main`: 중앙 고정 컬럼 (`width: min(92vw, 1400px)`, flex column, 상하 패딩 `clamp(60px,10vh,100px) / clamp(80px,12vh,120px)`)
- `#arabic-area`: **반드시 `container-type: inline-size; width: 100%;`** (cqi 단위 사용)
- 4코너 UI는 `position: fixed`:
  - `#ui-tl`: 좌상단 — 유닛명 + 섹션 탭
  - `#ui-tr`: `#main` 내 상단 — 타입 레이블 + 라하 국기
  - `#ui-bl`: 좌하단 — 저작권
  - `#ui-br`: 우하단 — 로고
- `#toolbar`: 하단 중앙 — 단축키 바
- `#sidebar`: 좌측 슬라이드아웃 — 유닛 인덱스

### 타이포그래피

| 요소 | 폰트 | 크기 |
|---|---|---|
| 아랍어 (기본) | Noto Sans Arabic 700 | `clamp(3rem, 9vw, 9rem)` |
| 아랍어 (문장형 — 유닛 A/G) | Noto Sans Arabic 700 | `clamp(2rem, 6vw, 6rem)` |
| 아랍어 (쓰기체) | Dongol / Noto Kufi Arabic | 동일 |
| 한국어 | Spoqa Han Sans Neo | `clamp(1.2rem, 3.5vw, 3.5rem)` |
| 노트 | Spoqa Han Sans Neo | `clamp(0.9rem, 2.2vw, 2.2rem)` |
| 타입 레이블 | Spoqa Han Sans Neo | `clamp(0.55rem, 0.85vw, 0.75rem)` |
| 사이드바 헤더 | Spoqa Han Sans Neo | `clamp(1.1rem, 2.5vw, 1.6rem)` |
| 인덱스 항목 | Spoqa Han Sans Neo | `clamp(0.75rem, 1.6vw, 1.1rem)` |
| 단축키 바 | Spoqa Han Sans Neo | `clamp(0.6rem, 0.9vw, 0.78rem)` |

행간: 아랍어 `1.6` / 한국어·노트 `1.4` / 단축키 리스트 `2.1`

```css
.arabic {
  font-family: 'Noto Sans Arabic', serif;
  font-size: clamp(3rem, 9vw, 9rem);
  font-weight: 700; direction: rtl; line-height: 1.6;
}
.arabic.arabic-sentence { font-size: clamp(2rem, 6vw, 6rem); }
.korean { font-size: clamp(1.2rem, 3.5vw, 3.5rem); transition: opacity 0.3s; }
.note {
  font-size: clamp(0.9rem, 2.2vw, 2.2rem);
  color: var(--sub);
  opacity: 1;  /* 항상 표시 — 해석 토글 무관 */
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

### 내비게이터 로직

**사이드바 (왼쪽 인덱스)**
- M키 또는 메뉴 버튼으로 토글
- pattern탭의 `ptnA` 타입 항목 중 `status = confirmed`만 표시
- 각 항목: 아랍어 / 한국어 줄바꿈, 둘 다 좌측 정렬
- 항목 누르면 해당 유닛 첫 슬라이드로 이동 + 사이드바 닫힘
- 너비 `min(440px, 92vw)`, 좌측 슬라이드 인입
- `border-right: 1px solid var(--border)`, `box-shadow: 4px 0 24px rgba(29,73,255,0.10)`

**상단 좌측 영역 (`#ui-tl`)**
- `position: fixed`, `max-width: 75vw`
- 내부 flex row: ① ptnA 정보(유닛번호 + 아랍어·한국어 가로) ② 섹션 탭
- 어떤 슬라이드를 봐도 현재 유닛의 ptnA 아랍어/한국어 항상 고정 표시 (대표 패턴)

```
[유닛번호] [ptnA 아랍어] [ptnA 한국어]    [패턴] [드릴] [표현] [칼리마트] [나스]
```

**섹션 탭 (상단 우측)** — 현재 유닛 안에서 해당 타입 첫 슬라이드로 점프. 데이터 없으면 비활성 (opacity 낮춤, 클릭 불가).

| 탭 | 매칭 타입 | 데이터 출처 |
|---|---|---|
| 패턴 Pattern | `ptn`, `ptna` | drill 탭 |
| 드릴 Drill | `drilla` | drill 탭 |
| 표현 Expression | `exp` | kalimat 탭 |
| 칼리마트 Kalimat | `kalimat` | kalimat 탭 |
| 나스 Nass | `nass` | nass 탭 |

### 컴포넌트

- **로딩 화면** — `--accent` 배경 전체화면, 중앙 흰색 로고(`ata-logo2.png`), 하단 `markazarabic 1.4.4 beta` 라벨 (흰색, `opacity: 0.75`, `letter-spacing: 2.5px`, 소문자)
- **진행바** — 상단 고정, 높이 3px, `--accent`, 슬라이드 진행률에 따라 너비 변화
- **하이라이트 박스** — `border: 3px solid var(--accent)` / `background: var(--accent-bg)` / `border-radius: 14px`
- **인덱스 항목 (`.idx-item`)** — `display: flex`, `gap: 0.7rem`, `align-items: baseline`, `border-left: 4px solid transparent`. 활성: `--accent` border + `var(--accent-bg)` 배경. 아랍어(`idx-ar`)·한국어(`idx-ko`) 모두 `text-align: left`
- **인덱스 태그 (`.idx-tag`)** — `font-size: 0.72em`, `background: var(--accent-bg)`, `border-radius: 4px`, 대문자
- **단축키 바** — 하단 중앙 고정, 투명 배경, 기본 `opacity: 0.6`, 활성 시 `1`. 아이콘 없이 텍스트만
- **단축키 뱃지 (`.kb`)** — `background: var(--bg)`, `border: 1px solid var(--border)`, `border-radius: 3px`
- **해석 토글** — Space 키, 한국어·노트 가리기/보기
- **본문 토글** — A 키, 아랍어 가리기/보기 (opacity 0)

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

### Write 애니메이션 모드 (`css = 'write'`)

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
```js
const wipeDuration = 0.5 + charCount * 0.5;  // 글자 수 비례
setTimeout(() => {
  token.style.transition = `clip-path ${wipeDuration}s linear`;
  requestAnimationFrame(() => {
    token.style.clipPath = 'inset(-40% 0% -40% 0%)';
  });
}, 400 + i * (wipeDuration * 1000 + 600));  // 순차 지연
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
.bl-label { font-size: clamp(0.6rem, 1.2vw, 1rem); color: var(--sub); }
```

### Book View 모드 (`B` 키)

`body.book-view` 클래스 토글로 동작.
- 슬라이드 UI 전체 숨김 (`#main`, `#sidebar`, `#toolbar`, `#ui-*` → `display: none !important`)
- `#book-root` 표시 → B5 비율 페이지 카드 렌더링
- 용도: 교재 초안 PDF 출력 미리보기

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

### 라하(방언) 깃발 (선생님앱)

타입 레이블 옆에 원형 국기 아이콘.
```html
<img src="../assets/icons/icon-egypt.svg" style="width:1.1em;height:1.1em;border-radius:50%;">
```

### 하이라이트 마크업
- `_단어_` → `.hl-box` (파란 테두리 박스)
- `*단어*` → `.hl-text` (파란 강조 텍스트, weight는 공통 규칙 참조 — 부모 weight 상속)

---

## 앱별 비교 요약

| 항목 | 교재 원본 (B5 인쇄) | 교재앱 (모바일) | 사용자앱 | 선생님앱 |
|---|---|---|---|---|
| 구현 파일 | `ata144_original/ata144_original.html` | `ata144_textbook/ata144_textbook.html` | `ata144_student/ata144_student.html` | `ata144_teacher/ata144_teacher.html` |
| 화면 | B5 데스크톱·인쇄 | 모바일 세로 | 모바일 세로 | 가로 대형 (TV·모니터) |
| 이동 방식 | 페이지(인쇄) | 스와이프 + 탭 + 버튼 | 스와이프 + 버튼 | 키보드 ←→ |
| 레퍼토리 | ✅ | ✅ | ❌ | ✅ |
| Write 애니메이션 | — | — | — | ✅ (write css) |
| Book View | — (그 자체가 book) | — | — | ✅ (B 키) |
| 라하 국기 | ✅ | ✅ | ✅ | ✅ |
| 의미 토글 | — | 버튼 (한/음가 같이) | 버튼 (한국어만) | Space (한/노트) |
| 음가 항상 표시 | ✅ (인쇄용) | 토글 따라 | ✅ | ✅ |
| 카드 2열 (한/아) | ✅ | ✅ | — (슬라이드형) | — (슬라이드형) |
| 슬라이드형 | — | — (스크롤) | ✅ | ✅ |
| 페이지 자동 분할 | ✅ (드릴) | — | — | — |

---

## CSS 코드 (시트 `css` 컬럼)

각 데이터 행의 `css` 값으로 표시 양식·노출 범위를 제어한다. `baseline` / `five` / `two` / `write` 등 표시 양식 코드는 본 문서의 각 앱 절(教재 인쇄 / 교재앱 / 선생님앱)에서 개별 정의한다.

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
