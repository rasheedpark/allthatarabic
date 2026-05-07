> **현재 초안 (Draft)** — 이 문서는 작성 중이며 내용이 변경될 수 있습니다.

# 올댓아라빅 All That Arabic 1.4.4
---

### 이론적 배경 Theoretical Background

| 방식 | 이름 | 핵심 접근 | 도구 |
|---|---|---|---|
| 1방식 | 구조화 structural | 문장 성분 → 트리구조 → 논리적 이해 | 문법맵핑, 연습문제, 작문 |
| 2방식 | 행동주의 behaviorism | 현지에서 배우듯, 모국어 습득하듯 | 스토리텔링, 연상, 토론, 활동 |
| **3방식** | **인지주의 cognitivism** | **패턴을 '습득'한 후 어휘를 바꿔가며 유추해 '말하게' 유도** | **패턴드릴, 단편말하기, 유추, 훈련** |
| 4방식 | 완전한 개인화 customized | 커리큘럼 불필요 | consulting 외 교육 도구 불필요 |

1방식은 언어를 규칙의 조합으로 보고 문장을 분해하여 이해시킨다. 논리적으로 정교하지만, 실제 발화 상황에서 학습자는 이 규칙들을 실시간으로 조립할 여유가 없다. 언어에 대한 지식은 생기지만 언어를 사용하는 능력은 만들어지지 않는다. 2방식은 어린아이가 모국어를 배우듯 풍부한 맥락과 대량 노출을 통해 포괄적인 방법으로 언어를 익히게 한다. 현지 몰입 환경에서는 강력하지만, 하루에 제한적인 시간만 외국어 학습에 할애하는 성인에게는 비현실적이다. 성인의 뇌는 이미 모국어에 최적화되어 있어, 짧은 노출만으로 언어 규칙을 스스로 유추하고 내재화하기 어렵다.

**제품의 목적은 아랍어 교육에 3방식을 도입하는 것이다**. 자주 쓰이는 아랍어 구문을 분석하지 않고 하나의 덩어리로 인식시킨 뒤, 그 패턴 안에서 어휘를 바꿔가며 반복해서 말하게 한다. 제한된 학습 시간 안에 언어를 각인시키려면 넓고 얕은 노출보다 좁고 깊게 패턴을 타격하는 훈련이 효율적이다. 패턴이 입에 붙으면 새 패턴이 이전 패턴과 결합되고, 이 결합이 반복될수록 더 긴 문장을 자동적으로 말할 수 있게 된다. 해석하는 것이 아니라 말하는 것이 목표다.

3방식이 완성되면 4방식으로의 이행이 가능해진다. 패턴과 어휘의 데이터베이스가 충분히 쌓이고 학습자의 특성과 취약점이 파악될 때, 정해진 커리큘럼 없이 학습자 개인에게 최적화된 패턴과 드릴을 실시간으로 제공할 수 있다. 올댓아라빅이 지금 구축하고 있는 모듈화된 콘텐츠 구조는 그 전환을 위한 기반이다.


### 원칙tenet
올댓아라빅은 아랍어의 어형(sarf)과 구문(nahw)을 패턴화하고, 학습자가 이를 하나의 덩어리(chunk)로 인식한 뒤 직접 말하는 것을 통해 자연스럽게 체득하도록 디자인하고 있다. 인지 부담을 최소화하고, 배운 패턴에 어휘를 바꿔 넣어 스스로 문장을 만들고 말할 수 있게 되는 것이 핵심 목표다.

핵심원칙은 1. 핵심 내용을 학습자가 바로 인지 할 수 있어야하며 2. 실제 아랍인들이 쓰는 표현만 다루며(교재에만 있는 말은 쓰지 않는다) 3. 패턴·어휘·예문·지문 등 구조화된 데이터베이스로 구축되어야 하며 이렇게 모듈화된 데이터 포맷은 4방식 개인화로 업데이트 하는 기반이 된다. 아울러 4. 빠르고 저비용으로 제작해 제한된 시간 안에 시제품 제작 - 제품검증 - 피드백 루프를 만들 수 있게 생산성이 담보되어야 한다.

