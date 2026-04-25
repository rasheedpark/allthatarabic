# ATA (All That Arabic) 프로젝트 지침

## 제품 개요
올댓아라빅(All That Arabic) 아랍어 수업용 슬라이드 앱.
현재 버전: **1.4.2** (`app142.html`)

---

## 스프레드시트 (1.4.2)
**Sheet ID**: `1ZRSqvWf1kRRv6s-ifa56Pud1puQKdzbAGzLIstlN_M0`

### 시트 탭 구조
| 탭 | 주요 컬럼 | U열 형식 |
|---|---|---|
| `pattern` | arabic, korean, note, category, id_pattern | 없음 (비어있음) |
| `repertory` | c, u, arabic, korean, note, category, id_repertory, id_pattern | `p1`, `p2`... |
| `drill` | c, u, arabic, korean, note, category, id_drill, id_pattern | `p1`, `p2`... |
| `expression` | c, u, arabic, korean, note, category, id_expression, id_pattern | `1`, `2`... (숫자) |
| `nass` | arabic, korean, note, category, id_words, id_pattern, sual | `1`, `2`... (숫자) |

### id_pattern 명명 규칙
- `P01`, `P01a`, `P01b`, `P01c` → 유닛 p1의 서브패턴
- `P02`, `P02a`, `P02b` → 유닛 p2의 서브패턴
- 패턴 시트의 C/U열은 비어있음. id_pattern으로만 그룹 판단.

### U열 매핑 (유닛 번호 대응)
- repertory/drill의 `u = "p1"` ↔ expression/nass의 `u = "1"` (p1 = 1)
- `p2` ↔ `2`, `p3` ↔ `3` ...

---

## 슬라이드 구조 (핵심 규칙)

### 슬라이드 순서
유닛별로 다음 순서를 반복:

```
유닛 p1
├── 서브패턴 P01
│   ├── 패턴 슬라이드 (id_pattern = "P01")
│   ├── 레퍼토리 슬라이드 (id_pattern = "P01", id_repertory 순)
│   └── 드릴 슬라이드 (id_pattern = "P01", id_drill 순)
├── 서브패턴 P01a
│   ├── 패턴 슬라이드 (id_pattern = "P01a")
│   ├── 레퍼토리 슬라이드 (id_pattern = "P01a")
│   └── 드릴 슬라이드 (id_pattern = "P01a")
├── 서브패턴 P01b
│   ├── 패턴 슬라이드
│   ├── 레퍼토리 슬라이드 (id_pattern = "P01b")
│   └── 드릴 슬라이드 (id_pattern = "P01b")
├── 서브패턴 P01c ...
├── 익스프레션 슬라이드 (expression u = "1", id_expression 순)
└── 나스 슬라이드 (nass u = "1", id_words 순)

유닛 p2 (같은 구조 반복)
...
```

### 핵심 규칙
1. **패턴끼리 먼저 묶으면 안 됨** — 서브패턴 하나씩 순서대로 처리
2. 각 서브패턴 안에서: **패턴 → 레퍼토리 → 드릴** 순
3. 서브패턴 정렬: id_pattern 알파벳 순 (P01 < P01a < P01b < P01c)
4. 레퍼토리/드릴 연결 기준: **id_pattern 컬럼** (u열이 아님)
5. 익스프레션/나스는 해당 유닛의 모든 서브패턴이 끝난 뒤에 표시
6. 익스프레션/나스 필터: expression u="1" = p1, u="2" = p2 (숫자 대응)

---

## 앱 구조 (app142.html)

- **단일 HTML 파일** — 외부 JS/CSS 없음
- JSONP로 구글 시트 직접 읽음 (`&headers=1`)
- 키보드: `←→` 이동, `Space` 해석 토글, `M` 사이드바, `S` 오디오, `T` 나스 지문
- 배포: GitHub Pages (`https://rasheedpark.github.io/allthatarabic/app142.html`)

---

## 아랍어 표기 원칙

1. **격모음(إعراب) 미표기** — 명사의 마지막 모음은 표시하지 않는다.
   - 탄윈(ـٌ ـٍ ـً) 사용 안 함
   - 마지막 격어미 모음(ـُ ـِ ـَ) 표시 안 함
   - 예: مُدَرِّس ✓ / مُدَرِّسٌ ✗ — هَذَا طَالِب ✓ / هَذَا طَالِبٌ ✗

2. **지시대명사** — 대거 알리프(ـٰ) 없이 파트하로 표기
   - هَذَا ✓ / هٰذَا ✗ — ذَلِكَ ✓ / ذٰلِكَ ✗

3. **음가(romanization)** — 항상 소문자 + 발음구별부호 사용
   - ā ī ū / ʕ / ṣ ḍ ṭ ẓ ḥ / th dh sh

---

## 나스(nass) 작성 규칙

**나스에 쓸 수 있는 단어는 딱 두 가지 타입뿐:**
1. **`kalimat`** 타입으로 등록된 어휘
2. **`exp`** 타입으로 등록된 표현

- 해당 유닛에 kalimat가 없으면 → 이전 유닛까지 누적된 `exp`만 사용
- drill, repertorie, summary, pattern 등 다른 타입에만 있는 단어는 **절대 사용 불가**
- 이름(alam 타입)은 사용 가능

---

## 향후 계획
- 챕터별 파일 생성 (선생님에게 링크 공유)
- 마스터앱: 챕터 선택 가능한 통합 버전
- 두 번째, 세 번째 제품 양식은 추후 정의
