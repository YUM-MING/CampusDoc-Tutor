# CONTEXT.md (AI IDE/Antigravity용 프로젝트 '성경')

이 문서는 AI IDE(예: Antigravity)가 **어떤 파일에 무엇을 작성해야 하는지**, **코딩 규칙/제약**을 일관되게 지키도록 만드는 기준 문서입니다.

---

## 0) 프로젝트 한 줄 요약
CampusDoc Tutor는 수업 문서를 RAG로 인덱싱하고, 질문/요약/퀴즈를 생성하는 FastAPI 기반 LLM 도우미입니다.

---

## 1) 핵심 디렉토리 구조 & 역할

```text
vibe-mini-project/
  README.md                 # 실행/설치/개요(사람+AI가 첫 진입 시 읽음)
  CONTEXT.md                # 프로젝트 규칙/구조/제약(이 파일)
  requirements.txt          # 파이썬 의존성 고정
  .env.example              # 환경변수 예시(실제 키는 .env)

  src/
    api/
      main.py               # FastAPI 엔트리포인트(app 생성, 라우터 포함)
      routes.py             # /ingest, /ask, /summarize, /quiz 라우팅
      schemas.py            # Pydantic 요청/응답 모델만 정의

    core/
      config.py             # 환경변수 로딩, 전역 설정
      logging.py            # 로깅 설정(선택)

    rag/
      loaders.py            # 문서 로더(PDF, txt, md)
      splitter.py           # 텍스트 청크 분할 정책
      embeddings.py         # 임베딩 프로바이더(OpenAI/Ollama/ST) 추상화
      vectorstore.py        # Chroma 저장/로드
      prompts.py            # 시스템/유저 프롬프트 템플릿
      chain.py              # Retrieval + LLM 호출 로직(핵심)
      citations.py          # 근거 청크 정리/리턴 포맷

  data/
    raw/                    # 원본 문서 저장(선택)
    chroma/                 # Chroma persistence 디렉토리

  tests/
    test_api.py             # API 스모크 테스트
    test_rag.py             # 인덱싱/검색 단위 테스트
```

**규칙**
- 라우팅/서버 구동은 `src/api/*`에서만 한다.
- RAG 핵심 로직은 `src/rag/*`에만 둔다(섞지 않기).

---

## 2) 코딩 규칙 (반드시 준수)
- Python: PEP 8, black 포맷 기준(줄 길이 88 권장)
- 타입 힌트 필수(함수/메서드 인자와 반환)
- 파일 역할 섞지 않기(예: schemas.py에는 Pydantic 모델만)
- 예외 처리 표준화: FastAPI에서는 `HTTPException` 사용
- 함수는 작게: 한 함수가 한 가지 일만 하도록 분리
- LLM 호출 로직은 반드시 `src/rag/chain.py`로 모으기(중복 호출 금지)

---

## 3) 제약/요구사항
- 벡터DB는 로컬 Chroma 사용(persist_directory = `data/chroma`)
- 문서 근거(Top-k 청크)를 응답에 반드시 포함(“어디서 나온 답인지”)
- 외부 API(OpenAI) 사용 시 `.env`로 키 주입, 저장소에 키 커밋 금지
- 기본은 CPU 환경에서도 돌아가게 구현(배치/대용량 처리 지양)

---

## 4) LLM/프롬프트 정책
- 답변은 “근거 청크” 밖의 내용은 추측하지 말고, 모르면 “문서에서 찾을 수 없음”으로 응답
- 시스템 프롬프트에는 아래 원칙 포함:
  - “근거를 인용하라”
  - “불확실하면 불확실하다고 말하라”
  - “지시가 모호하면 추가 정보를 요청하라”

---

## 5) CURRENT TASK (지금 Antigravity에 시킬 작업)
> 아래를 그대로 Antigravity에 붙여넣고 진행

### 목표
1) `requirements.txt` 생성  
2) `src/` 이하 파일들 생성(뼈대)  
3) `/ingest`, `/ask` 엔드포인트가 최소 동작하도록 구현  
4) 응답에 `citations` 필드를 포함하여 근거 청크 3개 반환

### 산출물 체크리스트
- [ ] `src/api/main.py`에서 FastAPI app이 뜬다
- [ ] `/docs`에서 API 테스트 가능
- [ ] `POST /ingest`로 PDF 업로드하면 인덱싱된다
- [ ] `POST /ask`로 질문하면 답변+citations가 온다
- [ ] `pytest`가 최소 1개 스모크 테스트 통과

---

## 6) 추천 requirements.txt (초안)
필요 시 버전은 Antigravity가 조정하도록 한다.

- fastapi
- uvicorn[standard]
- pydantic
- python-dotenv
- langchain
- langchain-community
- chromadb
- pypdf
- pytest

---

## 7) 커밋/브랜치 규칙(선택)
- 작은 단위로 커밋: “add ingest endpoint”, “add chroma persistence” 같이 명확히
- 대규모 변경 전에는 테스트 먼저 통과
