#!/usr/bin/env python3
"""Dayline 의 "Google 지도 타임라인 대안" 페이지 (/dayline/<언어>/google-timeline-alternative/).

Google 지도 타임라인이 휴대폰 저장 방식으로 바뀌고 웹에서 빠진 뒤로 대안을 찾는 검색이 많아,
무엇이 바뀌었는지 · 대안에서 볼 것 · Dayline 이 어떻게 하는지를 한 장에 적는다.

- 문구: scripts/dayline/timeline/<언어>.json (이 페이지에만 있는 글)
- Dayline 의 기능 설명 · FAQ · 스토어 버튼 · 모양은 랜딩(dayline_landing.py)의 것을 그대로 쓴다.
  Dayline 에 대한 글은 랜딩과 한 군데에서만 고친다
- Google 쪽 설명은 Google 지도 고객센터의 "Google 지도 타임라인 관리"에 적힌 것만 쓴다 (SOURCE)
- 랜딩과 같은 18개 언어. 언어를 늘리면 랜딩 · 이 페이지의 문구를 함께 더한다
"""
import json
import os

import dayline_landing as dl

SRC = os.path.join(dl.HERE, "dayline", "timeline")
SLUG = "google-timeline-alternative"
# Google 지도 고객센터: 타임라인 관리. hl 은 그 언어의 고객센터 언어
SOURCE = "https://support.google.com/maps/answer/6258979"
HELP_LANG = {"ko": "ko", "en": "en", "ja": "ja", "zh-hans": "zh-Hans", "zh-hant": "zh-Hant", "es": "es",
             "fr": "fr", "de": "de", "it": "it", "pt": "pt-BR", "nl": "nl", "da": "da", "pl": "pl", "ru": "ru",
             "ar": "ar", "id": "id", "vi": "vi", "fil": "fil"}
# 랜딩 FAQ 중 옮겨 오는 사람이 묻는 것: 앱을 닫아도 되나 · 배터리 · 서버로 가나
FAQ_PICK = (1, 3, 4)
TITLE_MAX, DESC_MAX = 60, 160
e = dl.e


def path(code):
    return f"/dayline/{code}/{SLUG}/"


def url(code):
    return dl.SITE + path(code)


def load(code):
    """랜딩 문구(dl.load) 위에 이 페이지의 문구를 얹는다. 겹치는 키는 이 페이지 것이 이긴다."""
    d = dl.load(code)
    with open(os.path.join(SRC, f"{code}.json"), encoding="utf-8") as f:
        d["tl"] = json.load(f)
    return d


def codes():
    return [c for c in dl.codes() if os.path.exists(os.path.join(SRC, f"{c}.json"))]


def lang_link(d, cur_attr):
    return (f'<a href="{path(d["code"])}" lang="{d["html_lang"]}" hreflang="{d["hreflang"]}"'
            f' data-lang="{d["code"]}"{cur_attr}>{e(d["label"])}</a>')


def lang_menu(cur, langs):
    here = next(d for d in langs if d["code"] == cur)
    items = "\n".join(
        "                <li>" + lang_link(d, ' aria-current="page"' if d["code"] == cur else "") + "</li>"
        for d in langs)
    return f'''<details class="lang-menu">
            <summary aria-label="Language">{dl.GLOBE}<span>{e(here["label"])}</span></summary>
            <ul>
{items}
            </ul>
        </details>'''


def langnav(cur, langs):
    links = [lang_link(d, ' class="on"' if d["code"] == cur else "") for d in langs]
    return '<nav class="langs" aria-label="Language">' + "\n            ".join(links) + "</nav>"


def alternates(langs):
    rows = [f'<link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x["code"])}" />' for x in langs]
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{url(dl.DEFAULT)}" />')
    return "\n".join(rows)


# 랜딩의 PAGE_SCRIPT 는 하루 화면(.day)을 움직이는데 이 페이지에는 없어, 언어 기억 · 메뉴 닫기만 따로 둔다
PAGE_SCRIPT = f"""<script>
    document.getElementById('year').textContent = new Date().getFullYear();
    (function () {{
        document.querySelectorAll('a[data-lang]').forEach(function (a) {{
            a.addEventListener('click', function () {{
                try {{ localStorage.setItem('{dl.STORAGE_KEY}', a.getAttribute('data-lang')); }} catch (err) {{}}
            }});
        }});
        var menu = document.querySelector('.lang-menu');
        document.addEventListener('click', function (ev) {{
            if (menu.open && !menu.contains(ev.target)) menu.open = false;
        }});
        document.addEventListener('keydown', function (ev) {{
            if (ev.key === 'Escape') menu.open = false;
        }});
    }})();
</script>"""

