#!/usr/bin/env python3
"""Dayline 이용 약관 · 개인정보 처리방침 · 커뮤니티 규칙 · 오픈소스 라이선스 페이지 생성기. build.py 가 같이 돌린다.

    python3 scripts/dayline_legal.py     (이 페이지들만 다시 만들 때)

dayline/<문서>.<언어>.html 의 본문을 dayline/style.css 와 함께 감싸 /dayline/ 아래에 쓴다.
이 본문이 기준이다 — 앱은 글을 따로 싣지 않고 이 주소를 연다.
라이선스는 언어마다 다른 글이 몇 줄뿐이라 본문 하나(dayline/licenses.html)에 dayline/strings.json 의 문구를 채운다.
제목도 strings.json 에 있다.

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

# 언어 순서 — 언어 줄이 이 순서를 따른다. Dayline 앱이 내는 언어와 같고(dayline-android AppLanguage,
# dayline-ios AppLanguage), 앱은 `?lang=` 에 이 태그를 그대로 싣는다. 파일 이름에는 소문자로 쓴다 (privacy.zh-hans.html).
LANGS = [
    ("ko", "한국어"), ("en", "English"), ("ja", "日本語"), ("zh-Hans", "简体中文"), ("zh-Hant", "繁體中文"),
    ("es", "Español"), ("fil", "Filipino"), ("nl", "Nederlands"), ("da", "Dansk"), ("de", "Deutsch"),
    ("ru", "Русский"), ("ar", "العربية"), ("it", "Italiano"), ("id", "Bahasa Indonesia"), ("pt", "Português"),
    ("pl", "Polski"), ("fr", "Français"), ("vi", "Tiếng Việt"),
]
DEFAULT = "en"
# 오른쪽에서 왼쪽으로 읽는 언어
RTL = {"ar"}

# 라이선스는 Waky 처럼 본문 머리(h1) 없이 목록부터 시작한다.
DOCS = ["privacy", "terms", "community", "licenses"]
NO_HEADING = {"licenses"}
# 언어마다 본문을 따로 두지 않고 틀 하나에 strings.json 의 문구를 채우는 문서
TEMPLATED = {"licenses"}


def slug(tag):
    return tag.lower()


def langnav(doc, lang):
    items = [
        f"<strong>{label}</strong>" if tag == lang else f'<a href="{doc}.{slug(tag)}.html">{label}</a>'
        for tag, label in LANGS
    ]
    return f'    <p class="langnav">{" · ".join(items)}</p>'


def head_script(doc, auto):
    """`?theme=light` 면 라이트로. 언어 자동 주소에서는 `?lang=` → 브라우저 언어 순으로 보고
    영어가 아니면 그 언어의 고정 주소로 옮긴다 (밝기는 들고 간다).

    언어 표기는 Waky 서버(zacolabs-backend src/lib/waky/legal/lang.ts normalizeLang)와 같게 읽는다:
    zh-Hans · zh-Hant 는 문자로, 문자가 없으면 지역(TW · HK · MO 는 번체)으로 가리고,
    옛 코드 in · tl 과 지역이 붙은 pt-BR 도 받는다."""
    redirect = ""
    if auto:
        redirect = f'''
        var LANGS = {json.dumps([slug(tag) for tag, _ in LANGS])};
        var OLD = {{ kr: "ko", jp: "ja", "in": "id", tl: "fil" }};
        function norm(v) {{
            v = (v || "").trim().toLowerCase().replace(/_/g, "-");
            if (v === "zh" || v.indexOf("zh-") === 0) {{
                if (v.indexOf("hant") !== -1) return "zh-hant";
                if (v.indexOf("hans") !== -1) return "zh-hans";
                return /-(tw|hk|mo)$/.test(v) ? "zh-hant" : "zh-hans";
            }}
            v = v.split("-")[0];
            v = OLD[v] || v;
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


def body_of(doc, lang, strings):
    if doc not in TEMPLATED:
        with open(os.path.join(SRC, f"{doc}.{slug(lang)}.html"), encoding="utf-8") as f:
            return f.read().rstrip("\n")
    with open(os.path.join(SRC, f"{doc}.html"), encoding="utf-8") as f:
        body = f.read().rstrip("\n")
    for key, text in strings.items():
        body = body.replace("{{" + key + "}}", text)
    if "{{" in body:
        raise SystemExit(f"{doc}.{slug(lang)}: strings.json 에 없는 문구가 있다")
    return body


def page(doc, lang, css, strings, auto=False):
    title = strings[doc]
    body = body_of(doc, lang, strings)
    heading = "" if doc in NO_HEADING else f"    <h1>{html.escape(title)}</h1>\n"
    direction = ' dir="rtl"' if lang in RTL else ""
    return f'''<!DOCTYPE html>
<html lang="{lang}"{direction}>
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
    with open(os.path.join(SRC, "strings.json"), encoding="utf-8") as f:
        strings = json.load(f)
    os.makedirs(OUT, exist_ok=True)
    count = 0
    for doc in DOCS:
        pages = {f"{doc}.{slug(tag)}.html": page(doc, tag, css, strings[slug(tag)]) for tag, _ in LANGS}
        pages[f"{doc}.html"] = page(doc, DEFAULT, css, strings[slug(DEFAULT)], auto=True)
        for name, text in pages.items():
            with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
                f.write(text)
            count += 1
    return count


if __name__ == "__main__":
    print(f"built {build()} dayline legal pages")
