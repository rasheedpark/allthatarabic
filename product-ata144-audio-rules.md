# ATA 1.4.4 듣기 파일 생성 및 적용 규칙

이 문서는 ATA 1.4.4의 듣기 오디오 파일을 생성하고 앱에서 연결하는 기준을 정의한다. 기준 앱은 `ata144_teacher/ata144_teacher.html`, `ata144_student/ata144_student.html`, `textbook144m.html`, `ata144_textbook/ata144_textbook.html`이다. 일반 학습 오디오는 `archive/ata-audio-pipeline/generate_144_audio.py`, 지문 오디오는 `archive/ata-audio-pipeline/generate_144_nass_elevenlabs.py`로 생성한다.

## 1. 기본 원리

ATA 1.4.4 앱은 시트의 각 행에서 유닛 코드와 ID 값을 읽고, Google Cloud Storage의 정해진 경로에서 파일을 직접 찾는다. 앱은 먼저 `.mp3`를 시도하고, 실패하면 `.wav`를 시도한다.

```text
https://storage.googleapis.com/all-that-arabic-14/audio/{unit_code}/{id}.mp3
https://storage.googleapis.com/all-that-arabic-14/audio/{unit_code}/{id}.wav
```

예를 들어 `U = A01`, `id_drill = dri_banata`이면 앱은 아래 순서로 요청한다.

```text
https://storage.googleapis.com/all-that-arabic-14/audio/A01/dri_banata.mp3
https://storage.googleapis.com/all-that-arabic-14/audio/A01/dri_banata.wav
```

현재 일반 학습 오디오 생성 스크립트는 Google Cloud Text-to-Speech의 `ar-XA-Chirp3-HD-Aoede` 보이스를 사용해 WAV 파일을 만들고, `gs://all-that-arabic-14/audio/{unit_code}/`에 업로드한다.

지문(`nass`) 오디오는 대화 자연성이 중요하므로 Google TTS가 아니라 ElevenLabs를 사용한다. 나쓰 전용 생성 스크립트는 `archive/ata-audio-pipeline/generate_144_nass_elevenlabs.py`이며, 출력 파일명과 업로드 위치는 다른 오디오와 동일하게 `audio/{unit_code}/{id_nass}.mp3`를 따른다.

개발 테스트 중 WAV만 올려 둔 상태에서는 앱 URL에 `audio=wav`를 붙이면 `.wav`를 먼저 요청한다. 예: `?unit=A01&audio=wav`.

## 2. 저장소 구조

오디오 파일은 스토리지 버킷 안에 `audio` 폴더를 만들고, 그 아래에 유닛 코드 폴더를 둔다.

```text
all-that-arabic-14/
└── audio/
    ├── A01/
    │   ├── ptn_ba-bu-bi.wav
    │   ├── rep_ba.wav
    │   ├── dri_banata.wav
    │   └── exp_as-salamu-alaykum.wav
    ├── A02/
    └── A03/
```

유닛 코드는 시트의 `U` 값을 사용한다. `--unit 1`, `--unit p1`, `--unit A01`은 생성 스크립트에서 모두 `A01`로 정규화된다.

## 3. 대상 데이터

듣기 파일 생성 대상은 아래 탭의 `status = confirmed` 행이다.

| 탭 | 대상 타입 | 설명 |
|---|---|---|
| `pattern` | `ptn` | 패턴 대표음 |
| `repertory` | `repertory`, `repertorie` | 패턴별 대표 예문과 발음 레퍼토리 |
| `drill` | `drillA`, `drillB`, `drillC` | 따라 읽기와 연습 문장 |
| `expression` | `exp` | 유닛별 표현 |
| `nass` | `nass`, `nass+` | ElevenLabs로 생성하는 지문 대화 |

`units`, `kalimat`는 현재 자동 생성 대상에 포함하지 않는다.

### 3.1 지문(nass) ElevenLabs 생성 규칙

나쓰는 `nass` 탭의 `status = confirmed` 행을 대상으로 한다. 파일명은 반드시 `id_nass`와 같아야 하며, 앱은 아래 위치에서 먼저 MP3를 찾는다.

```text
audio/{U}/{id_nass}.mp3
```

ElevenLabs 입력문에는 각 발화 앞에 `[naturally] [correctly]`를 붙인다. 이는 대화를 자연스럽고 정확하게 읽도록 유도하기 위한 TTS 지시문이며, 앱에 표시되는 아랍어 원문에는 영향을 주지 않는다.

