# 🔍 Local CodeReview AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green.svg)](https://ollama.ai/)

> **로컬 LLM 기반 AI 코드 리뷰 도구** — 인터넷 없이, API 키 없이, 완전히 로컬에서 동작하는 AI 코드 리뷰어

## ✨ 주요 기능

- 🔄 **Git Diff 기반 코드 리뷰** — 변경된 코드만 분석하여 효율적인 리뷰
- 📄 **전체 파일 코드 리뷰** — 파일 전체를 분석하여 종합적인 피드백
- 🔒 **보안 취약점 탐지** — SQL Injection, XSS 등 보안 이슈 자동 탐지
- 🎨 **코드 스타일/컨벤션 체크** — PEP8, 네이밍 컨벤션 등 코드 품질 검사
- 📝 **Markdown 리포트 생성** — 리뷰 결과를 깔끔한 Markdown 파일로 저장
- 💻 **CLI 인터페이스** — 간편한 커맨드라인 인터페이스

## 🚀 빠른 시작

### 사전 요구사항

1. **Python 3.9+**
2. **Ollama** 설치 및 실행

   ```bash
   # Ollama 설치 (https://ollama.ai)
   # 모델 다운로드
   ollama pull codellama
   ```

### 설치

```bash
# 저장소 클론
git clone https://github.com/jeonghoemoon/local-codereview-ai.git
cd local-codereview-ai

# 의존성 설치
pip install -e .
```

### 사용법

```bash
# 전체 파일 리뷰
codereview review path/to/file.py

# Git diff 리뷰 (스테이징된 변경사항)
codereview diff --staged

# Git diff 리뷰 (특정 커밋 비교)
codereview diff HEAD~1

# 보안 취약점 탐지
codereview security path/to/file.py

# 코드 스타일 체크
codereview style path/to/file.py

# 전체 분석 (리뷰 + 보안 + 스타일)
codereview full path/to/file.py

# 리포트를 Markdown 파일로 저장
codereview review path/to/file.py --output report.md
```

## 📋 명령어 상세

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `review` | 전체 파일 코드 리뷰 | `codereview review main.py` |
| `diff` | Git diff 기반 리뷰 | `codereview diff --staged` |
| `security` | 보안 취약점 탐지 | `codereview security app.py` |
| `style` | 코드 스타일 체크 | `codereview style utils.py` |
| `full` | 전체 분석 | `codereview full server.py` |

### 공통 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--model` | 사용할 Ollama 모델 | `codellama` |
| `--output` | 리포트 출력 파일 경로 | (콘솔 출력) |
| `--lang` | 리뷰 결과 언어 | `ko` (한국어) |

## 🏗️ 프로젝트 구조

```
local-codereview-ai/
├── src/
│   └── codereview/
│       ├── __init__.py
│       ├── cli.py          # CLI 인터페이스
│       ├── reviewer.py     # 코드 리뷰 엔진
│       ├── diff_analyzer.py # Git diff 분석
│       ├── security.py     # 보안 취약점 탐지
│       ├── style_checker.py # 스타일 체크
│       ├── report.py       # Markdown 리포트 생성
│       ├── llm_client.py   # Ollama LLM 클라이언트
│       └── prompts.py      # AI 프롬프트 템플릿
├── tests/
│   ├── __init__.py
│   ├── test_reviewer.py
│   ├── test_security.py
│   └── test_style_checker.py
├── examples/
│   └── sample_code.py      # 테스트용 샘플 코드
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## 🤝 기여하기

기여를 환영합니다! [CONTRIBUTING.md](CONTRIBUTING.md)를 참고해주세요.

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

## 🙏 감사의 글

- [Ollama](https://ollama.ai/) — 로컬 LLM 런타임
- [Code Llama](https://ai.meta.com/blog/code-llama-large-language-model-coding/) — Meta의 코드 특화 LLM
