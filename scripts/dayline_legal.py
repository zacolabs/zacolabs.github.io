#!/usr/bin/env python3
"""Dayline 이용 약관 · 개인정보 처리방침 · 오픈소스 라이선스 페이지 생성기. build.py 가 같이 돌린다.

    python3 scripts/dayline_legal.py     (이 페이지들만 다시 만들 때)

dayline/<문서>.<언어>.html 의 본문을 dayline/style.css 와 함께 감싸 /dayline/ 아래에 쓴다.
이 본문이 기준이다 — 앱은 글을 따로 싣지 않고 이 주소를 연다.

    /dayline/<문서>.<언어>.html   언어 고정
    /dayline/<문서>.html          언어 자동: ?lang= → 브라우저 언어 → 영어

모양과 주소 규칙은 Waky 의 같은 페이지(zacolabs-backend src/content/waky/legal, /api/<문서>.html)를 따른다.
Waky 는 서버가 ?lang= · ?theme= 을 읽지만 여기는 정적 호스팅이라 페이지 안의 스크립트가 읽는다.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(HERE, "dayline")
OUT = os.path.join(ROOT, "dayline")

# 언어 순서 — 언어 줄이 이 순서를 따른다. Dayline 앱이 내는 언어와 같다.
LANGS = [("ko", "한국어"), ("en", "English")]
DEFAULT = "en"

# 문서와 언어별 제목. 라이선스는 Waky 처럼 본문 머리(h1) 없이 목록부터 시작한다.
DOCS = {
    "privacy": {"ko": "Dayline 개인정보 처리방침", "en": "Dayline Privacy Policy"},
    "terms": {"ko": "Dayline 이용 약관", "en": "Dayline Terms of Service"},
    "licenses": {"ko": "Dayline 오픈소스 라이선스", "en": "Dayline Open Source Licenses"},
}
NO_HEADING = {"licenses"}


def langnav(doc, lang):
    items = [
        f"<strong>{label}</strong>" if code == lang else f'<a href="{doc}.{code}.html">{label}</a>'
        for code, label in LANGS
    ]
    return f'    <p class="langnav">{" · ".join(items)}</p>'


def head_script(doc, auto):
    """`?theme=light` 면 라이트로. 언어 자동 주소에서는 `?lang=` → 브라우저 언어 순으로 보고
    영어가 아니면 그 언어의 고정 주소로 옮긴다 (밝기는 들고 간다)."""
    redirect = ""
    if auto:
        redirect = f'''
        var LANGS = {json.dumps([code for code, _ in LANGS])};
        function norm(v) {{
            v = (v || "").trim().toLowerCase().replace(/_/g, "-").split("-")[0];
            if (v === "kr") v = "ko";
            return LANGS.indexOf(v) !== -1 ? v : null;
        }}
        var wanted = [q.get("lang")].concat(navigator.languages || [navigator.language]);
        for (var i = 0; i < wanted.length; i++) {{
            var l = norm(wanted[i]);
            if (!l) continue;
            if (l !== "{DEFAULT}") location.replace("{doc}." + l + ".html" + (light ? "?theme=light" : ""));
            break;
        }}'''
    return f'''<script>
    (function () {{
        var q = new URLSearchParams(location.search);
        var light = (q.get("theme") || "").toLowerCase() === "light";
        if (light) document.documentElement.setAttribute("data-theme", "light");{redirect}
    }})();
</script>'''


def page(doc, lang, css, auto=False):
    title = DOCS[doc][lang]
    with open(os.path.join(SRC, f"{doc}.{lang}.html"), encoding="utf-8") as f:
        body = f.read().rstrip("\n")
    heading = "" if doc in NO_HEADING else f"    <h1>{html.escape(title)}</h1>\n"
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)}</title>
{head_script(doc, auto)}
<style>
{css}</style>
</head>
<body>
<div class="container">
{heading}{langnav(doc, lang)}
{body}
</div>
<script>
    // 언어를 바꿔도 밝기가 따라가게 한다
    if (document.documentElement.getAttribute("data-theme") === "light") {{
        document.querySelectorAll(".langnav a").forEach(function (a) {{
            a.setAttribute("href", a.getAttribute("href") + "?theme=light");
        }});
    }}
</script>
</body>
</html>
'''


def build():
    with open(os.path.join(SRC, "style.css"), encoding="utf-8") as f:
        css = f.read()
    os.makedirs(OUT, exist_ok=True)
    count = 0
    for doc in DOCS:
        pages = {f"{doc}.{code}.html": page(doc, code, css) for code, _ in LANGS}
        pages[f"{doc}.html"] = page(doc, DEFAULT, css, auto=True)
        for name, text in pages.items():
            with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
                f.write(text)
            count += 1
    return count


if __name__ == "__main__":
    print(f"built {build()} dayline legal pages")