나쓰는 남녀 화자를 명확히 나누어 생성한다. 한 지문 안의 줄 단위 발화를 각각 별도 입력으로 보내고, 각 줄에 남성/여성 목소리를 배정한다. 자동 추정이 애매한 지문은 스크립트의 `SPEAKER_OVERRIDES`에 `M,F`처럼 직접 지정한다.

목소리 배정은 다양성을 유지하되 가중치를 둔다. 가중치가 붙은 목소리는 같은 조건에서 더 자주 선택된다.

| 구분 | 목소리 후보 |
|---|---|
| 남성 | Faisal Ali(사우디, 가중치), Adeeb(사우디), Jeddawi(사우디), Hijazi(현대표준), Ghawi(걸프), Hadi N(레반틴) |
| 여성 | Heba Mansuri – Arabic Customer Care(사우디, 가중치), Salma(걸프), Noura(걸프), Farah(요르단, 가중치), Sara-soft, calm and gentle(요르단), Lina(요르단), Laloosh-warm finance(레반틴), Refoush(레반틴) |

ElevenLabs에는 같은 이름의 목소리가 여러 개 있을 수 있으므로, 목소리 규칙에는 단순 이름이 아니라 계정에 표시되는 전체 voice name을 적는다. 특히 Heba Mansuri는 중복 항목이 있으므로 아래처럼 구별한다.

| 표시 이름 | voice id | 사용 여부 |
|---|---|---|
| Heba Mansuri – Arabic Customer Care | QsV9PCczMIklRM6xLPAS | 사용 |
| Heba Mansuri - Gentle and Calm | v7UCHHCrHj1KBa4E41gb | 제외 |
| Heba Mansuri - Tough Recovery Agent | E4GutuQ39akNBbiYuhh2 | 제외 |

방언 태그에 따른 목소리 제한은 다음과 같다.

- 표준어/걸프 태그: 사우디, 걸프, 현대표준 목소리를 같은 풀로 사용한다.
- 레반트 태그: 레반틴 목소리와 요르단 목소리만 사용한다. 레반틴 목소리는 레반트 태그가 붙은 지문에만 사용한다.
- 이집트 태그: 이집트 목소리만 사용한다. 아직 이집트 목소리가 배정되지 않았으므로 생성 전에 목소리 후보를 먼저 추가한다.

발음이 자연스럽지 않을 때는 앱 원문을 고치지 않고 TTS 입력문만 조정한다. 우선순위는 `tss -> tts -> tts_script -> tts_arabic -> arabic`이다. 예를 들어 완료시제 여성형 발음에 보조 `ي`가 필요하거나, 휴지에서 타마르부타를 `ـه`처럼 들리게 해야 하는 경우에는 `tss` 또는 스크립트의 보정 규칙으로 처리한다. 이 규칙은 실제 테스트를 통해 점진적으로 구체화한다.

## 4. 파일명 산출 규칙

파일명은 확장자를 제외하고 시트의 ID 값과 정확히 같아야 한다. 앱과 생성 스크립트가 같은 ID 우선순위를 사용한다.

```text
id_unit
id_ptn(no)
id_ptn
id_drill
id_rep
id_repertory
id_kalimat
id_expression
id_nass
```

예를 들어 `id_expression = exp_kayfa-l-hal`이면 파일명은 `exp_kayfa-l-hal.wav`가 된다. 현재 운영 기준은 “ID 값 = 파일명”이다. 지문의 경우 `id_nass`가 곧 파일명이다.

초기 데이터처럼 ID가 비어 있는 행을 위한 legacy fallback 규칙은 생성기와 앱에 남겨둘 수 있지만, 새 데이터에서는 ID가 비어 있으면 생성 전 시트를 먼저 보정한다.

## 5. 앱 적용 규칙

모든 앱은 현재 유닛 코드와 해당 행의 ID 값을 조합해 오디오 URL을 만든다. 파일 목록을 탐색하지 않고 직접 URL을 요청하므로, 스토리지 객체명이 규칙과 다르면 재생되지 않는다.

| 앱 | 사용자 동작 | 재생 기준 |
|---|---|---|
| 선생님용 앱 | 재생 버튼 또는 `S` 키 | 현재 슬라이드 행의 `U` + ID |
| 학생용 앱 | 재생 버튼 | 현재 슬라이드 행의 `U` + ID |
| 교재용 앱 | 아랍어 텍스트 클릭/탭 | 클릭한 행의 `U` + ID |

교재용 앱에서는 시각적 재생 버튼을 두지 않고, 아랍어 자체가 인터랙션 대상이다. 선생님용 앱에서는 슬라이드의 재생 버튼이 인터랙션 대상이다.

## 6. TTS/TSS 입력 텍스트 규칙

