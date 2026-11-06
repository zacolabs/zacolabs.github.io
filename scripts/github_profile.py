#!/usr/bin/env python3
"""GitHub 프로필 README (github.com/zacolabs) 생성기.

    python3 scripts/github_profile.py [출력 폴더, 기본 ../zacolabs]

프로필에는 zacolabs/zacolabs 저장소의 README.md 하나만 보인다 — 방문자 언어로 바뀌지 않아서
README.md 는 영어로 두고, 맨 위의 언어 줄에서 README.<언어>.md 로 보낸다.
문구는 회사 소개와 같은 scripts/i18n/<언어>.json 을, 스토어 · 랜딩 주소는 build.py 의 것을 쓴다.
랜딩 본문을 옮기지 않고 짧은 소개와 링크만 둔다 (같은 글이 두 곳에 있으면 검색에서 서로 겨룬다).
README 에만 쓰는 몇 마디는 아래 TEXT 에 있다 — 언어를 늘릴 때는 TEXT 에 그 언어를 더한다.
"""
import os
import sys

import build
import catcaptain_landing
import dayline_landing
import eightbillion_landing

SITE = build.SITE
ICON = f"{SITE}/zacolabs-assets"
# README.md 가 영어다. 언어 줄은 이 순서로 나온다
LANGS = ("en", "ko")
TEXT = {
    "en": {"products": "Products", "website": "Website", "contact": "Contact",
           "company": "About Zaco Labs", "korea": "Available in Korea only; the website is in Korean."},
    "ko": {"products": "제품", "website": "웹사이트", "contact": "문의",
           "company": "Zaco Labs 소개", "korea": None},
}


def readme_name(code):
    return "README.md" if code == build.DEFAULT else f"README.{code}.md"


def links(*pairs):
    """[이름](주소) 를 · 로 잇는다. 주소가 없는 것은 뺀다."""
    return " · ".join(f"[{name}]({url})" for name, url in pairs if url)


def product(icon, name, kind, title, body, link_line, note=None):
    lines = [f'### <img src="{ICON}/{icon}" width="28" height="28" alt="" align="center"> {name}', "",
             f"**{title}**", "", body, ""]
    if note:
        lines += [f"> {note}", ""]
    lines += [f"<sub>{kind}</sub>", "", link_line, ""]
    return "\n".join(lines)


def readme(code):
    t = build.load(code)
    x = TEXT[code]
    soon = t["coming_soon"]
    lang_line = " · ".join(
        f"<b>{build.load(c)['label']}</b>" if c == code else f'<a href="{readme_name(c)}">{build.load(c)["label"]}</a>' for c in LANGS)

    def stores(web, play, apple):
        """웹사이트 · 스토어 링크. 스토어가 하나도 없으면 끝에 "출시 예정"을 붙인다."""
        line = links((x["website"], web), ("Google Play", play), ("App Store", apple))
        return line if play or apple else " · ".join(filter(None, (line, soon)))

    products = [
        product("duire_icon-104.webp", t["duire_name"], t["duire_kind"], t["duire_title"], t["duire_body"],
                links((x["website"], build.duire_url(code)), ("Store Bridge", build.bridge_url(code)))),
        product("app_icon-104.webp", "Waky", t["waky_kind"], t["waky_title"], t["waky_body"],
                stores(build.waky_url(t), build.PLAY, build.APPLE)),
        product("dayline_icon-104.webp", "Dayline", t["waky_kind"], t["dayline_title"], t["dayline_body"],
                stores(SITE + dayline_landing.landing_path(code), build.DAYLINE_PLAY, build.DAYLINE_APPLE)),
        product("catcaptain_icon-104.webp", t["catcaptain_name"], t["catcaptain_kind"], t["catcaptain_title"],
                t["catcaptain_body"], stores(SITE + catcaptain_landing.PATH, build.CATCAPTAIN_PLAY, build.CATCAPTAIN_APPLE),
                x["korea"]),
        product("catinroom_icon-104.webp", "Cat in Room", t["waky_kind"], t["catinroom_title"], t["catinroom_body"],
                stores(None, build.CATINROOM_PLAY, build.CATINROOM_APPLE)),
        product("8billion_icon-104.webp", "8 Billion", t["eightbillion_kind"], t["eightbillion_title"],
                t["eightbillion_body"],
                stores(SITE + eightbillion_landing.landing_path(code), build.EIGHTBILLION_PLAY, build.EIGHTBILLION_APPLE)),
    ]
    about = "<br>\n".join(t["about"])
    return f"""<!-- scripts/github_profile.py (zacolabs.github.io) 가 만든다 — 직접 고치지 말 것 -->
<p align="center">
  <img src="{ICON}/logo-256.webp" width="96" height="96" alt="{t['logo_alt']}">
</p>
<h1 align="center">Zaco Labs</h1>
<p align="center">{t['tagline']}</p>
<p align="center">{lang_line}</p>

<p align="center">
{about}
</p>

## {x['products']}

{chr(10).join(products)}
---

[{x['company']}]({build.url(code)}) · {x['contact']}: [zaco.labs@gmail.com](mailto:zaco.labs@gmail.com)
"""


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(build.ROOT, "..", "zacolabs"))
    os.makedirs(out, exist_ok=True)
    for code in LANGS:
        with open(os.path.join(out, readme_name(code)), "w", encoding="utf-8") as f:
            f.write(readme(code))
    print(f"wrote {len(LANGS)} READMEs to {out}")


if __name__ == "__main__":
    main()