# 이 페이지에만 있는 모양 (비교표 · 목록). 나머지는 랜딩 style.css
EXTRA_CSS = """
    .article > * { max-width:46em; }
    .article p + p, .article h2 + p { margin-top:14px; }
    .article p { font-size:16.5px; }
    .glance-wrap { margin-top:28px; overflow-x:auto; }
    .glance { width:100%; border-collapse:separate; border-spacing:0; background:var(--card); border-radius:var(--radius); overflow:hidden; font-size:15.5px;
        border:var(--edge) solid var(--ink); box-shadow:4px 4px 0 var(--ink); }
    .glance th, .glance td { padding:14px 18px; text-align:start; vertical-align:top; }
    .glance thead th { background:var(--ink); color:#fff; font-weight:700; }
    .glance tbody tr + tr th, .glance tbody tr + tr td { border-top:1.5px solid var(--divider); }
    .glance tbody th { font-weight:700; width:30%; }
    .glance-note { margin-top:12px; font-size:14px; color:var(--muted); }
    .plain-list { margin-top:22px; padding-inline-start:1.2em; }
    .plain-list li { font-size:16.5px; }
    .plain-list li + li { margin-top:10px; }
    .crumbs { padding-top:28px; font-size:14px; color:var(--muted); }
    .crumbs a, .article a, .more a { text-decoration:underline; text-underline-offset:3px; }
    .hero-text { padding-top:24px; }
    .more { margin-top:26px; font-weight:700; }
"""


def page(d, langs, css, legal):
    code, t = d["code"], d["tl"]
    canon = dl.SITE + path(code)
    landing = dl.url(code)
    home = dl.SITE + ("/" if code == dl.DEFAULT else f"/{code}/")
    org, site = f"{dl.SITE}/#organization", f"{dl.SITE}/#website"
    og_image = f"{dl.SITE}{dl.ASSETS}/{dl.og_name(code)}"
    source = f"{SOURCE}?hl={HELP_LANG[code]}"
    faqs = [d["faqs"][i] for i in FAQ_PICK]
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": org, "name": "Zaco Labs", "url": dl.SITE + "/",
         "logo": {"@type": "ImageObject", "url": f"{dl.SITE}/zacolabs-assets/logo.png"},
         "email": "zaco.labs@gmail.com"},
        {"@type": "WebSite", "@id": site, "url": dl.SITE + "/", "name": "Zaco Labs", "publisher": {"@id": org}},
        {"@type": "WebPage", "@id": canon + "#webpage", "url": canon, "name": t["title"],
         "description": t["description"], "inLanguage": d["html_lang"], "isPartOf": {"@id": site},
         "about": {"@id": landing + "#app"}, "breadcrumb": {"@id": canon + "#breadcrumb"},
         "citation": source, "publisher": {"@id": org},
         "primaryImageOfPage": {"@type": "ImageObject", "url": og_image, "width": 1200, "height": 630}},
        {"@type": "BreadcrumbList", "@id": canon + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Zaco Labs", "item": home},
            {"@type": "ListItem", "position": 2, "name": "Dayline", "item": landing},
            {"@type": "ListItem", "position": 3, "name": t["crumb"], "item": canon}]},
        # 앱 자체는 랜딩이 자세히 적는다. 여기서는 같은 @id 로 가리키며 이름 · 종류만 싣는다
        {"@type": "MobileApplication", "@id": landing + "#app", "name": "Dayline", "url": landing,
         "applicationCategory": "LifestyleApplication", "operatingSystem": "Android, iOS",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": d["currency"]},
         "publisher": {"@id": org}},
    ]}
    locales = "\n".join(f'<meta property="og:locale:alternate" content="{x["og_locale"]}" />'
                        for x in langs if x["code"] != code)
    app_banner = f'\n<meta name="apple-itunes-app" content="app-id={dl.APPLE_ID}" />' if dl.APPLE_ID else ""
    changed = "\n".join(f"            <p>{e(p)}</p>" for p in t["changed"])
    head = "".join(f'<th scope="col">{e(h)}</th>' for h in t["glance_head"])
    rows = "\n".join(
        f'                    <tr><th scope="row">{e(r[0])}</th><td>{e(r[1])}</td><td>{e(r[2])}</td></tr>'
        for r in t["glance_rows"])
    feats = "\n".join(
        f'''                <li>
                    <h3>{e(f["title"])}</h3>
                    <p>{e(f["text"])}</p>
                </li>''' for f in d["features"])
    limits = "\n".join(f"                <li>{e(x)}</li>" for x in t["limits"])
    faq_html = "\n".join(
        f'''                <details>
                    <summary>{e(f["q"])}</summary>
                    <div class="answer">{e(f["a"])}</div>
                </details>''' for f in faqs)
    dir_attr = ' dir="rtl"' if d["dir"] == "rtl" else ""
    return f'''<!DOCTYPE html>
<html lang="{d["html_lang"]}"{dir_attr}>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["description"])}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<meta name="author" content="Zaco Labs" />{app_banner}
<meta name="theme-color" content="#ffffff" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Dayline" />
<meta property="og:locale" content="{d["og_locale"]}" />
{locales}
<meta property="og:title" content="{e(t["title"])}" />
<meta property="og:description" content="{e(t["description"])}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{e(t["title"])}" />
<meta name="twitter:description" content="{e(t["description"])}" />
<meta name="twitter:image" content="{og_image}" />
<link rel="icon" href="{dl.ICON}" />
<link rel="apple-touch-icon" href="{dl.ICON}" />
<link rel="canonical" href="{canon}" />
{alternates(langs)}
{dl.ld(graph)}
<style>{css.replace("{{FONT}}", d["font"])}{EXTRA_CSS}</style>
</head>
<body>

<header class="site">
    <div class="wrap">
        <a class="brand" href="{dl.path(code)}">
            <img src="{dl.ICON}" alt="" width="30" height="30" />
            <span>Dayline</span>
        </a>
        {lang_menu(code, langs)}
    </div>
</header>

<main>
    <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="{home[len(dl.SITE):]}">Zaco Labs</a> › <a href="{dl.path(code)}">Dayline</a> › {e(t["crumb"])}</nav>

        <section class="hero-text article">
            <h1>{e(t["h1"])}</h1>
            <p class="lede">{e(t["lede"])}</p>
        </section>

        <section class="article">
            <h2>{e(t["changed_title"])}</h2>
{changed}
        </section>

        <section>
            <h2>{e(t["glance_title"])}</h2>
            <div class="glance-wrap">
                <table class="glance">
                    <thead><tr>{head}</tr></thead>
                    <tbody>
{rows}
                    </tbody>
                </table>
            </div>
            <p class="glance-note">{e(t["glance_note"])}</p>
        </section>

        <section>
            <h2>{e(t["how_title"])}</h2>
            <p class="section-lede">{e(t["how_lede"])}</p>
            <ul class="feature-list">
{feats}
            </ul>
            <p class="more"><a href="{dl.path(code)}">{e(t["more"])}</a></p>
        </section>

        <section class="article">
            <h2>{e(t["limits_title"])}</h2>
            <ul class="plain-list">
{limits}
            </ul>
        </section>

        <section id="faq">
            <h2>{e(d["faq_title"])}</h2>
            <div class="faq-list">
{faq_html}
            </div>
        </section>

        <section class="article">
            <h2>{e(t["sources_title"])}</h2>
            <ul class="plain-list">
                <li><a href="{source}" target="_blank" rel="noopener">{e(t["source_label"])}</a></li>
            </ul>
        </section>
    </div>

    <section class="cta">
        <div class="wrap">
            <h2>{e(d["cta_title"])}</h2>
            <p>{e(d["cta_text"])}</p>
            {dl.badges(d)}
        </div>
    </section>
</main>

<footer class="site">
    <div class="wrap">
        <div class="row"><a href="/dayline/privacy.{code}.html">{e(legal["privacy"])}</a> · <a href="/dayline/terms.{code}.html">{e(legal["terms"])}</a> · <a href="/dayline/community.{code}.html">{e(legal["community"])}</a></div>
        <div class="row"><a href="/">{e(d["about_link"])}</a> · <a href="mailto:zaco.labs@gmail.com">zaco.labs@gmail.com</a></div>
        <div class="row">© <span id="year">2026</span> Zaco Labs. {e(d["rights"])}</div>
        {langnav(code, langs)}
    </div>
</footer>

{PAGE_SCRIPT}
{dl.APP_LINK_SCRIPT}
</body>
</html>
'''


