# ATA (All That Arabic) 프로젝트 지침

## 제품 개요
올댓아라빅(All That Arabic) 아랍어 수업용 슬라이드 앱.
현재 버전: **1.4.4**

---

## 저장소 구조

```
ATA-14/                                         GitHub Pages 배포 루트 (저장소 자체)
├── index.html                                  랜딩 (앱 링크)
│
│   # 1.4.4 (현행)
├── ata144_original/ata144_original.html        교재 (인쇄 B5 원본)
├── ata144_teacher/ata144_teacher.html          메인앱 (선생님용)
├── ata144_textbook/ata144_textbook.html        교재용 앱 (학생용 모바일)
├── ata144_student/ata144_student.html          (legacy 슬라이드형 학생앱 — index 미노출)
│
│   # 1.4.3 (legacy, 병행 운영)
├── ata143_teacher/ata143_teacher.html          메인앱 (선생님용)
├── archive/app143s.html                        복습앱 (학생용, summary 슬라이드 포함)
│
├── app144.html, app144s.html                   옛 URL → 새 URL redirect stub
├── assets/                                     공유 자산 (로고, 폰트, 국기 아이콘)
│
├── product-ata144.md                           제품 문서 (메인)
├── product-ata144-appendix.md                  CSS 부록
├── product-ata144-audio-rules.md               오디오 생성 규칙
├── product-ata144-image-rules.md               이미지 생성 규칙
├── product-ata144-design.md                    디자인 코드 문서
├── product-ata144-design(mobile).md            모바일 앱 실험 기록
└── archive/                                    옛 버전 (142, 143)
```

### 산출물 5종 (현행 + legacy)
| # | 산출물 | 로컬 경로 | 배포 URL |
|---|---|---|---|
| 1 | 1.4.4 교재 (인쇄) | `ata144_original/ata144_original.html` | https://rasheedpark.github.io/allthatarabic/ata144_original/ata144_original.html |
| 2 | 1.4.4 메인앱 (선생님용) | `ata144_teacher/ata144_teacher.html` | https://rasheedpark.github.io/allthatarabic/ata144_teacher/ata144_teacher.html |
| 3 | 1.4.4 교재용 앱 (학생용) | `ata144_textbook/ata144_textbook.html` | https://rasheedpark.github.io/allthatarabic/ata144_textbook/ata144_textbook.html |
| 4 | 1.4.3 메인앱 (선생님용, legacy) | `ata143_teacher/ata143_teacher.html` | https://rasheedpark.github.io/allthatarabic/ata143_teacher/ata143_teacher.html |
| 5 | 1.4.3 복습앱 (학생용, legacy) | `archive/app143s.html` | https://rasheedpark.github.io/allthatarabic/archive/app143s.html |

랜딩: https://rasheedpark.github.io/allthatarabic/

### 에셋 경로 (앱 내부)
앱이 하위 폴더(`ata144_teacher/`, `ata144_textbook/`, `ata144_original/`, `ata143_teacher/`)에 있으므로 에셋을 `../assets/...`로 참조. `archive/app143s.html`도 `../assets/...`.
- 폰트: `../assets/fonts/Dongol-Regular.otf`
- 로고: `../assets/ata-logo2.png`
- 국기: `../assets/icons/icon-egypt.png`, `icon-lebanon.png`, `icon-saudi.png`

### 작업/배포 워크플로
| 브랜치 | 역할 |
|---|---|
| `main` | 배포 — GitHub Pages가 서빙. |
| `dev`  | 작업 — 일상 작업 모두 여기서. |

```bash
# 일상 작업
git checkout dev
# 파일 수정
git add .
git commit -m "메시지"
git push origin dev

# 배포
git checkout main
git merge dev
git push origin main
git checkout dev
```

---

## 스프레드시트 (1.4.4)
**Sheet ID**: `1w7e0mLLgFhzU7Ixs6CUfzgrwUG6EEy8jHijXF5UJwY8`

### 시트 탭 구조
| 탭명 | 포함 타입 | 주요 컬럼 |
|---|---|---|
| `units` | unit | C, U, arabic, korean, note, type, status, id_unit |
| `pattern` | ptnA, ptnB | C, U, arabic, korean, note, type, status, id_ptn, id_ptn(no) |
| `drill` | ptn, repertory, mithāl, drillA, drillB, summary, writing | C, U, arabic, korean, note, type, status, id_drill, ref_ptn, lahja, script, css, url |
| `kalimat` | exp, kalimat | C, U, arabic, korean, note, type, status, id_kalimat |
| `nass` | nass | C, U, arabic, korean, note, type, status, id_nass, ptn_key |

> **TAB 상수 (앱 코드)**
> - `TAB_UNIT = 'units'` (단수 아님, 복수)
> - `TAB_KALIMAT = 'kalimat'` (exp와 kalimat 타입 모두 이 탭에 있음)
> - 선생님용 앱은 추가로 `TAB_REPERTORY = 'repertory'`, `TAB_EXPRESSION = 'expression'` 탭도 참조