TTS에 보내는 텍스트는 앱에 보이는 텍스트와 완전히 같을 필요는 없다. 발음을 안정적으로 만들기 위해 TTS 전용 전처리를 적용한다. 시트에서 실제 발음 지시를 다시 써 둔 열은 `tss`이며, 이 값이 있으면 다른 컬럼보다 우선한다.

### 6.1 텍스트 선택 우선순위

생성 스크립트는 아래 순서로 TTS 입력 텍스트를 선택한다.

```text
tss -> tts -> tts_script -> tts_arabic -> arabic
```

`tss`는 앱 표시용 텍스트가 아니라 “이렇게 읽어라”를 지정하는 발음 스크립트다. `tss` 값이 실제 텍스트이면 그 값을 그대로 TTS 입력으로 사용한다. 값이 비어 있거나 `0`, `1`, `true`, `false` 같은 체크/플래그 값이면 발음 스크립트로 보지 않는다.

위 컬럼들이 없으면 기본적으로 `arabic` 컬럼을 사용한다. `script` 컬럼은 한국어 설명문인 경우가 많으므로 기본 TTS 입력으로 쓰지 않는다. 단, `script`에 아랍어가 있고 다른 입력 텍스트가 전혀 없을 때만 fallback으로 사용할 수 있다.

### 6.2 마크업 제거

시트에서 강조나 발음 표시용으로 쓰는 `*`, `_`는 TTS 전에 제거한다.

```text
بَنَ*يْ*تُ -> بَنَيْتُ
_ba_       -> ba
```

### 6.3 어말 수쿤 추가

ATA 표기 원칙상 명사의 마지막 격모음은 쓰지 않는다. 그러나 TTS는 끝 모음이 없는 단어를 불안정하게 읽을 수 있으므로, 단어 끝 아랍어 자음에 모음부호가 없으면 수쿤 `ْ`을 추가한다.

```text
السَّلَام -> السَّلَامْ
كَيْفَ الْحَال؟ -> كَيْفَ الْحَالْ؟
```

이미 파트하, 담마, 카스라, 탄윈, 수쿤이 있으면 추가하지 않는다. 샷다로 끝나는 경우에는 샷다 뒤에 수쿤을 추가할 수 있다.

### 6.4 TTS 예외 스크립트

몇몇 항목은 TTS가 장모음이나 특정 연결 발음을 잘못 읽을 수 있다. 이때는 생성 스크립트의 `PRONUNCIATION_OVERRIDES`에 ID별 예외를 등록한다.

```python
PRONUNCIATION_OVERRIDES = {
    "dri_example": "وَاادِي",
}
```

예외 스크립트는 앱 표시용 텍스트가 아니라 TTS 입력 전용이다.

### 6.5 나쓰 화자 성별 지정

`nass` 탭에는 화자 성별을 직접 지정하는 `speaker1`, `speaker2` 열을 둘 수 있다. 값은 `M`, `F`만 사용한다. 이 값이 있으면 생성 스크립트는 자동 추정이나 `SPEAKER_OVERRIDES`보다 시트 값을 먼저 따른다.

```text
speaker1 = F
speaker2 = M
```

예를 들어 첫 줄에서 여성이 `أَنَا سَارَة`처럼 말하는 지문은 `speaker1 = F`로 지정한다. 화자가 셋 이상 필요한 지문은 우선 지문 구조를 다시 검토하고, 꼭 필요할 때만 `speaker3` 같은 열을 추가한다.

### 6.6 타마르부타와 여성형 접미 발음 보정

타마르부타와 여성형 접미 발음은 앱 표시용 원문과 TTS 입력문을 분리해서 처리한다. 시트의 `arabic`에는 교재에 보일 정확한 표기를 유지하고, ElevenLabs가 어색하게 읽는 경우에만 `tss`에 발음 유도용 문장을 넣는다.

연결형의 첫 요소처럼 `ة` 뒤에 다음 단어가 이어지는 경우, TTS 입력에서는 `ة`를 쓰지 않고 앞 자음을 파트하로 읽게 만든다.

```text
دَقِيقَة وَاحِدَة -> دَقِيقَ وَاحِدَهْ
طَالْعَة الْحِين -> طَالْعَ الْحِين
نَازِلَة الْحِين -> نَازِلَ الْحِين
```

휴지나 문장 끝에서 타마르부타로 끝나는 말은 TTS 입력에서 `هْ`로 바꿔 닫아 읽게 할 수 있다.

```text
تَعْبَانَة -> تَعْبَانَهْ
جُوعَانَة -> جُوعَانَهْ
لَحْظَة -> لَحْظَهْ
```