- **패턴pattern**, 사용자가 보는 즉시 인지하고 바로 '말하기'를 할 수 있어야 한다. 설명은 패턴을 이해하는 데 필요한 최소한으로만 한다.
- **드릴drill**, 배운 패턴을 사용자가 말하기 위한 것이다. 아랍어 문장을 한국어로 해석하거나 번역하는 방식을 배제한다. 배웠던 패턴에 어휘를 바꿔 반복해서 말하도록 유도한다.
- **표현expression**, 빈출 어휘와 표현 중 패턴으로 정형화하기 어렵거나, 패턴으로 다룰 수 있어도 지금 당장 빠르게 익혀야 하는 것들을 따로 다룬다.
- **유추inference**, 배운 패턴을 스스로 떠올리고 적용할 수 있는 다양한 문제를 제공한다. 맥락 안에서 스스로 생각하고 말하게 유도하는 것이 목적이며, 이 과정이 실질적인 언어 운용 능력을 만든다.
- **단어kalimat**, 빈출 순으로 우선 선정하되, 패턴을 설명하기 좋은 단어를 먼저 고르고, 지문(nass) 구성에 필요한 단어를 추가로 보충한다.
- **내러티브narrative**, 선생님의 재량 영역으로 제품과 강의를 보다 유연하게 만들고, 아랍어·아랍인·아랍 문화에 대한 언어적·문화적 배경지식을 제공하는 이야깃거리를 선정해 활용한다.


> ⚠️ **드릴·표현·지문 제작 원칙**
> 드릴, 표현, 유추활동을 위한 지문을 만들 때는 반드시 **실제 아랍인들이 쓰는 자연스러운(طَبِيعِيّ, ṭabīʕī)** 문장이어야 한다. 아직 배우지 않은 패턴과 어휘(kalimat)가 포함되어서는 안 된다.
> 단, **해당 유닛에서 새로 도입되는 kalimat와 expression은 활용 가능**하다.

### 구조structure

1.4.4 데이터시트에는 패턴·레퍼토리·드릴·표현·지문·어휘·내러티브가 입력되며, 이 데이터를 기반으로 앱과 콘텐츠가 만들어진다. 선생님용 앱은 온라인/오프라인 수업 현장에서 선생님이 직접 조작하며 수업을 진행하는 도구이며 학생용 앱은 사용자가 접속해 배운 패턴을 반복 연습하는 용도로 쓴다(이후 말하기가 가능한 형태로 업데이트). 콘텐츠는 세 종류로 다르스는 패턴·드릴 데이터를 기반으로 제작하는 녹화 강의다. 칼럼은 표현 데이터를 활용한 유튜브 콘텐츠로, 표현 하나를 중심으로 파생 표현과 예문을 묶어 전달한다. 깔람은 내러티브 데이터를 기반으로 아랍어·아랍인·아랍 문화를 주제로 한 콘텐츠로 구성될 예정이다.

- 데이터시트datasheet(1.4.4)
	- 앱application
		- 선생님용 앱(app_teacher)
		- 사용자용 앱(app_user)
	- 콘텐츠contents
		- 다르쓰darss
		- 칼람kalam
		- 깔람qalam

**데이터시트 구조상 표시되는 열을 다음과 같이 정의한다.**

- **C** — 챕터명. 각 챕터는 하나의 공통 테마를 공유하며, 정규수업 기준 한 챕터가 1개월(8회 수업)을 구성하는 것을 가정한다.
- **U** — 유닛 번호. 한 유닛은 하나의 대표 패턴을 가지며, 여기에 따라올 수 있는 2–4개의 서브패턴을 포함할 수 있다.
- **arabic** — 해당 양식(패턴·드릴·표현·지문·어휘 등)에 따라 사용자가 배울 핵심 내용을 표시한다. 앱에 노출되며 가릴 수 있다.
- **korean** — arabic을 부연하는 한국어 의미. 앱에 노출되며 가릴 수 있다.
- **transliteration** — 아랍어 발음을 로마자로 표기한 음가. 앱에 노출되며 가릴 수 있다. 코드 내 고유식별자(id) 구성에도 사용된다.
- **type** — 해당 데이터의 성격을 정의한다. 후술한다.
- **status** — 해당 데이터의 작업 상태를 나타낸다. 앱에는 confirmed 상태의 데이터만 노출된다.
- **id** — 해당 데이터의 고유 식별자. 타입별로 산출 규칙이 다르며 후술한다.
- **lahja** — 지역(방언) 코드. 기본값은 MSA이며 내용에 따라 구별된다.
- **script** — 레퍼토리 고유의 표준화된 설명 방식.
- **css** — 앱에 노출되는 데이터의 고유 표시 양식을 지정한다.
- **url** — 해당 데이터 파일의 위치. 앱과 연동된다.
- **중복** — 데이터의 활용 빈도를 추적한다.

