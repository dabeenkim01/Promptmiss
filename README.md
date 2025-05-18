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

## ✅ 현재 완료된 작업 (2025.05.18 기준, 최신 반영 완료)

### 1. Django 백엔드 초기 세팅
- 프로젝트명: `config`
- 앱명: `prompts`
- `rest_framework`, `prompts` 앱 등록
- `.gitignore`에 venv, pycache, DS_Store 등 추가

### 2. 모델 설계
- Prompt 모델: user(FK), title, content, tags, created_at
- Execution 모델: prompt(FK), user_input, result, executed_at

### 3. API 개발
- PromptViewSet, ExecutionViewSet 구현 (ModelViewSet)
- PromptSerializer, ExecutionSerializer 구현
- 사용자 인증 기반 Prompt 생성 (request.user 자동 연동)
- 로그인 사용자만 프롬프트 생성 가능 (IsAuthenticated)
- 전체 Prompt 목록 조회 (비로그인 가능, IsAuthenticatedOrReadOnly)
- 내 프롬프트만 필터링 조회 (`/api/prompts/?mine=true`)
- `/api/prompts/`, `/api/executions/`, `/api/accounts/` REST API 엔드포인트 생성

- 좋아요/북마크 기능 구현 (`/api/prompts/<id>/like/`, `/bookmark/`)
- `?liked=true`, `?bookmarked=true` 파라미터로 필터링 가능
- PromptSerializer에 like_count, bookmark_count 필드 포함
- 실행 API (`/api/prompts/<id>/execute/`) 구현 및 실행 결과 저장
- Execution 모델에 user 필드 추가, 본인 이력만 필터링 조회 가능
- Prompt 상세 응답에 실행 이력과 댓글 리스트 포함

### 4. 테스트
- Postman에서 회원가입/로그인/프롬프트 생성 테스트 완료
- JWT 토큰 기반 인증 테스트 완료 (access + refresh)
- 인증 사용자 기반 프롬프트 생성 및 조회 정상 작동 확인

### 5. 댓글 기능 추가
- Comment 모델 생성: user, prompt, content, created_at
- `/api/comments/`로 CRUD API 구현 (ModelViewSet)
- Prompt 상세 조회 시 댓글 리스트 포함 (최신순 정렬)
- 댓글 응답에 작성자 정보 포함
- 댓글 수정/삭제 시 본인만 가능하도록 커스텀 권한(`IsOwnerOrReadOnly`) 설정

### 6. 프롬프트 수정/삭제 및 권한 처리
- 프롬프트 수정/삭제 기능 API 구현 (PUT, DELETE)
- `perform_update`, `perform_destroy`에서 작성자 본인 확인
- PromptSerializer 사용자 필드 구조 정리 (ID 반환)
- 사용자 정보 조회 API(`/api/users/me/`) 구현
- 작성자 외 접근 시 `PermissionDenied` 처리

### 7. 프론트엔드 기능 연동 (Vue)
- 프롬프트 수정/삭제 페이지 구현 및 API 연동
- 작성자 본인에게만 수정/삭제 버튼 노출
- 삭제 시 confirm 처리 및 중복 클릭 방지 로직 추가
- Tailwind 기반 스타일 통일 (생성/수정/상세)
- 사용자 정보 localStorage 관리 및 권한 확인 연동

---

## 🧭 다음 작업 예정
✅ 프론트(Vue)에서 Axios로 API 연동
✅ JWT 기반 사용자 인증 기능 연동
- GPT API 호출 연동 (프롬프트 실행 결과 자동 생성)