여성에게 말하는 접미형이 짧게 끊겨 남성형처럼 들릴 때는 TTS 입력에서 마지막에 보조 `ي`를 붙여 여성형 발음을 유도한다. 이 보정도 앱 표시용 원문에는 넣지 않는다.

```text
لَكِ -> لَكِي
عَلَى مَهْلِك -> عَلَى مَهْلِكِي
```

## 7. 1과 테스트 생성 절차

1과만 먼저 확인할 때는 반드시 dry-run으로 대상과 TTS 입력문을 확인한 뒤 실제 생성한다.

```bash
cd "/Users/rasheedpark/Library/CloudStorage/GoogleDrive-someaugust17@gmail.com/공유 드라이브/마르카즈아라빅 팀 드라이브/제품products/ATA-14"
python3 archive/ata-audio-pipeline/generate_144_audio.py --dry-run --unit A01
```

출력에서 유닛 코드, ID, TTS 입력문이 맞으면 실제 생성한다.

```bash
python3 archive/ata-audio-pipeline/generate_144_audio.py --unit A01
```

GCS 업로드 없이 프로젝트 안의 `audio/{unit_code}/` 폴더에만 샘플을 만들 때는 아래처럼 실행한다.

```bash
python3 archive/ata-audio-pipeline/generate_144_audio.py --unit A01 --local-only --output-dir audio
```

특정 파일 하나만 재생성할 때는 `--id`와 `--overwrite`를 쓴다.

```bash
python3 archive/ata-audio-pipeline/generate_144_audio.py --id dri_banata --overwrite
```

`tss` 열에 발음 스크립트가 있는 항목만 다시 생성할 때는 `--only-tss`를 사용한다. 이 명령은 로컬 `audio/{unit_code}/` 폴더에 WAV를 저장하고, 동시에 GCS의 같은 경로에 업로드한다.

```bash
python3 archive/ata-audio-pipeline/generate_144_audio.py --unit A01 --only-tss --overwrite --output-dir audio
```

이 작업은 `tss` 값이 있는 행만 대상으로 하므로, 기존 전체 오디오를 다시 만들지 않고 수정된 발음 항목만 덮어쓴다.

### 7.2 나쓰 ElevenLabs 생성 절차

나쓰 오디오는 ElevenLabs API 키가 필요하다. API 키는 코드에 직접 쓰지 않고 `archive/ata-audio-pipeline/.env` 또는 환경변수의 `ELEVENLABS_API_KEY`로 관리한다.

먼저 누락 파일과 배정될 목소리를 dry-run으로 확인한다.

```bash
python3 archive/ata-audio-pipeline/generate_144_nass_elevenlabs.py --unit A14 --unit A15 --missing-only --dry-run
```

안전상 `--unit` 또는 `--id` 없이 전체 유닛을 자동 스캔하지 않는다. 전체 유닛을 대상으로 할 때는 실수 방지를 위해 `--all-units`를 명시해야 한다.

확인 후 실제 MP3를 생성하고 로컬 `audio/{unit_code}/`와 GCS에 동시에 저장한다.

```bash
python3 archive/ata-audio-pipeline/generate_144_nass_elevenlabs.py --unit A14 --unit A15 --missing-only
```

특정 지문 하나만 다시 만들 때는 `--id`와 `--overwrite`를 쓴다.

```bash
python3 archive/ata-audio-pipeline/generate_144_nass_elevenlabs.py --id nass_jib-li-qahwa --overwrite
```

## 8. 생성 후 확인

생성 후 앱에서 아래 방식으로 확인한다.

| 앱 | 확인 방법 |
|---|---|
| 선생님용 앱 | 해당 슬라이드에서 오디오 버튼 또는 `S` 키 |
| 학생용 앱 | 해당 슬라이드에서 오디오 버튼 |
| 교재용 앱 | 해당 아랍어 텍스트 클릭/탭 |

브라우저에서 직접 확인할 때는 아래 URL 형식을 사용한다.

```text
https://storage.googleapis.com/all-that-arabic-14/audio/A01/dri_banata.wav
```

## 9. 주의사항

- `audio/{unit_code}/`가 현재 앱의 실제 오디오 폴더 구조이다.
- 문서나 과거 메모에 있는 `listening144`, `listening(144)` 표기는 1.4.4 현재 운영 기준이 아니다.
- 파일명은 URL 인코딩되어 요청되지만, GCS 객체명 자체는 ID와 확장자를 그대로 사용한다.
- 같은 ID라도 유닛 폴더가 다르면 다른 오디오로 취급된다.
- API 키와 서비스 인증 정보는 코드에 직접 추가하지 말고 환경변수 또는 로컬 `.env`에서 관리한다.
