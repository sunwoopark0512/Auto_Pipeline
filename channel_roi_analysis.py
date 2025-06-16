import json
import os
import logging

CONFIG_PATH = os.getenv("CHANNEL_SPECS_PATH", "config/channel_specs.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def load_channels(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("channels", [])


def calc_roi(ch):
    cpm = ch.get("cpm", 0)
    cpc = ch.get("cpc", 0)
    cpa = ch.get("cpa", 0)
    return round(cpm * 0.5 + cpc * 0.3 + cpa * 0.2, 2)


def main():
    channels = load_channels(CONFIG_PATH)
    for ch in channels:
        ch["roi_score"] = calc_roi(ch)
    channels.sort(key=lambda x: x["roi_score"], reverse=True)

    print("채널 ROI 우선순위")
    for idx, ch in enumerate(channels, start=1):
        spec = ch.get("content_spec", {})
        print(f"{idx}. {ch['name']} - ROI {ch['roi_score']}")
        print(
            f"   규격: 텍스트 {spec.get('text_length', 'N/A')}, "
            f"이미지 {spec.get('image_size', 'N/A')}, "
            f"영상 {spec.get('video_size', 'N/A')}, "
            f"해시태그 {spec.get('hashtags', 'N/A')}"
        )


if __name__ == "__main__":
    main()
