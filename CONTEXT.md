# CONTEXT.md

## 1. 핵심 파일 구조 (Core File Structure)
```
CampusDoc-Tutor/
├── client_test.py          # API 테스트를 위한 클라이언트 스크립트
├── requirements.txt        # 프로젝트 의존성 목록
├── src/
│   ├── api/
│   │   ├── main.py         # FastAPI 앱 진입점, 정적 파일 마운트
│   │   └── routes.py       # API 엔드포인트 정의 (/ingest, /ask, /files, /reset)
│   ├── core/
│   │   └── config.py       # 환경 변수 및 설정 (Ollama 설정 등)
│   ├── rag/
│   │   ├── chain.py        # RAG 체인 로직 (답변 생성, 추천 질문 생성)
│   │   ├── prompts.py      # LLM 프롬프트 템플릿 (한국어 최적화)
│   │   └── vectorstore.py  # ChromaDB 벡터 스토어 관리
│   └── static/             # 웹 프론트엔드 리소스
│       ├── index.html      # 메인 UI
│       ├── script.js       # 프론트엔드 로직 (파일 처리, 채팅)
│       └── style.css       # 스타일시트
└── data/
    ├── chroma/             # 벡터 데이터베이스 저장소
    └── raw/                # 업로드된 원본 PDF 파일 저장소
```

## 2. 데이터 명세 (Data Specification)
*   **Input Data**: PDF (`.pdf`) 파일. 텍스트 추출이 가능한 형식이어야 합니다.
*   **Vector Store**: ChromaDB (Local Persist).
    *   **Collection**: PDF 텍스트 청크 및 임베딩 벡터.
    *   **Embedding Model**: Ollama (`llama3`).
*   **API Interactions**: JSON Format.
    *   `/ingest`: Multipart Form Data (File).
    *   `/ask`: JSON `{"question": "..."}` -> JSON `{"answer": "...", "citations": [...]}`.

## 3. 기술적 제약 사항 (Technical Constraints)
*   **Context Window**: 로컬 LLM(Llama 3)의 컨텍스트 윈도우 제한으로 인해, 매우 긴 문서의 경우 전체 요약보다는 검색된(Retrieved) 일부 청크에 기반한 답변이 생성됩니다.
*   **Local Inference**: Ollama를 로컬에서 구동하므로, 호스트 머신의 GPU/CPU 성능에 따라 응답 속도가 달라질 수 있습니다.
*   **PDF Parsing**: 이미지로 된 PDF(스캔본)는 OCR 처리가 되어 있지 않으면 텍스트 인식이 불가능할 수 있습니다.

## 4. 개선 사항 (Improvements)
*   **OCR 통합**: 스캔된 PDF 문서 지원을 위한 Tesseract 등 OCR 엔진 도입.
*   **Streaming Response**: 긴 답변 생성 시 사용자 경험 향상을 위한 토큰 스트리밍 적용.
*   **Multi-turn Chat**: 현재 단답형 RAG 구조에서, 이전 대화 맥락을 기억하는 멀티턴(Memory) 구조로 고도화.
*   **Advanced Retrieval**: Hybrid Search (Keyword + Vector) 또는 Reranking 도입으로 검색 정확도 향상.
