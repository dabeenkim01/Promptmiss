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

## ✅ 현재 완료된 작업 (2025.05.22 기준, 최신 반영 완료)

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
- 댓글 수정/삭제는 작성자 본인만 가능 (Vue에서 로그인 사용자 ID 비교로 제어)
- 대댓글 기능 구현 (parent 필드를 활용한 계층 구조)
- 대댓글은 하나의 댓글 아래로만 단일 깊이로 렌더링
- 대댓글 상태는 `replies` 배열로 응답되며, 작성, 좋아요, 삭제까지 모두 지원

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

### 10. 프론트엔드 로직 개선 및 상태 관리 일원화
- PromptListView.vue에서 axios 직접 호출 제거, 상태 관리를 전적으로 Pinia store로 통합
- prompt store에 `toggleLike`, `toggleBookmark`, `handleLike`, `handleBookmark` 추가
- 좋아요/북마크 토글 시 실시간 UI 반영 (카운트 업데이트 및 목록에서 조건 제거)
- HomeView.vue도 store 기반으로 실시간 인기 프롬프트 렌더링 및 상호작용 구현
- 각 뷰에서 중복 로직 제거 및 UI 단순화

### 11. 프론트엔드 전역 스타일 시스템 도입 및 UI 리팩토링
- 전역 스타일 클래스 구조(`main.css`) 도입
  - `--bg-main`, `--text-sub` 등 CSS 변수 기반 다크 테마 색상 시스템 정의
  - Tailwind `@apply`를 활용한 전역 클래스 생성  
    - `.form-container`, `.input-field`, `.btn-primary`, `.prompt-card`, `.page-center` 등
- 중복되던 프롬프트 카드 구조를 `PromptCard.vue` 컴포넌트로 분리하여 재사용성 향상
- `PromptListView.vue`, `HomeView.vue`, `PromptCreateView.vue`, `LoginView.vue` 등에 전역 스타일 반영
- Tailwind purge에 의해 삭제되지 않도록 `tailwind.config.js`에 `safelist` 설정 추가
- 스타일이 적용되지 않던 문제 해결:
  - `scoped` 제거 및 전역 클래스 적용
  - main.css 내부에 클래스 누락된 부분 보완
  - Tailwind 캐시 재빌드 및 purge 방지 설정 반영

---

## 🧭 다음 작업 예정
- GPT API 호출 연동 (프롬프트 실행 결과 자동 생성)