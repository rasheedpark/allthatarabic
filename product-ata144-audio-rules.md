# ATA 1.4.4 듣기 파일 생성 및 적용 규칙

이 문서는 ATA 1.4.4의 듣기 오디오 파일을 생성하고 앱에서 연결하는 기준을 정의한다. 기준 앱은 `ata144_teacher/ata144_teacher.html`, `ata144_student/ata144_student.html`, `textbook144m.html`, `ata144_textbook/ata144_textbook.html`이며, 생성 스크립트는 `archive/ata-audio-pipeline/generate_144_audio.py`이다.

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

현재 생성 스크립트는 Google Cloud Text-to-Speech의 `ar-XA-Chirp3-HD-Aoede` 보이스를 사용해 WAV 파일을 만들고, `gs://all-that-arabic-14/audio/{unit_code}/`에 업로드한다.

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

`units`, `kalimat`, `nass`는 현재 자동 생성 대상에 포함하지 않는다. 나스 오디오는 별도 운영 규칙이 확정되면 추가한다.

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

예를 들어 `id_expression = exp_kayfa-l-hal`이면 파일명은 `exp_kayfa-l-hal.wav`가 된다. 현재 운영 기준은 “ID 값 = 파일명”이다.

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
