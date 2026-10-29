#!/usr/bin/env python3
"""8 Billion marketing pages. Copy: 8billion/<language>.json; design: 8billion/style.css.

Product and art sources: onelife/store/{play,app-store}/listing.md,
app/lib/app/palette.dart, app/assets/branding, tools/branding/rendered_figures.
The generated pages need no build step or network dependency in the browser.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / '8billion'
SITE = 'https://zacolabs.github.io'
LANGS = ('ko', 'en', 'ja', 'zh-hans', 'zh-hant')
LANG_NAMES = dict(zip(LANGS, ('한국어', 'English', '日本語', '简体中文', '繁體中文')))
LANG_TAGS = dict(zip(LANGS, ('ko', 'en', 'ja', 'zh-Hans', 'zh-Hant')))
LOCALES = dict(zip(LANGS, ('ko_KR', 'en_US', 'ja_JP', 'zh_CN', 'zh_TW')))


def landing_path(code):
    return f'/8billion/{code + "/" if code in LANGS and code != "en" else ""}'


def load(code):
    return json.loads((SOURCE / f'{code}.json').read_text())


def e(value):
    return html.escape(str(value), quote=True)


def section_copy(t, key):
    kicker, title, body = t[key]
    return f'<div class="section-copy"><p class="kicker">{e(kicker)}</p><h2>{title}</h2><p>{e(body)}</p></div>'


def person(name, cls=''):
    return f'<img class="person {cls}" src="/8billion/assets/people/{name}.png" alt="" width="96" height="144" loading="lazy">'


def release(t):
    return f'<div class="release"><span class="badge">{e(t["soon"])}</span><span class="platforms">{e(t["platforms"])}</span></div>'


def page(code):
    t = load(code)
    canonical = SITE + landing_path(code)
    company = f'/{code}/' if code != 'en' else '/'
    language_links = ''.join(
        f'<a href="{landing_path(lang)}" data-lang="{lang}" lang="{LANG_TAGS[lang]}" hreflang="{LANG_TAGS[lang]}"'
        + (' aria-current="page"' if lang == code else '') + f'>{LANG_NAMES[lang]}</a>'
        for lang in LANGS)
    locale_alternates = ''.join(
        f'<meta property="og:locale:alternate" content="{LOCALES[lang]}">'
        for lang in LANGS if lang != code)
    rows = ''.join(f'<dt>{e(label)}</dt><dd>{e(value)}</dd>' for label, value in t['birthRows'])
    timeline = ''.join(f'<li><span class="age">{e(age)}</span>{e(text)}</li>' for age, text in t['timeline'])
    stats = ''.join(f'<div class="stat"><span>{e(label)}</span><div class="meter" aria-hidden="true"><span style="width:{value}%"></span></div></div>' for label, value in zip(t['stats'], (72, 58, 81, 64)))
    worlds = []
    for year in (1950, 1975, 2000, 2026, 2050, 2075, 2100, 2125, 2150, 2175, 2200):
        label = t['worldLabels'][1 if year == 2026 else 0 if year < 2026 else 2 if year <= 2100 else 3]
        worlds.append(f'<div class="world{" start" if year == 2026 else ""}"><span class="year">{year}</span><small>{e(label)}</small></div>')
    faqs = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faqs'])
    alternates = ''.join(f'<link rel="alternate" hreflang="{LANG_TAGS[lang]}" href="{SITE}{landing_path(lang)}">' for lang in LANGS)
    graph = {
        '@context': 'https://schema.org', '@graph': [
            {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical,
             'name': t['title'], 'description': t['description'], 'inLanguage': LANG_TAGS[code],
             'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/8billion/#app'}},
            {'@type': 'VideoGame', '@id': SITE + '/8billion/#app', 'name': '8 Billion: Another Life',
             'url': SITE + '/8billion/', 'description': t['description'], 'genre': 'Life simulation',
             'gamePlatform': ['iOS', 'Android'], 'inLanguage': list(LANG_TAGS.values()),
             'applicationCategory': 'GameApplication', 'operatingSystem': 'Android, iOS',
             'image': SITE + '/zacolabs-assets/8billion_icon.png', 'isAccessibleForFree': True,
             # 무료로 시작하고, 광고를 보거나 프리미엄을 한 번 사서 세계를 연다 (FAQ 와 같다)
             'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
             'publisher': {'@id': SITE + '/#organization'}, 'author': {'@id': SITE + '/#organization'}},
            # @id 는 한 페이지 안에서만 풀리므로, Dayline 랜딩처럼 조직 · 사이트 노드를 함께 싣는다
            {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'Zaco Labs', 'url': SITE + '/',
             'logo': {'@type': 'ImageObject', 'url': SITE + '/zacolabs-assets/logo.png'}, 'email': 'zaco.labs@gmail.com'},
            {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Zaco Labs',
             'publisher': {'@id': SITE + '/#organization'}},
            {'@type': 'FAQPage', 'inLanguage': LANG_TAGS[code], 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in t['faqs']]},
        ]}
    return f'''<!doctype html>
<html lang="{LANG_TAGS[code]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="/8billion/assets/language.js"></script>
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['description'])}">
<meta name="theme-color" content="#0b1026">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canonical}">
{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}/8billion/">
<link rel="icon" href="/zacolabs-assets/8billion_icon.png">
<link rel="stylesheet" href="/8billion/assets/style.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="8 Billion: Another Life">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{LOCALES[code]}">
{locale_alternates}
<meta property="og:image" content="{SITE}/8billion/assets/og.webp">
<meta property="og:image:width" content="1024"><meta property="og:image:height" content="500">
<meta property="og:image:alt" content="8 Billion: Another Life — One life among eight billion">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False).replace('<', '&lt;')}</script>
</head>
<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
<header><div class="wrap header-inner">
<a class="brand" href="{landing_path(code)}"><img src="/zacolabs-assets/8billion_icon.png" alt="" width="38" height="38"><span>8 Billion<small>ANOTHER LIFE</small></span></a>
<nav aria-label="{e(t['navLabel'])}"><a href="#life">{e(t['nav'][0])}</a><a href="#worlds">{e(t['nav'][1])}</a><a href="#faq">{e(t['nav'][2])}</a></nav>
<details class="languages"><summary>{LANG_NAMES[code]} <span aria-hidden="true">⌄</span></summary><div class="language-menu"><a href="/8billion/" data-lang="system">{e(t['systemLanguage'])}</a>{language_links}</div></details>
</div></header>
<main id="main">
<section class="wrap hero">
<div><p class="eyebrow">{e(t['eyebrow'])}</p><h1>{t['headline']}</h1><p class="intro">{t['intro']}</p>{release(t)}<a class="explore" href="#life">{e(t['explore'])}</a></div>
<figure class="hero-art"><img src="/8billion/assets/hero.webp" width="1024" height="1024" alt="{e(t['heroAlt'])}" fetchpriority="high"><figcaption>{e(t['caption'])}</figcaption></figure>
</section>
<section class="section" id="life"><div class="wrap split">
{section_copy(t, 'birth')}
<div><div class="panel"><p class="panel-label pixel">One in 8 Billion</p><div class="birth-content">{person('baby-female-0', 'baby')}<dl>{rows}</dl></div><p class="birth-question">{e(t['birthQuestion'])}</p></div><p class="sample">{e(t['sample'])}</p></div>
</div></section>
<section class="section moments"><div class="wrap split"><ol class="timeline">{timeline}</ol>{section_copy(t, 'moments')}</div></section>
<section class="section"><div class="wrap"><div class="split">
{section_copy(t, 'choice')}
<div><div class="choice-scene" aria-hidden="true">{person('adult-female-1')}{person('adult-male-0')}{person('elder-female-0')}</div><div class="panel"><p class="panel-label pixel">{e(t['choiceAge'])}</p><p class="choice-prompt">{e(t['choicePrompt'])}</p><div class="option">{e(t['choiceOptions'][0])}</div><div class="option">{e(t['choiceOptions'][1])}</div></div><p class="choice-note">{e(t['choiceNote'])}</p></div>
</div><div class="stats"><div><h3>{e(t['statsTitle'])}</h3><p>{e(t['statsBody'])}</p></div><div>{stats}</div></div></div></section>
<section class="section worlds" id="worlds"><div class="wrap"><div class="world-heading"><div><p class="kicker">{e(t['worlds'][0])}</p><h2>{t['worlds'][1]}</h2></div><p>{e(t['worlds'][2])}</p></div><div class="world-grid">{''.join(worlds)}</div><p class="world-note">{e(t['worldNote'])}</p></div></section>
<section class="section"><div class="wrap split">{section_copy(t, 'archive')}<div class="archive-art" aria-hidden="true">{person('baby-female-0')}{person('child-female-0')}{person('adult-female-1')}{person('elder-female-0')}</div></div></section>
<section class="section" id="faq"><div class="wrap"><div class="faq-wrap"><h2>{e(t['faqTitle'])}</h2>{faqs}</div></div></section>
<section class="wrap closing">{person('adult-male-0')}<h2 class="closing-title">{t['closing']}</h2><p>{e(t['closingBody'])}</p>{release(t)}</section>
</main>
<footer><div class="wrap footer-inner"><span>© 2026 Zaco Labs</span><div class="footer-links"><a href="/8billion/privacy.html">{e(t['privacy'])}</a><a href="mailto:zaco.labs@gmail.com">{e(t['contact'])}</a><a href="{company}">{e(t['company'])}</a></div></div></footer>
</body>
</html>
'''


def sitemap_urls(today):
    links = ''.join(f'<xhtml:link rel="alternate" hreflang="{LANG_TAGS[code]}" href="{SITE}{landing_path(code)}" />' for code in LANGS)
    links += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/8billion/" />'
    return '\n'.join(f'<url><loc>{SITE}{landing_path(code)}</loc><lastmod>{today}</lastmod>{links}</url>' for code in LANGS)


def build():
    keys = set(load('en'))
    for code in LANGS:
        if set(load(code)) != keys:
            raise ValueError(f'{code}: translation keys do not match English')
        path = ROOT / landing_path(code).lstrip('/') / 'index.html'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page(code), encoding='utf-8')
    (ROOT / '8billion/assets/style.css').write_text((SOURCE / 'style.css').read_text(), encoding='utf-8')
    (ROOT / '8billion/assets/language.js').write_text((SOURCE / 'language.js').read_text(), encoding='utf-8')
    return len(LANGS)


if __name__ == '__main__':
    print(f'built {build()} 8 Billion landing pages')