<svg viewBox="0 0 760 430" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:760px;" font-family="'Apple SD Gothic Neo','Noto Sans KR',sans-serif;">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#333"/>
    </marker>
    <marker id="arr-d" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#888"/>
    </marker>
  </defs>
  <rect x="218" y="30" width="272" height="200" rx="8" fill="white" stroke="#333" stroke-width="1.5"/>
  <text x="354" y="56" text-anchor="middle" font-size="13" font-weight="700" fill="#111">데이터시트</text>
  <line x1="232" y1="64" x2="476" y2="64" stroke="#bbb" stroke-width="1"/>
  <rect x="232" y="74" width="120" height="28" rx="4" fill="white" stroke="#bbb" stroke-width="1"/>
  <text x="292" y="93" text-anchor="middle" font-size="11" fill="#333">패턴</text>
  <rect x="362" y="74" width="116" height="28" rx="4" fill="white" stroke="#bbb" stroke-width="1"/>
  <text x="420" y="93" text-anchor="middle" font-size="11" fill="#333">드릴</text>
  <rect x="232" y="112" width="120" height="28" rx="4" fill="white" stroke="#bbb" stroke-width="1"/>
  <text x="292" y="131" text-anchor="middle" font-size="11" fill="#333">레퍼토리</text>
  <rect x="362" y="112" width="116" height="28" rx="4" fill="white" stroke="#bbb" stroke-width="1"/>
  <text x="420" y="131" text-anchor="middle" font-size="11" fill="#333">어휘 / 표현</text>
  <rect x="232" y="150" width="120" height="28" rx="4" fill="white" stroke="#bbb" stroke-width="1"/>
  <text x="292" y="169" text-anchor="middle" font-size="11" fill="#333">지문</text>
  <rect x="362" y="150" width="116" height="28" rx="4" fill="white" stroke="#bbb" stroke-width="1"/>
  <text x="420" y="169" text-anchor="middle" font-size="11" fill="#333">내러티브</text>
  <text x="105" y="26" text-anchor="middle" font-size="11" fill="#555">앱</text>
  <rect x="15" y="35" width="185" height="68" rx="6" fill="white" stroke="#333" stroke-width="1.5"/>
  <text x="107" y="57" text-anchor="middle" font-size="12" font-weight="700" fill="#111">선생님용 앱</text>
  <text x="107" y="74" text-anchor="middle" font-size="10" fill="#444">온라인 / 오프라인 수업</text>
  <text x="107" y="90" text-anchor="middle" font-size="10" fill="#444">선생님이 직접 조작</text>
  <rect x="15" y="120" width="185" height="68" rx="6" fill="white" stroke="#333" stroke-width="1.5"/>
  <text x="107" y="142" text-anchor="middle" font-size="12" font-weight="700" fill="#111">사용자용 앱</text>
  <text x="107" y="159" text-anchor="middle" font-size="10" fill="#444">배운 패턴 반복 연습</text>
  <text x="107" y="175" text-anchor="middle" font-size="10" fill="#444">말하기 기능 추가 예정</text>
  <line x1="218" y1="88" x2="202" y2="78" stroke="#333" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="218" y1="145" x2="202" y2="154" stroke="#333" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="625" y="26" text-anchor="middle" font-size="11" fill="#555">콘텐츠</text>
  <rect x="530" y="35" width="185" height="68" rx="6" fill="white" stroke="#333" stroke-width="1.5"/>
  <text x="622" y="57" text-anchor="middle" font-size="12" font-weight="700" fill="#111">다르스</text>
  <text x="622" y="74" text-anchor="middle" font-size="10" fill="#444">녹화 강의</text>
  <text x="622" y="90" text-anchor="middle" font-size="10" fill="#444">패턴 · 드릴 기반</text>
  <rect x="530" y="120" width="185" height="68" rx="6" fill="white" stroke="#333" stroke-width="1.5"/>
  <text x="622" y="142" text-anchor="middle" font-size="12" font-weight="700" fill="#111">칼람</text>
  <text x="622" y="159" text-anchor="middle" font-size="10" fill="#444">유튜브 콘텐츠</text>
  <text x="622" y="175" text-anchor="middle" font-size="10" fill="#444">표현 + 파생표현 · 예문</text>
  <rect x="530" y="205" width="185" height="68" rx="6" fill="white" stroke="#333" stroke-width="1.5"/>
  <text x="622" y="227" text-anchor="middle" font-size="12" font-weight="700" fill="#111">깔람</text>
  <text x="622" y="244" text-anchor="middle" font-size="10" fill="#444">유튜브 콘텐츠</text>
  <text x="622" y="260" text-anchor="middle" font-size="10" fill="#444">아랍어 · 문화 내러티브</text>
  <line x1="490" y1="88" x2="528" y2="69" stroke="#333" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="490" y1="126" x2="528" y2="154" stroke="#333" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="490" y1="164" x2="528" y2="239" stroke="#333" stroke-width="1.2" marker-end="url(#arr)"/>
  <line x1="715" y1="69"  x2="730" y2="69"  stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="715" y1="154" x2="730" y2="154" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="715" y1="239" x2="730" y2="239" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <line x1="730" y1="69"  x2="730" y2="239" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
  <polyline points="730,154 750,154 750,380 107,380 107,190" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="4,3" marker-end="url(#arr-d)"/>
  <rect x="305" y="371" width="175" height="18" rx="6" fill="white" stroke="#bbb" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="392" y="384" text-anchor="middle" font-size="9" fill="#888">콘텐츠 → 사용자용 앱 통합 예정</text>
