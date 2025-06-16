# Auto Pipeline

본 저장소는 키워드 기반 콘텐츠 제작을 자동화하기 위한 스크립트를 포함합니다. 
새롭게 `channel_roi_analysis.py`와 `config/channel_specs.json` 파일이 추가되어 
플랫폼별 수익 지표와 콘텐츠 규격을 확인하고 ROI 우선순위를 계산할 수 있습니다.

## ROI 분석 사용법
```bash
python channel_roi_analysis.py
```
해당 명령을 실행하면 각 채널의 ROI 점수와 권장 규격이 출력됩니다.