def check(langs):
    keys = set(next(x for x in langs if x["code"] == dl.DEFAULT)["tl"])
    for d in langs:
        t = d["tl"]
        missing = keys - set(t)
        if missing:
            raise SystemExit(f"dayline/timeline/{d['code']}.json 에 빠진 문구: {', '.join(sorted(missing))}")
        # 검색결과에서 잘리지 않게
        if len(t["title"]) > TITLE_MAX or len(t["description"]) > DESC_MAX:
            raise SystemExit(f"dayline/timeline/{d['code']}.json: title {len(t['title'])}자 · "
                             f"description {len(t['description'])}자 (최대 {TITLE_MAX} · {DESC_MAX})")
        if len(t["glance_head"]) != 3 or any(len(r) != 3 for r in t["glance_rows"]):
            raise SystemExit(f"dayline/timeline/{d['code']}.json: 비교표는 세 칸이다")


def sitemap_urls(today):
    """dayline_landing.sitemap_urls 가 같이 싣는다."""
    langs = [load(c) for c in codes()]
    links = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x["code"])}" />' for x in langs
    ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url(dl.DEFAULT)}" />'
    return "\n".join(f'''  <url>
    <loc>{url(x["code"])}</loc>
    <lastmod>{today}</lastmod>
{links}
  </url>''' for x in langs)


def llms_link():
    """llms.txt 의 한 줄."""
    t = load(dl.DEFAULT)["tl"]
    return f"- [{t['title']}]({url(dl.DEFAULT)}): {t['description']}"


def build():
    langs = [load(c) for c in codes()]
    check(langs)
    with open(os.path.join(dl.SRC, "style.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(dl.HERE, "dayline", "strings.json"), encoding="utf-8") as f:
        legal = json.load(f)
    for d in langs:
        out = os.path.join(dl.OUT, d["code"], SLUG)
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(d, langs, css, legal[d["code"]]))
    return len(langs)


if __name__ == "__main__":
    print(f"built {build()} dayline timeline pages")
