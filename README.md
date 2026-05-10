# 올댓아라빅 (All That Arabic) — v1.4.4

마르카즈아라빅 아랍어 교육 콘텐츠. 선생님용·학생용·교재용 모바일 앱.

## 디렉토리 구조

```
allthatarabic/
├── index.html                       랜딩 (3개 앱 링크)
├── ata144_teacher/index.html        선생님용 (수업 슬라이드)
├── ata144_student/index.html        학생용 (모바일 복습)
├── ata144_textbook/index.html       교재용 모바일 앱 (실험)
├── app144.html, app144s.html        옛 URL → 새 URL redirect
├── assets/                          공유 자산 (로고, 폰트, 국기 아이콘)
├── product-ata144.md                제품 문서 (메인)
├── product-ata144-appendix.md       CSS 부록
├── product-ata144-audio-rules.md    오디오 생성 규칙
├── product-ata144-image-rules.md    이미지 생성 규칙
├── product-ata144-design(mobile).md 모바일 앱 실험 기록
├── product-ata143.md                옛 1.4.3 문서 (참고)
└── archive/                         옛 버전 (143, app, slides)
```

## 배포 URL

- 랜딩: https://rasheedpark.github.io/allthatarabic/
- 선생님용: https://rasheedpark.github.io/allthatarabic/ata144_teacher/
- 학생용: https://rasheedpark.github.io/allthatarabic/ata144_student/
- 교재용 모바일: https://rasheedpark.github.io/allthatarabic/ata144_textbook/

## 데이터 소스

- Google Sheets: `1w7e0mLLgFhzU7Ixs6CUfzgrwUG6EEy8jHijXF5UJwY8`
- 오디오: `gs://all-that-arabic-14/listening144/`

## 작업/배포 워크플로

| 브랜치 | 역할 |
|---|---|
| `main` | **배포** — GitHub Pages가 서빙. 학생/선생님이 보는 화면. |
| `dev`  | **작업** — 일상 작업 모두 여기서. 학생/선생님은 영향 없음. |

### 일상 작업

```bash
git checkout dev          # 한 번만, 이후 dev 유지
# 파일 수정
git add .
git commit -m "메시지"
git push origin dev       # GitHub에 백업 (배포 X)
```

### 배포 (dev → main)

```bash
git checkout main
git merge dev
git push origin main      # → 1~2분 내 GitHub Pages 자동 갱신
git checkout dev          # 다시 작업 모드로 복귀
```

### 롤백

```bash
git checkout main
git revert HEAD
git push origin main
```

자세한 워크플로 설명은 `product-ata144.md` 참고.
