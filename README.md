# Promptmiss

**My Prompt Promise**

---

## 📌 프로젝트 소개
GPT 프롬프트를 저장하고 공유하며 실행할 수 있는 커뮤니티형 웹 서비스입니다.

---

## 🛠 기술 스택
- **Backend**: Django, Django REST Framework
- **Frontend**: Vue 3, Vite
- **Database**: SQLite (추후 PostgreSQL 전환 가능)

---

## 📁 폴더 구조
```
promptmiss/
├── backend/        # Django API 서버
├── frontend/       # Vue 앱 (Vite 기반)
├── .gitignore
└── README.md
```

---

## ✅ 현재 완료된 작업 (2025.05.19 기준, 최신 반영 완료)

### 1. Django 백엔드 초기 세팅
- 프로젝트명: `config`
- 앱명: `prompts`, `accounts`
- `rest_framework`, `corsheaders`, `prompts`, `accounts` 등 앱 등록
- `.gitignore`에 venv, pycache, DS_Store 등 추가

### 2. 모델 설계
- Prompt 모델: user(FK), title, content, created_at
- Execution 모델: prompt(FK), user_input, result, executed_at
- Tag 모델, PromptTag 중간 테이블을 통해 N:M 구현
- Comment 모델: user(FK), prompt(FK), content, created_at, likes(M:M)
- 좋아요/북마크용 중간 테이블 (PromptLike, PromptBookmark) 별도 구현

### 3. API 개발
- PromptSerializer에서 댓글, 실행 이력 포함 응답
- 사용자 인증 기반 Prompt 생성 (`request.user`)
- 전체 Prompt 목록 조회 (비로그인 가능, 필터링 지원)
- 내 프롬프트만 조회 (`/api/prompts/?mine=true`)
- 좋아요/북마크 기능 (`/api/prompts/<id>/like/`, `/bookmark/`)
- 댓글 좋아요 기능 (`/comments/<id>/like/`)
- 실행 API (`/api/prompts/<id>/execute/`) 구현 및 결과 저장

### 4. 사용자 인증
- JWT 기반 인증 구현 (access + refresh 토큰)
- 로그인/회원가입/내 정보 API 구현
- 인증 사용자만 Prompt/Comment 생성 및 수정 가능
- 본인 외 접근 시 `PermissionDenied` 처리

### 5. 댓글 기능
- `/api/comments/`로 CRUD API 구현 (ModelViewSet)
- Prompt 상세 조회 시 댓글 리스트 포함
- 댓글 좋아요 수 및 상태 포함 응답
- 댓글 수정/삭제는 작성자 본인만 가능 (`IsOwnerOrReadOnly`)

### 6. 프롬프트 수정/삭제 및 권한 처리
- 프롬프트 수정/삭제 API 구현
- PromptSerializer 사용자 필드 구조 정리 (ID + username 응답)
- 사용자 정보 API(`/api/users/me/`) 구현

### 7. 프론트엔드 기능 연동 (Vue)
- PromptListView, PromptDetailView, PromptCreateView, PromptUpdateView 등 페이지 구현
- Tailwind 기반 스타일 통일 (생성/수정/상세)
- 사용자 정보 localStorage 연동 및 권한 확인
- 댓글 입력, 수정, 삭제 구현
- prompt 및 comment 작성자 본인만 수정/삭제 가능
- 실행 결과 출력 + 로딩 처리 구현

### 8. 좋아요 및 북마크 기능 개선
- PromptSerializer에 is_liked, is_bookmarked 필드 추가
- 각 프롬프트에 대해 현재 로그인 사용자의 좋아요/북마크 여부를 응답에 포함
- PromptListView 및 PromptDetailView에서 하드코딩된 좋아요/북마크 컴포넌트 제거
- 상태 관리는 전적으로 백엔드 응답을 기반으로 렌더링
- 좋아요/북마크 토글 시 서버 응답을 바탕으로 Vue reactivity 정상 반영되도록 개선
- 댓글에도 동일한 방식으로 좋아요 상태 렌더링 반영

### 9. 좋아요/북마크 전반 리팩토링
- LikeButton.vue, BookmarkButton.vue 제거 및 컴포넌트 의존성 축소
- 좋아요 및 북마크 UI를 모두 서버 응답 기반 렌더링으로 통일
- `prompt.is_liked`, `prompt.bookmark_count` 등을 기반으로 Vue 템플릿에서 직접 처리
- 댓글 좋아요 로직도 동일하게 서버 기반 `is_liked`, `like_count` 구조로 리팩토링
- Vue 반응성 문제 해결: `prompt.value = {...}` 대신 배열 교체 또는 `splice` 구조 적용
- 전체 좋아요/북마크 기능의 백엔드 일관성 확보 및 프론트 간결화

---

## 🧭 다음 작업 예정
- GPT API 호출 연동 (프롬프트 실행 결과 자동 생성)