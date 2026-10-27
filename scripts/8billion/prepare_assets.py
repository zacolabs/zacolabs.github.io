#!/usr/bin/env python3
"""Refresh local assets from onelife; run after changing translated copy.

python3 -m pip install pillow fonttools brotli
python3 scripts/8billion/prepare_assets.py /path/to/onelife
python3 scripts/build.py

The ordinary site build uses the committed assets and needs no extra packages.
"""
import argparse
import shutil
from pathlib import Path

from fontTools import subset
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('onelife', type=Path)
    source = parser.parse_args().onelife
    here = Path(__file__).resolve().parent
    assets = here.parent.parent / '8billion/assets'
    (assets / 'people').mkdir(parents=True, exist_ok=True)
    for name, path in [('hero', 'app/assets/branding/brand-mark.png'),
                       ('og', 'store/play/en/feature-graphic.png')]:
        with Image.open(source / path) as im:
            im.save(assets / f'{name}.webp', lossless=True)
    for name in ('baby-female-0', 'child-female-0', 'adult-male-0',
                 'adult-female-1', 'elder-female-0'):
        shutil.copyfile(source / f'tools/branding/rendered_figures/{name}.png',
                        assets / f'people/{name}.png')
    shutil.copyfile(source / 'app/assets/fonts/OFL.txt', assets / 'OFL.txt')
    # Include translated text plus the template's Latin labels and era numbers.
    text = ''.join(path.read_text() for path in here.glob('*.json'))
    text += 'One in 8 Billion ANOTHER LIFE 0123456789 한국어 EN'
    options = subset.Options()
    options.flavor = 'woff2'
    font = subset.load_font(source / 'app/assets/fonts/Galmuri11.ttf', options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    subset.save_font(font, assets / 'galmuri.woff2', options)
    print('Updated 8 Billion artwork and subset font.')


if __name__ == '__main__':
    main()
