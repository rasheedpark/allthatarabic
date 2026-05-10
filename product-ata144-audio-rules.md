# ATA 1.4.4 듣기 파일 생성 규칙

이 문서는 ATA 1.4.4의 듣기 오디오 파일을 생성하고 앱에서 연결하는 기준을 정의한다. 기준 앱은 `app144.html`이며, 생성 스크립트는 `ata-audio-pipeline/generate_144_audio.py`이다.

## 1. 기본 원리

ATA 1.4.4 앱은 시트의 각 행에서 오디오 키를 만들고, Google Cloud Storage의 정해진 경로에서 파일을 직접 찾는다. 앱은 먼저 `.mp3`를 시도하고, 실패하면 `.wav`를 시도한다.

```text
https://storage.googleapis.com/all-that-arabic-14/listening144/{audio_key}.mp3
https://storage.googleapis.com/all-that-arabic-14/listening144/{audio_key}.wav
```

현재 생성 스크립트는 Google Cloud Text-to-Speech의 `ar-XA-Chirp3-HD-Aoede` 보이스를 사용해 WAV 파일을 만들고, `gs://all-that-arabic-14/listening144/`에 업로드한다.

## 2. 대상 데이터

듣기 파일 생성 대상은 아래 세 탭의 `status = confirmed` 행이다.

| 탭 | 대상 타입 | 설명 |
|---|---|---|
| `repertory` | `repertory`, `repertorie` | 패턴별 대표 예문과 발음 레퍼토리 |
| `drill` | `drillA`, `drillB`, `drillC` | 따라 읽기와 연습 문장 |
| `expression` | `exp` | 유닛별 표현 |

`pattern`, `units`, `kalimat`, `nass`는 현재 자동 생성 대상에 포함하지 않는다. 나스 오디오는 별도 운영 규칙으로 관리한다.

## 3. 오디오 키 산출 규칙

오디오 키는 파일명에서 확장자를 뺀 값이다. 앱과 생성 스크립트가 같은 규칙을 사용해야 한다.

### 3.1 명시 ID 우선

행에 아래 ID 컬럼이 있으면 그 값을 그대로 오디오 키로 사용한다.

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

예를 들어 `id_kalimat = exp_as-salāmu ʿalaykum`이면 파일명은 `exp_as-salāmu ʿalaykum.wav`가 된다.

### 3.2 ID가 비어 있을 때의 fallback

1.4.4 시트에는 초기 데이터처럼 ID가 비어 있고 `note`만 있는 행이 있다. 이 경우 아래 규칙으로 오디오 키를 만든다.

| 탭/타입 | 조건 | 오디오 키 |
|---|---|---|
| `repertory` | `note`가 `_ba_`, `_ta_`처럼 `_`로 시작하거나 `fatha`, `damma`인 경우 | `rep_{note}` |
| `repertory` | 그 외의 레퍼토리 예문 | `mit_{note}` |
| `drillA/B/C` | 모든 드릴 행 | `dri_{note}` |
| `exp` | ID가 비어 있는 표현 행 | `exp_{note}` |

예시는 다음과 같다.

```text
repertory note="_ba_"       -> rep__ba_.wav
repertory note="ba·ta·tha"  -> mit_ba·ta·tha.wav
drillA note="banata"        -> dri_banata.wav
drillA note="bana*y*tu"     -> dri_bana*y*tu.wav
expression note="kayfa..."  -> exp_kayfa....wav
```

## 4. TTS 입력 텍스트 규칙

TTS에 보내는 텍스트는 앱에 보이는 텍스트와 완전히 같을 필요는 없다. 발음을 안정적으로 만들기 위해 TTS 전용 전처리를 적용한다.

### 4.1 텍스트 선택 우선순위

생성 스크립트는 아래 순서로 TTS 입력 텍스트를 선택한다.

```text
tts -> tts_script -> tts_arabic -> arabic
```

위 컬럼들이 없으면 기본적으로 `arabic` 컬럼을 사용한다. `script` 컬럼은 한국어 설명문인 경우가 많으므로 기본 TTS 입력으로 쓰지 않는다. 단, `script`에 아랍어가 있고 다른 입력 텍스트가 전혀 없을 때만 fallback으로 사용할 수 있다.