</svg>

### 타입type
type은 해당 데이터의 성격을 정의한다.

- **unit** — 유닛의 타이틀 역할을 한다. 해당 유닛의 대표 패턴을 보여주며, 앱에서 유닛 구분자로 표시된다.

- **ptn** — 사용자가 말하기로 배워야 할 핵심 패턴이다. 아랍어를 패턴화해 발화를 통한 학습을 지향하는 이 방법론의 핵심 내용이다. `no_ptn`(순서값)과 `id_ptn`(고유식별자)으로 식별된다. 추후 ptnA(핵심 패턴)·ptnB(서브 패턴)으로 세분화할 예정이며, 1.4.4에서는 **ptn**으로 통일한다.

- **repertory** — 패턴 설명 시 함께 제시되는 예시이다. 항상 해당 패턴 직후에 붙어 나오며, ref값으로 패턴과 연결된다. `id_rep` = 유닛코드 + `_rep_` + note. 패턴이 노출될 때 레퍼토리도 함께 표시된다. 유닛 연결 외에 패턴과도 연결할지는 추후 결정한다.

- **drill** — 핵심 패턴을 말하기로 연습하기 위한 예문들이다. `id_drill` = 유닛코드 + `_drill_` + note. 기본적으로 유닛과 연결되며, 해당 유닛에 나온 패턴들이 골고루 포함되어야 한다. 패턴과의 직접 연결 여부는 추후 결정한다.

	  - **drillA** — 핵심예문. 앱에서 **drill**로 노출. 해당 유닛의 모든 패턴·레퍼토리 종료 후 일괄 표시. darss 콘텐츠 미포함. 교재 연습문제 "읽기/따라읽기" 섹션에 배치.
	  - **drillB** — 추가예문. 앱에서 **practice**로 노출. nass 이후에 표시. `{{...}}`로 감싼 부분은 앱과 교재 모두에서 빈칸으로 처리되어 학습자가 직접 유추하는 연습문제로 활용된다.
	  - **drillC** — 부가예문. `{{...}}`로 감싼 부분은 빈칸 처리되는 것은 동일하나, 앱과 교재 모두에 노출되지 않는다. 추후 별도 용도로 활용 예정.

- **exp** — 패턴으로 정규화하기 어려운 빈출 표현이다. 유닛과의 연관성을 권장하나 자유롭게 지정 가능하다. `id_exp` = 유닛코드 + `_exp_` + note. 앱에서 drillA 이후에 노출된다.

