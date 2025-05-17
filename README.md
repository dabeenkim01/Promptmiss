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

## ✅ 현재 완료된 작업 (2025.05.17 기준)

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

### 4. 테스트
- Postman에서 회원가입/로그인/프롬프트 생성 테스트 완료
- JWT 토큰 기반 인증 테스트 완료 (access + refresh)
- 인증 사용자 기반 프롬프트 생성 및 조회 정상 작동 확인

---

## 🧭 다음 작업 예정
- 프론트(Vue)에서 Axios로 API 연동
- JWT 기반 사용자 인증 기능 추가
- 프롬프트 실행 결과 자동 생성 로직 구현 (ex. GPT API 연동)
