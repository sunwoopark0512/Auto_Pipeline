import os
import json
import logging
import random
from typing import Optional

try:
    import requests
except ImportError:  # fallback if requests not installed
    requests = None

# ---------------------- 설정 ----------------------
CACHE_PATH = os.getenv("CPC_CACHE_PATH", "data/cpc_cache.json")
API_URL = os.getenv("CPC_API_URL")  # 외부 CPC API 엔드포인트

_cpc_cache = {}

# ---------------------- 캐시 로딩/저장 ----------------------
def _load_cache():
    global _cpc_cache
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                _cpc_cache = json.load(f)
        except Exception as e:
            logging.warning(f"CPC 캐시 로딩 실패: {e}")
            _cpc_cache = {}


def _save_cache():
    try:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(_cpc_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.warning(f"CPC 캐시 저장 실패: {e}")


_load_cache()

# ---------------------- API 호출 ----------------------
def fetch_cpc_from_api(keyword: str) -> Optional[int]:
    if not API_URL or requests is None:
        return None
    try:
        response = requests.get(API_URL, params={"keyword": keyword}, timeout=5)
        response.raise_for_status()
        data = response.json()
        cpc_value = int(data.get("cpc"))
        return cpc_value
    except Exception as e:
        logging.error(f"CPC API 실패: {keyword} - {e}")
        return None


# ---------------------- 더미 CPC ----------------------
def fetch_cpc_dummy(keyword: str) -> int:
    return random.randint(500, 2000)


# ---------------------- 공개 함수 ----------------------
def get_cpc(keyword: str) -> int:
    if keyword in _cpc_cache:
        return _cpc_cache[keyword]

    cpc = fetch_cpc_from_api(keyword)
    if cpc is None:
        cpc = fetch_cpc_dummy(keyword)
    _cpc_cache[keyword] = cpc
    _save_cache()
    return cpc