- **nass** — 해당 유닛의 패턴과 표현을 조합한 지문이다. `id_nass` = 유닛코드 + `_nass_` + note. 기본 형태는 따라하기로 시작하며, 수알(سؤال)이 포함된 경우 올말맞추기가 메인 활동이 된다. 앱과 교재 모두에 노출된다.

	- **nass+** — 예비용 지문이다. nass와 동일한 형식으로 작성되며, 추후 레벨테스트 등에 활용된다. 앱과 교재에는 노출되지 않는다.

- **kalimat** — 유닛별 사용 어휘를 제한하는 단어 목록이다. 앱에서 가장 마지막에 노출되며 유닛별 단어장으로 제공된다.

> **id 산출 규칙** (변경됨): 모든 타입에서 `유닛코드_type_note` 형식을 따른다.
> - `id_drill` = `{u}_drill_{note}` (예: `A01_drill_bana·ta`)
> - `id_rep` = `{u}_rep_{note}` (예: `A01_rep_bana·ta`)
> - `id_exp` = `{u}_exp_{note}` (예: `A01_exp_ṣabāḥ-al-khayr`)
> - `id_nass` = `{u}_nass_{note}` (예: `A01_nass_al-usra`)
>
> 시트 수식: `=U열셀&"_drill_"&note열셀` (각 탭 type명에 맞게 변경)

#### 상태값 Status

제품 제작에 있어 모든 데이터의 상태값(status)을 다음과 같이 정의한다.

- **inbox** — 검토 전 단계. 아이디어나 내용을 일단 기록해둔 상태.
- **draft** — 초기 작성 단계. 내용이 갖춰지기 시작한 상태.
- **hold** — 보류. 작업을 일시 중단하거나 판단을 미룬 상태.
- **confirmed** — 확정. 앱과 교재에 반영된다.

#### 시트 탭 구조 (1.4.4)

| 탭 | 역할 | 비고 |
|---|---|---|
| **유닛탭** | 각 유닛의 대표 정보 | 기존 패턴탭에서 이름 변경 |
| **패턴탭** | 각 패턴의 no_ptn·id_ptn 및 상세 내용 | 신설 |
| **드릴탭** | drillA·drillB·drillC 데이터, 패턴과 연결 | 기존 탭 구조 수정 |
| **표현탭** | exp 데이터 | 신설, kalimat탭과 분리 |
| **칼리마트탭** | kalimat 단어 목록 | 기존 유지 |
| **나스탭** | nass 지문 데이터 | 기존 유지 |


### 사용자용 앱 User App (app144s)

`app144s.html`은 학습자가 배운 패턴을 자율적으로 복습하기 위한 모바일 최적화 앱이다. 선생님용 앱(`app144.html`)과 같은 데이터시트를 공유하지만 표시 방식과 구성이 다르다.

**선생님용 앱과의 차이점**

| 항목 | 선생님용 (app144) | 사용자용 (app144s) |
|---|---|---|
| 화면 최적화 | 가로 대형 (TV·모니터) | 모바일 세로 (최대 640px) |
| 이동 방식 | 키보드 ← → | 스와이프 (좌우) + 하단 버튼 |
| 레퍼토리 | 노출 | **생략** |
| ptn 슬라이드 | arabic + korean + note | arabic + **summary** 컬럼 (설명 텍스트) |
| 미쌀(mithāl) | 레퍼토리와 동일 양식 | 동일 양식으로 표시 |
| 노출 타입 | ptn, repertory, mithāl, drillA, exp, kalimat, nass | ptn, mithāl, drillA, exp, kalimat, nass |
| 레이아웃 | position: fixed 4코너 | flex column, 100dvh, max-width 640px |

**노출 타입 (SHOW_TYPES)**

사용자용 앱에서 표시되는 타입: `ptn`, `mithal`, `drilla`, `exp`, `kalimat`, `nass`

레퍼토리(`repertory`)는 사용자용 앱에서 제외된다. 나머지 로직(status=confirmed 필터, 유닛 순서, 나스 포함)은 선생님용 앱과 동일하다.

**ptn 슬라이드 렌더링**

ptn 타입은 드릴탭의 `summary` 컬럼 내용을 설명 영역으로 표시한다. summary가 없을 경우 `scriptA` 컬럼을 대신 사용한다.