### 슬라이드 순서 (buildSlides 기준)
```
유닛 슬라이드 (unit)
패턴별 반복:
  패턴 슬라이드 (ptn)
  → 레퍼토리 슬라이드 (repertory, ref_ptn 매칭)
  → 드릴A 슬라이드 (drillA, ref_ptn 매칭)
드릴B/C (연습, 해당 유닛 전체)
표현 슬라이드 (exp)
나스 슬라이드 (nass)
단어 슬라이드 (kalimat)
```

### status 필터
- 모든 탭에서 `status = confirmed`인 행만 앱에 노출된다.

---

## 앱 구조

### 공통
- **단일 HTML 파일** — 외부 JS/CSS 없음 (구글 폰트·CDN 폰트 제외)
- JSONP(gviz/tq)로 구글 시트 직접 읽음
- `_cache` 객체로 탭별 데이터 메모리 캐시
- `status = confirmed` 필터 적용
- 오디오: GCS `all-that-arabic-14/listening144/{key}.mp3` (실패 시 `.wav` 폴백)

### 선생님용 앱 (`ata144_teacher.html`)
- 대형 화면 (TV, 모니터) 최적화, 가로 레이아웃
- 키보드: `←→` 이동, `Space` 해석 토글, `A` 아랍어 토글, `M` 사이드바, `S` 오디오, `T` 나스 지문
- 상단 좌측: 유닛 정보 + 섹션 탭 (패턴/연습/표현/지문/단어)
- 상단 중앙: 슬라이드 타입 레이블 + 라흐자 국기
- `css = 'write'`: Dongol 폰트 + R→L clip-path 와이프 애니메이션
- `css = 'baseline'`: 글자 하단 라인 정렬 그리드
- Book view 모드(`B` 키): B5 교재 초안 PDF 형태로 렌더링
- `container-type: inline-size` on `#arabic-area` (cqi 단위 필요)

### 학생용 앱 (`ata144_student.html`)
- 모바일 최적화, 세로 레이아웃
- 스와이프(터치) + 버튼 이동
- 레퍼토리 슬라이드 생략 (학생 복습 목적)
- 패턴 요약(ptn summary) 표시
- `TAB_UNIT = 'units'`, `TAB_KALIMAT = 'kalimat'`

---

## 아랍어 표기 원칙

1. **격모음(إعراب) 미표기** — 명사의 마지막 모음은 표시하지 않는다.
   - 탄윈(ـٌ ـٍ ـً) 사용 안 함
   - 마지막 격어미 모음(ـُ ـِ ـَ) 표시 안 함
   - 예: مُدَرِّس ✓ / مُدَرِّسٌ ✗ — هَذَا طَالِب ✓ / هَذَا طَالِبٌ ✗

2. **지시대명사** — 대거 알리프(ـٰ) 없이 파트하로 표기
   - هَذَا ✓ / هٰذَا ✗ — ذَلِكَ ✓ / ذٰلِكَ ✗

3. **음가(romanization)** — `note` 컬럼. 항상 소문자 + 발음구별부호
   - ā ī ū / ʕ / ṣ ḍ ṭ ẓ ḥ / th dh sh
   - 앱에서 항상 표시 (의미 토글 영향 받지 않음)

---

## ID 명명 규칙

모든 행은 ARRAYFORMULA로 자동 생성되는 고유 ID를 가진다.

| 탭 | id 컬럼 | 형식 | 예시 |
|---|---|---|---|
| `units` | `id_unit` | `{U}_{slug(note)}` | `A01_ba-ta-tha-nun-ya` |
| `pattern` | `id_ptn` | `ptn_{slug}` | `ptn_ba-bu-bi` |
| `pattern` | `id_ptn(no)` | `ptn{NNN}_{slug}` | `ptn002_ba-bu-bi` |
| `drill` | `id_drill` | `{type_lower}_{slug}` | `drilla_banata` |
| `kalimat` | `id_kalimat` | `{type_lower}_{slug}` | `exp_as-salamu`, `kalimat_ana` |
| `nass` | `id_nass` | `nass_{첫3단어_slug}` | `nass_as-salamu-alaykum` |

`slug(note)`: note값을 소문자·하이픈 정규화한 문자열.

---

## 나스(nass) 작성 규칙

**나스에 쓸 수 있는 단어는 딱 두 가지 타입뿐:**
1. **`kalimat`** 타입으로 등록된 어휘
2. **`exp`** 타입으로 등록된 표현

- 해당 유닛에 kalimat가 없으면 → 이전 유닛까지 누적된 `exp`만 사용
- drill, repertory, summary, pattern 등 다른 타입에만 있는 단어는 **절대 사용 불가**
- 이름(alam 타입)은 사용 가능
