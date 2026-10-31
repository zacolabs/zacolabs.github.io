#!/usr/bin/env python3
"""냥반장 랜딩의 그림을 앱 저장소에서 만든다 (Pillow 필요). 일반 빌드는 이걸 돌리지 않는다.

    python3 scripts/catcaptain/prepare_assets.py ../catcaptain-android

- shot-1~5.webp — App Store 스크린샷 2~6번(store/appstore/ko)의 아래쪽 카드만 잘라 낸 것. 제목은 랜딩이 글로 쓴다
- cat-<이름>.webp — 앱의 예시 고양이(app/src/main/res/drawable-nodpi/cat_*.jpg)
- og.jpg — 공유 미리보기. App Store 헤더 그림(header.png)을 1200x630 으로 자른 것
"""
import sys
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent.parent / 'catcaptain' / 'assets'
CATS = ('danmuji', 'godeungeo', 'hoejang', 'hotteok', 'kkamang', 'tuxedo')
# 스크린샷(1206x2622)에서 카드가 있는 줄. 위의 제목 · 설명과 아래 여백을 뺀다
CARD_TOP, CARD_BOTTOM = 960, 2390


def main(app):
    OUT.mkdir(parents=True, exist_ok=True)
    shots = app / 'store/appstore/ko'
    for i in range(2, 7):
        im = Image.open(shots / f'screenshot-{i}.png').convert('RGB')
        card = im.crop((0, CARD_TOP, im.width, CARD_BOTTOM))
        card = card.resize((720, round(720 * card.height / card.width)), Image.LANCZOS)
        card.save(OUT / f'shot-{i - 1}.webp', quality=82, method=6)
    for name in CATS:
        im = Image.open(app / f'app/src/main/res/drawable-nodpi/cat_{name}.jpg').convert('RGB')
        im.resize((256, 256), Image.LANCZOS).save(OUT / f'cat-{name}.webp', quality=82, method=6)
    head = Image.open(shots / 'header.png').convert('RGB').resize((1200, 675), Image.LANCZOS)
    head.crop((0, 0, 1200, 630)).save(OUT / 'og.jpg', quality=86, optimize=True, progressive=True)


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve())