- 아랍어(`arabic`)가 있으면 상단에 작게 표시
- summary/scriptA 텍스트를 줄 단위로 파싱:
  - `- `로 시작하는 줄 → 불릿 항목 (점 + 텍스트)
  - 일반 줄 → 산문(prose) 단락
- 줄바꿈과 인라인 스타일(`**bold**`, `*italic*`, `[[arabic]]` 등) 지원

**모바일 레이아웃**

```
.app {
  display: flex; flex-direction: column;
  height: 100dvh; max-width: 640px;
  margin: 0 auto; background: var(--surface);
}
```

태블릿/데스크탑(660px 이상)에서는 상하 28px 여백과 border-radius를 추가해 카드형 레이아웃으로 표시된다.

**스와이프 제스처**

터치 시작(`touchstart`)과 종료(`touchend`) 좌표 차이로 슬라이드 이동을 감지한다.
- 수평 이동 42px 이상이고 수직 이동의 1.5배 이상이면 슬라이드 이동
- 왼쪽 스와이프 → 다음 슬라이드 / 오른쪽 스와이프 → 이전 슬라이드

**로딩 화면**

선생님용 앱과 동일: `--accent`(#1D49FF) 배경, 중앙 흰색 로고, 하단 `markazarabic 1.4.4 beta` 레이블.

**첫 방문 온보딩**

`localStorage` 플래그(`ata144s_onboarded`)로 첫 방문 여부를 확인한다. 첫 방문 시 조작법 안내 화면이 표시되며, 이후 방문 시 건너뛴다.

**주요 컴포넌트 (사용자용 앱)**

- **상단 바** — 유닛·슬라이드 번호 표시, 해석 토글 버튼
- **슬라이드 카드** — 스크롤 가능, 중앙 정렬, 하단 스와이프 힌트
- **하단 버튼** — 이전(`‹`) / 다음(`›`) 이동 버튼
- **사이드바** — 유닛 인덱스, 선생님용 앱과 동일한 구조
- **해석 토글** — 한국어·노트 텍스트 가리기/보기

---

### 참고References

#### 구글시트 인증 관련

Google Sheets API를 Claude가 직접 읽고 쓰기 위해 아래 방식으로 인증을 설정했다.

- **인증 방식**: `gcloud auth login --enable-gdrive-access`
  - 서비스 계정 키 없이 사용자 계정으로 직접 인증
  - 조직 정책(`iam.disableServiceAccountKeyCreation`)으로 서비스 계정 키 생성이 차단되어 있어 이 방식 채택
- **토큰 발급**: `gcloud auth print-access-token`으로 매 호출 시 토큰 사용
- **API 엔드포인트**: `https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{range}`
- **헬퍼 스크립트**: `~/.claude/sheets_helper.sh`

**관련 리소스**
- 1.4.4 스프레드시트: https://docs.google.com/spreadsheets/d/1w7e0mLLgFhzU7Ixs6CUfzgrwUG6EEy8jHijXF5UJwY8
- Google Sheets API 문서: https://developers.google.com/sheets/api/reference/rest
- Google Cloud Console: https://console.cloud.google.com

---

### 앱 표시 로직 App Display Logic

**데이터 노출 기준**
선생님용 앱은 유닛별로 묶어 순서대로 표시하며, `status = confirmed`인 데이터만 노출된다. 화면 상단에 해당 행의 `type` 값이 작게 표시된다. 기본 화면 양식은 1.4.3과 동일하다.

**오디오 재생 로직**
앱은 시트의 `url` 컬럼을 사용하지 않는다. 대신 행의 `key` 값으로 URL을 직접 조합한다.

```
https://storage.googleapis.com/all-that-arabic-14/listening(144)/{key}.mp3
```

실패 시 `.wav`로 폴백. key가 곧 파일명이므로 파일 목록 탐색 없이 바로 요청하여 로딩 지연이 없다. 오디오 파일은 `listening(144)/` 폴더에 보관한다.

> **1.4.3 → 1.4.4 변경점**: 오디오 폴더가 `listening/` → `listening(144)/`로 변경됨. URL 구성 기준이 `id_datasheet` → `key`로 바뀜.

