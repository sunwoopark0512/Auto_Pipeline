# Auto_Pipeline

이 프로젝트는 여러 플랫폼에 맞게 콘텐츠를 변환하는 도구를 제공합니다.

## 사용 방법
1. `content_converter.py` 모듈에서 `convert_content` 함수를 불러옵니다.
2. 원본 텍스트와 변환할 플랫폼 이름을 인자로 전달합니다.
3. 지원 플랫폼: `youtube`, `instagram`, `tiktok`, `facebook`, `linkedin`.

```python
from content_converter import convert_content

text = "원소스 멀티유스 전략으로 수익을 극대화하는 방법\n..."
yt_script = convert_content(text, "youtube")
print(yt_script)
```

새로운 플랫폼 템플릿을 추가하려면 `TEMPLATES` 딕셔너리에 항목을 추가하고 `convert_content`에서 분기 처리를 구현하면 됩니다.
