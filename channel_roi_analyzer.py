import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

CHANNEL_SPECS_PATH = os.getenv('CHANNEL_SPECS_PATH', 'config/channel_specs.json')
ROI_RANKING_PATH = os.getenv('ROI_RANKING_PATH', 'data/channel_roi_ranking.json')

# ---------------------- ROI 계산 ----------------------

def load_specs(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_roi(spec: dict) -> float:
    cpm = spec.get('cpm', 0)
    cpa = spec.get('cpa', 0)
    cpc = spec.get('cpc', 0)
    return cpm * 0.5 + cpa * 0.3 + cpc * 0.2


def rank_channels(specs: dict) -> list:
    ranking = []
    for channel, spec in specs.items():
        score = compute_roi(spec)
        ranking.append({'channel': channel, 'roi_score': round(score, 2)})
    ranking.sort(key=lambda x: x['roi_score'], reverse=True)
    return ranking


def main() -> None:
    if not os.path.exists(CHANNEL_SPECS_PATH):
        logging.error(f"Spec file not found: {CHANNEL_SPECS_PATH}")
        return
    specs = load_specs(CHANNEL_SPECS_PATH)
    ranking = rank_channels(specs)

    os.makedirs(os.path.dirname(ROI_RANKING_PATH), exist_ok=True)
    with open(ROI_RANKING_PATH, 'w', encoding='utf-8') as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)
    logging.info(f"ROI ranking saved to {ROI_RANKING_PATH}")

    print("ROI Ranking:")
    for idx, entry in enumerate(ranking, 1):
        print(f"{idx}. {entry['channel']} - score {entry['roi_score']}")


if __name__ == '__main__':
    main()
