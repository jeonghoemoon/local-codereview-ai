# 🤝 Contributing to Local CodeReview AI

기여를 환영합니다! 이 문서는 프로젝트에 기여하는 방법을 안내합니다.

## 🐛 버그 리포트

1. [Issues](https://github.com/jeonghoemoon/local-codereview-ai/issues)에서 이미 보고된 버그인지 확인해주세요.
2. 새 이슈를 만들 때 다음 정보를 포함해주세요:
   - 운영체제 및 Python 버전
   - Ollama 버전 및 사용 모델
   - 재현 단계
   - 예상 동작 vs 실제 동작

## 💡 기능 제안

새로운 기능 아이디어가 있다면 Issue를 열어 논의해주세요.

## 🔧 개발 환경 설정

```bash
# 저장소 포크 및 클론
git clone https://github.com/jeonghoemoon/local-codereview-ai.git
cd local-codereview-ai

# 개발 의존성 설치
pip install -e ".[dev]"

# 테스트 실행
pytest
```

## 📝 Pull Request 가이드라인

1. `main` 브랜치에서 새 브랜치를 만들어주세요.
2. 변경사항에 대한 테스트를 추가해주세요.
3. 모든 테스트가 통과하는지 확인해주세요.
4. 커밋 메시지는 명확하게 작성해주세요.
5. PR 설명에 변경사항을 상세히 기술해주세요.

## 📋 코드 스타일

- PEP 8 스타일 가이드를 따릅니다.
- Type hints를 사용해주세요.
- Docstring은 Google 스타일을 따릅니다.

## 📜 라이선스

기여하신 코드는 [MIT 라이선스](LICENSE)에 따라 배포됩니다.