### 4.2 마크업 제거

시트에서 강조나 발음 표시용으로 쓰는 `*`, `_`는 TTS 전에 제거한다.

```text
بَنَ*يْ*تُ -> بَنَيْتُ
_ba_       -> ba
```

### 4.3 어말 수쿤 추가

ATA 표기 원칙상 명사의 마지막 격모음은 쓰지 않는다. 그러나 TTS는 끝 모음이 없는 단어를 불안정하게 읽을 수 있으므로, 단어 끝 아랍어 자음에 모음부호가 없으면 수쿤 `ْ`을 추가한다.

```text
السَّلَام -> السَّلَامْ
كَيْفَ الْحَال؟ -> كَيْفَ الْحَالْ؟
```

이미 파트하, 담마, 카스라, 탄윈, 수쿤이 있으면 추가하지 않는다. 샷다로 끝나는 경우에는 샷다 뒤에 수쿤을 추가할 수 있다.

### 4.4 TTS 예외 스크립트

몇몇 항목은 TTS가 장모음이나 특정 연결 발음을 잘못 읽을 수 있다. 이때는 생성 스크립트의 `PRONUNCIATION_OVERRIDES`에 ID별 예외를 등록한다.

```python
PRONUNCIATION_OVERRIDES = {
    "dri_example": "وَاادِي",
}
```

예외 스크립트는 앱 표시용 텍스트가 아니라 TTS 입력 전용이다.

## 5. 1과 테스트 생성 절차

1과만 먼저 확인할 때는 반드시 dry-run으로 대상과 TTS 입력문을 확인한 뒤 실제 생성한다.

```bash
cd "/Users/rasheedpark/Library/CloudStorage/GoogleDrive-someaugust17@gmail.com/공유 드라이브/마르카즈아라빅 팀 드라이브/제품products/ATA-14"
python3 ata-audio-pipeline/generate_144_audio.py --dry-run --unit p1
```

출력에서 오디오 키와 TTS 입력문이 맞으면 실제 생성한다.

```bash
python3 ata-audio-pipeline/generate_144_audio.py --unit p1
```

GCS 업로드 없이 프로젝트 안의 별도 폴더에만 샘플을 만들 때는 아래처럼 실행한다. 1.4.4 시트의 1과 유닛 코드는 `A01`이며, 생성기는 `--unit 1`, `--unit p1`, `--unit A01`을 모두 `A01`로 처리한다.

```bash
python3 ata-audio-pipeline/generate_144_audio.py --unit 1 --local-only --output-dir audio144-unit1-sample
```

특정 파일 하나만 재생성할 때는 `--id`와 `--overwrite`를 쓴다.

```bash
python3 ata-audio-pipeline/generate_144_audio.py --id dri_banata --overwrite
```

## 6. 생성 후 확인

생성 후 앱에서 `S` 키 또는 오디오 버튼으로 확인한다. 앱은 같은 오디오 키에 대해 아래 순서로 요청한다.

```text
{audio_key}.mp3
{audio_key}.wav
```

현재 자동 생성기는 WAV를 올리므로, 기존 MP3가 없는 경우 두 번째 요청에서 재생된다. 기존 MP3가 이미 있으면 앱은 MP3를 먼저 재생한다.

브라우저에서 직접 확인할 때는 아래 URL 형식을 사용한다.

```text
https://storage.googleapis.com/all-that-arabic-14/listening144/dri_banata.wav
```

## 7. 주의사항

- `listening144`가 현재 앱의 실제 오디오 폴더명이다.
- 문서나 과거 메모에 있는 `listening(144)` 표기는 현재 앱 기준과 다르므로 새 파일 생성에는 사용하지 않는다.
- 파일명은 URL 인코딩되어 요청되지만, GCS 객체명 자체는 오디오 키와 확장자를 그대로 사용한다.
- `note` 기반 fallback 파일명에는 `*`, `·`, `ā`, `ʿ` 같은 문자가 포함될 수 있다. 현재 앱과 생성기는 이 값을 그대로 사용한다.
- API 키와 서비스 인증 정보는 코드에 직접 추가하지 말고 환경변수 또는 로컬 `.env`에서 관리한다.
