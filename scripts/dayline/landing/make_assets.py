#!/usr/bin/env python3
"""Dayline 랜딩의 공유 미리보기 그림을 스토어 그림에서 만든다.

    python3 scripts/dayline/landing/make_assets.py

앱 저장소가 이 저장소 옆에 있어야 하고(dayline-android), Pillow 가 필요하다.
스토어 그림이 바뀌었거나 랜딩에 언어를 더했을 때만 돌린다 — build.py 는 이걸 돌리지 않는다.

    assets/og-<언어>.png      Play 피처 그래픽(1024x500)을 1200x630 바탕 가운데에 놓은 것
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "dayline", "assets")
PLAY = os.path.normpath(os.path.join(ROOT, "..", "dayline-android", "store", "play"))
BG = (0x11, 0x11, 0x13)


def store_tag(code):
    """랜딩의 언어 코드(zh-hans)를 스토어 그림의 폴더 이름(zh-Hans)으로."""
    return {"zh-hans": "zh-Hans", "zh-hant": "zh-Hant"}.get(code, code)


def og(im):
    im = im.convert("RGB")
    w = 1200
    h = round(im.height * w / im.width)
    canvas = Image.new("RGB", (1200, 630), BG)
    canvas.paste(im.resize((w, h), Image.LANCZOS), (0, (630 - h) // 2))
    return canvas


def main():
    os.makedirs(OUT, exist_ok=True)
    codes = sorted(f[:-5] for f in os.listdir(os.path.join(HERE, "i18n")) if f.endswith(".json"))
    for code in codes:
        tag = store_tag(code)
        og(Image.open(os.path.join(PLAY, tag, "feature-graphic.png"))).save(
            os.path.join(OUT, f"og-{code}.png"), optimize=True)
        print("made", code)


if __name__ == "__main__":
    main()
