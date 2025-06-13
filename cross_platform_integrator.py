import logging
from typing import Dict, List

# ---------------------- 로깅 설정 ----------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- 데이터 통합 ----------------------

def integrate_data(*datasets: Dict) -> Dict:
    """여러 플랫폼의 데이터를 통합"""
    logging.info("데이터 통합 시작")

    integrated: Dict[str, float | int | List] = {}
    for data in datasets:
        for key, value in data.items():
            # 기존 키가 존재하면 값 합산 또는 업데이트
            if isinstance(value, (int, float)):
                integrated[key] = integrated.get(key, 0) + value
            elif isinstance(value, list):
                integrated.setdefault(key, []).extend(value)
            else:
                integrated[key] = value

    logging.info("데이터 통합 완료")
    return integrated

