# CampusDoc Tutor

## 1. 개요 및 목적 (Overview & Purpose)
**CampusDoc Tutor**는 RAG(Retrieval-Augmented Generation) 기술을 기반으로 한 지능형 문서 튜터 시스템입니다.
사용자가 PDF 문서를 업로드하면, 해당 문서의 내용을 분석하여 질문에 대한 답변을 제공하고, 요약, 퀴즈 생성 등 학습을 돕는 다양한 기능을 수행합니다.
복잡한 문서 내용을 쉽게 이해하고 학습할 수 있도록 돕는 것을 목적으로 합니다.

## 2. 기술 스택 (Tech Stack)
*   **Backend Framework**: FastAPI
*   **Language**: Python 3.9+
*   **LLM & Embeddings**: Ollama (Llama 3)
*   **Vector Database**: ChromaDB
*   **RAG Framework**: LangChain
*   **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 3. 설치 방법 (Installation)

### 사전 준비
1.  [Python](https://www.python.org/) 설치
2.  [Ollama](https://ollama.com/) 설치 및 `llama3` 모델 다운로드
    ```bash
    ollama pull llama3
    ```

### 프로젝트 설정
1.  저장소 클론
    ```bash
    git clone https://github.com/YUM-MING/CampusDoc-Tutor.git
    cd CampusDoc-Tutor
    ```
2.  가상환경 생성 및 실행 (Windows)
    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  의존성 패키지 설치
    ```bash
    pip install -r requirements.txt
    ```

## 4. 실행 방법 (Execution)
서버 실행:
```powershell
python -m uvicorn src.api.main:app --reload
```
웹 브라우저에서 `http://127.0.0.1:8000` 접속

## 5. 제공 기능 (Provided Features)
*   **PDF 문서 업로드**: 사용자가 학습할 PDF 파일을 업로드하여 시스템에 등록할 수 있습니다.
*   **문서 기반 질의응답 (QA)**: 업로드된 문서 내용을 바탕으로 정확한 답변과 출처(인용)를 제공합니다.
*   **자동 추천 질문**: 문서 업로드 시, 핵심 내용을 바탕으로 AI가 질문 3가지를 자동으로 추천해 줍니다.
*   **학습 도구 생성**: "요약해줘", "퀴즈 만들어줘", "문제 내줘" 등의 요청을 통해 학습 자료를 생성할 수 있습니다.
*   **파일 관리**: 업로드된 파일을 관리하고, 필요 시 전체 초기화(Reset)할 수 있습니다.
*   **파일 검증**: 업로드된 파일의 용량을 확인하고 원본을 뷰어로 열어볼 수 있습니다.

## 6. Github 링크 (GitHub Link)
*   [https://github.com/YUM-MING/CampusDoc-Tutor](https://github.com/YUM-MING/CampusDoc-Tutor)
