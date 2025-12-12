# CampusDoc Tutor (캠퍼스독 튜터)

강의 자료(PDF)를 인덱싱하고, 질문에 대한 답변과 근거(출처)를 제공하는 RAG 기반 AI 튜터입니다.

## 1. 프로젝트 개요 및 구조

이 프로젝트는 **FastAPI**를 기반으로 하며, **LangChain**과 **ChromaDB**를 사용하여 RAG(Retrieval-Augmented Generation) 파이프라인을 구축했습니다. 유지보수를 위해 코드는 기능별로 철저히 분리되어 있습니다.

### 디렉토리 및 파일 상세 설명

```text
vibe-mini-project/
├── .env                # API 키 등 보안이 필요한 환경 설정 (GitHub 등 공유 금지)
├── requirements.txt    # 프로젝트 실행에 필요한 파이썬 패키지 목록
├── README.md           # 프로젝트 설명 및 실행 가이드
│
├── src/                # 소스 코드 메인 디렉토리
│   ├── api/            # [API 계층] 사용자와 상호작용하는 HTTP 엔드포인트
│   │   ├── main.py     # FastAPI 앱 생성 및 서버 실행 진입점
│   │   ├── routes.py   # 실제 API 경로(/ingest, /ask)와 로직 연결
│   │   └── schemas.py  # API 요청/응답 데이터의 형태(타입) 정의
│   │
│   ├── core/           # [설정 계층] 전역 설정 관리
│   │   └── config.py   # .env 파일 로드 및 전역 변수(Settings) 관리
│   │
│   └── rag/            # [RAG 계층] AI 로직 핵심
│       ├── loaders.py  # PDF 파일 로딩 담당
│       ├── splitter.py # 긴 텍스트를 작은 단위(Chunk)로 쪼개는 역할
│       ├── embeddings.py # 텍스트를 벡터(숫자)로 변환하는 모델 설정
│       ├── vectorstore.py # 벡터 데이터베이스(Chroma) 저장/조회 관리
│       ├── prompts.py  # AI에게 지시할 프롬프트(지시문) 템플릿
│       ├── chain.py    # 검색 + 답변 생성을 연결하는 메인 로직
│       └── citations.py # 답변의 근거(출처 파일, 페이지)를 정리하는 도구
│
├── data/               # 데이터 저장소
│   ├── raw/            # 업로드된 원본 PDF 파일들이 저장됨
│   └── chroma/         # 인덱싱된 벡터 데이터가 저장되는 로컬 DB 폴더
│
└── tests/              # 테스트 코드
    └── test_api.py     # API가 정상 동작하는지 확인하는 테스트
```

---

## 2. 코드 상세 설명 (Core Logic)

핵심 동작 방식을 이해하기 위한 주요 파일 설명입니다.

### 1) `src/api/routes.py` (요청 처리)
사용자의 요청을 받아 RAG 로직으로 전달합니다.
- **/ingest (POST)**: 업로드된 PDF를 받아 `data/raw`에 저장 -> `loaders.py`로 읽기 -> `splitter.py`로 분할 -> `vectorstore.py`로 DB에 저장합니다.
- **/ask (POST)**: 질문을 받음 -> `chain.py`의 `ask_question_logic` 실행 -> 결과와 함께 `citations.py`로 포맷팅된 출처를 반환합니다.

### 2) `src/rag/chain.py` (질문/답변 로직)
RAG의 두뇌 역할을 합니다.
1. 사용자의 질문을 받으면 `vectorstore`에서 가장 관련성 높은 문서 조각(Chunk) 3개를 찾습니다.
2. 찾은 문서 내용과 질문을 `prompts.py`에 정의된 템플릿에 넣습니다.
3. OpenAI GPT-4o에 전달하여 답변을 생성합니다.

### 3) `src/rag/vectorstore.py` (저장소)
**ChromaDB**를 사용하여 텍스트 데이터를 벡터로 변환해 저장하고 관리합니다. 로컬 폴더인 `data/chroma`에 영구 저장되므로 서버를 껐다 켜도 데이터가 유지됩니다.

---

## 3. 설치 및 실행 (Setup & Run)

### 1. 필수 조건
- Python 3.10 이상
- `.env` 파일에 API Key 설정 필수

### 2. 설치
```bash
# 가상환경 생성 (선택)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (.env)
루트 경로에 `.env` 파일을 생성하고 키를 입력합니다.
```ini
OPENAI_API_KEY=sk-...           # 필수
TAVILY_API_KEY=tvly-...         # (선택) 웹 검색용
LANGCHAIN_API_KEY=...           # (선택) LangSmith 모니터링용
LANGCHAIN_TRACING_V2=true       # (선택) LangSmith 활성화
```

### 4. 서버 실행
```bash
uvicorn src.api.main:app --reload
```

---

## 4. 사용 방법 (Usage)

서버 실행 후 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** 에 접속하면 Swagger UI가 열립니다.

1. **/ingest**: PDF 파일을 업로드하여 학습시킵니다.
2. **/ask**: "이 문서의 요약은?" 같은 질문을 보냅니다.
3. **결과**: AI의 답변과 함께 참고한 PDF 페이지 번호가 표시됩니다.
