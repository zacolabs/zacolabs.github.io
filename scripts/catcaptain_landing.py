#!/usr/bin/env python3
"""냥반장 랜딩(/catcaptain/)과 공유 링크 페이지(/catcaptain/open/). 문구: catcaptain/ko.json, 모양: catcaptain/style.css.

냥반장은 한국에서만 서비스해서 한국어 한 벌만 만든다. 그림은 catcaptain/prepare_assets.py 가 앱 저장소에서 만든다.

공유 링크: 앱이 공유하는 주소는 /catcaptain/open/?to=<앱 경로> 다 (예: ?to=yarn/user/123).
페이지는 그 경로를 앱 주소 catcaptain://<앱 경로> 로 바꿔
  - 안드로이드: 바로 intent 주소로 앱을 연다 — 앱이 없으면 브라우저가 Google Play(아직 없으면 이 랜딩)로 보낸다
  - 아이폰: 사파리 맨 위에 스마트 앱 배너를 띄운다 — 앱이 있으면 [열기]가 앱 주소를 넘기고, 없으면 [보기]가 App Store 로 간다.
    앱이 없을 때 사파리가 "주소가 유효하지 않음" 창을 띄우지 않게 저절로 열지는 않고, [앱에서 열기] 버튼을 누를 때만 연다
    (버튼은 배너가 뜨지 않는 카카오톡 같은 앱 속 브라우저를 위한 것이기도 하다)
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(__file__).resolve().parent / 'catcaptain'
SITE = 'https://zacolabs.github.io'
PATH = '/catcaptain/'
OPEN_PATH = '/catcaptain/open/'
PACKAGE = 'com.zacolabs.catcaptain'
SCHEME = 'catcaptain'
APPLE_ID = '6824216133'
# 한국 스토어에만 있어 App Store 주소에 /kr/ 를 넣는다 — 나라가 없는 주소는 한국 밖에서 404 다.
APPLE = f'https://apps.apple.com/kr/app/id{APPLE_ID}'
# Play 는 아직 공개 전이다. 공개되면 주소를 넣는다 — 랜딩 · 회사 소개 카드에 Google Play 버튼이 나오고, 공유 링크가 앱이 없을 때 여기로 보낸다.
PLAY = None  # f'https://play.google.com/store/apps/details?id={PACKAGE}'
# 안드로이드에서 Google Play 버튼이 대신 여는 앱 실행 주소 (dayline_landing.APP_LINK_SCRIPT 가 바꾼다)
APP_LINK = f'intent://open#Intent;scheme={SCHEME};package={PACKAGE};end'

PLAY_PATH = "M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.208 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.041 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"
APPLE_PATH = "M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"
# 히어로의 고양이 동그라미: (그림, 왼쪽 %, 위 %, 지름 px). App Store 헤더 그림의 배치를 따른다
HERO_CATS = (('danmuji', 30, 26, 190), ('hotteok', 2, 8, 120), ('kkamang', 66, 2, 128),
             ('tuxedo', 0, 58, 112), ('godeungeo', 72, 62, 104), ('hoejang', 40, 70, 96))


def load():
    return json.loads((SOURCE / 'ko.json').read_text())


def e(value):
    return html.escape(str(value), quote=True)


def store_badges(t, app_link=None):
    """스토어 버튼. Play 주소가 없으면 그 자리에 "출시 예정"을 낸다."""
    apple = (f'<a class="badge" href="{APPLE}" target="_blank" rel="noopener">'
             f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{APPLE_PATH}"/></svg>'
             '<span><small>Download on the</small><strong>App Store</strong></span></a>')
    if PLAY:
        app = f' data-app="{app_link}"' if app_link else ''
        play = (f'<a class="badge" href="{PLAY}"{app} target="_blank" rel="noopener">'
                f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{PLAY_PATH}"/></svg>'
                '<span><small>GET IT ON</small><strong>Google Play</strong></span></a>')
    else:
        play = f'<span class="badge soon">{e(t["playSoon"])}</span>'
    return f'<div class="stores">{apple}{play}</div>'


def head(t, title, description, canonical, robots, extra=''):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#faf6f1">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/zacolabs-assets/catcaptain_icon.png">
<link rel="apple-touch-icon" href="/zacolabs-assets/catcaptain_icon.png">
<link rel="stylesheet" href="/catcaptain/assets/style.css">
<meta name="apple-itunes-app" content="app-id={APPLE_ID}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="냥반장">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta property="og:image" content="{SITE}/catcaptain/assets/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="냥반장 — 동네 고양이, 찍으면 알아봐요">
<meta name="twitter:card" content="summary_large_image">
{extra}</head>
'''


def footer(t):
    return f'''<footer><div class="wrap footer-inner"><span>© 2026 Zaco Labs</span><div class="footer-links">
<a href="/catcaptain/privacy.html">{e(t['privacy'])}</a><a href="/catcaptain/terms.html">{e(t['terms'])}</a><a href="/catcaptain/licenses.html">{e(t['licenses'])}</a><a href="mailto:zaco.labs@gmail.com">{e(t['contact'])}</a><a href="/ko/">{e(t['company'])}</a>
</div></div></footer>
'''


def landing(t):
    canonical = SITE + PATH
    cats = ''.join(
        f'<img class="cat" src="/catcaptain/assets/cat-{name}.webp" alt="" width="{size}" height="{size}" '
        f'style="left:{left}%;top:{top}%;width:{size}px">'
        for name, left, top, size in HERO_CATS)
    features = ''.join(
        f'''<section class="feature{' flip' if i % 2 else ''}"><div class="wrap feature-inner">
<div class="feature-copy"><p class="kicker">{e(kicker)}</p><h2>{title}</h2><p>{e(body)}</p></div>
<img class="shot" src="/catcaptain/assets/shot-{i + 1}.webp" alt="{e(alt)}" width="720" height="854" loading="lazy" decoding="async">
</div></section>
''' for i, (kicker, title, body, alt) in enumerate(t['features']))
    more = ''.join(f'<div class="more-card"><h3>{e(title)}</h3><p>{e(body)}</p></div>' for title, body in t['more'])
    faqs = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t['faqs'])
    graph = {
        '@context': 'https://schema.org', '@graph': [
            {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': t['title'],
             'description': t['description'], 'inLanguage': 'ko',
             'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': canonical + '#app'}},
            {'@type': 'MobileApplication', '@id': canonical + '#app', 'name': '냥반장',
             'alternateName': ['냥반장 - 동네 길고양이 도감', 'Cat Captain'], 'url': canonical,
             'description': t['description'], 'applicationCategory': 'LifestyleApplication',
             'operatingSystem': 'iOS' + (', Android' if PLAY else ''), 'inLanguage': 'ko',
             'image': SITE + '/zacolabs-assets/catcaptain_icon.png',
             'installUrl': [u for u in (APPLE, PLAY) if u],
             'countriesSupported': 'KR',
             'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'KRW'},
             'publisher': {'@id': SITE + '/#organization'}},
            {'@type': 'FAQPage', 'inLanguage': 'ko', 'mainEntity': [
                {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in t['faqs']]},
        ]}
    ld = f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False).replace("<", "&lt;")}</script>\n'
    return head(t, t['title'], t['description'], canonical, 'index,follow,max-image-preview:large', ld) + f'''<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
<header class="top"><div class="wrap top-inner">
<a class="brand" href="{PATH}"><img src="/zacolabs-assets/catcaptain_icon-104.webp" alt="" width="36" height="36"><span>냥반장</span></a>
<nav aria-label="{e(t['navLabel'])}"><a href="#features">{e(t['nav'][0])}</a><a href="#faq">{e(t['nav'][1])}</a></nav>
<a class="top-cta" href="#download">{e(t['download'])}</a>
</div></header>
<main id="main">
<section class="hero"><div class="wrap hero-inner">
<div class="hero-copy"><p class="eyebrow">{e(t['eyebrow'])}</p><h1>{t['headline']}</h1><p class="intro">{e(t['intro'])}</p>{store_badges(t, APP_LINK)}<p class="free">{e(t['free'])}</p></div>
<div class="hero-art" role="img" aria-label="{e(t['heroAlt'])}">{cats}<span class="stamp" aria-hidden="true"><small>냥반장</small><b>{e(t['stamp'])}</b><small class="stamp-date"></small></span></div>
</div></section>
<div id="features">
{features}</div>
<section class="more"><div class="wrap"><h2>{e(t['moreTitle'])}</h2><div class="more-grid">{more}</div></div></section>
<section class="faq" id="faq"><div class="wrap faq-inner"><h2>{e(t['faqTitle'])}</h2>{faqs}</div></section>
<section class="closing" id="download"><div class="wrap closing-inner">
<img src="/zacolabs-assets/catcaptain_icon.png" alt="" width="88" height="88" loading="lazy">
<h2>{t['closing']}</h2><p>{e(t['closingBody'])}</p>{store_badges(t, APP_LINK)}
</div></section>
</main>
{footer(t)}<script>
    (function () {{
        var d = new Date(), s = document.querySelector('.stamp-date');
        if (s) s.textContent = (d.getMonth() + 1) + '.' + d.getDate();
    }})();
</script>
<script>
    if (/Android/i.test(navigator.userAgent)) document.querySelectorAll('a[data-app]').forEach(function (a) {{
        a.href = a.getAttribute('data-app');
        a.removeAttribute('target');
    }});
</script>
</body>
</html>
'''


def open_page(t):
    o = t['open']
    fallback = PLAY or SITE + PATH
    play = (f'<a class="btn line" id="store-play" href="{PLAY}" hidden>{e(o["play"])}</a>' if PLAY
            else f'<span class="btn line soon" id="store-play" hidden>{e(t["playSoon"])}</span>')
    # 사파리의 앱 배너는 페이지를 읽을 때 meta 를 본다 — 머리에서 바로 앱 주소(app-argument)를 붙인다.
    # 앱 경로는 글자 · 숫자 · / _ . ~ = & ? % - 만 받는다 (intent 주소의 # ; 와 스크립트가 끼어들지 못하게)
    early = f'''<script>
    window.CATCAPTAIN_TO = (function () {{
        var to = (new URLSearchParams(location.search).get('to') || '').replace(/^\\/+/, '');
        return /^[A-Za-z0-9][A-Za-z0-9\\/_.~=&?%-]{{0,199}}$/.test(to) ? to : 'open';
    }})();
    document.querySelector('meta[name="apple-itunes-app"]').setAttribute('content',
        'app-id={APPLE_ID}, app-argument={SCHEME}://' + window.CATCAPTAIN_TO);
</script>
'''
    return head(t, o['title'], o['description'], SITE + PATH, 'noindex,follow', early) + f'''<body class="open-body">
<main class="open-card">
<img src="/zacolabs-assets/catcaptain_icon.png" alt="냥반장" width="96" height="96">
<h1>{e(o['heading'])}</h1>
<p id="open-msg">{e(o['body'])}</p>
<div class="open-actions">
<a class="btn" id="open-app" href="{SCHEME}://open">{e(o['openButton'])}</a>
<a class="btn line" id="store-apple" href="{APPLE}">{e(o['appStore'])}</a>
{play}
</div>
<a class="open-about" href="{PATH}">{e(o['about'])}</a>
</main>
<script>
    (function () {{
        var to = window.CATCAPTAIN_TO, deep = '{SCHEME}://' + to;
        var ua = navigator.userAgent;
        var android = /Android/i.test(ua);
        var ios = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        var open = document.getElementById('open-app'), msg = document.getElementById('open-msg');
        var apple = document.getElementById('store-apple'), play = document.getElementById('store-play');
        if (android) {{
            // 앱이 있으면 앱이 열리고, 없으면 브라우저가 fallback 주소(Google Play, 아직 없으면 랜딩)로 간다
            var intent = 'intent://' + to + '#Intent;scheme={SCHEME};package={PACKAGE};S.browser_fallback_url='
                + encodeURIComponent('{fallback}') + ';end';
            open.href = intent;
            msg.textContent = {json.dumps(o['bodyAndroid'], ensure_ascii=False)};
            apple.hidden = true;
            play.hidden = false;
            location.href = intent;
            return;
        }}
        open.href = deep;
        if (ios) {{
            // 시간이 지나면 App Store 로 보내는 방식은 쓰지 않는다 — 사파리가 "냥반장에서 열까요?"를 묻는 동안에도
            // 페이지가 그대로 보여 앱이 있는데도 스토어로 가 버린다. 앱이 없으면 배너의 [보기]나 App Store 버튼으로 간다
            msg.textContent = {json.dumps(o['bodyIos'], ensure_ascii=False)};
            return;
        }}
        // 컴퓨터: 앱을 열 수 없으니 스토어만 보여 준다
        msg.textContent = {json.dumps(o['bodyDesktop'], ensure_ascii=False)};
        open.hidden = true;
        play.hidden = false;
    }})();
</script>
</body>
</html>
'''


def sitemap_urls(today):
    return f'<url><loc>{SITE}{PATH}</loc><lastmod>{today}</lastmod></url>'


def build():
    t = load()
    (ROOT / 'catcaptain/index.html').write_text(landing(t), encoding='utf-8')
    (ROOT / 'catcaptain/open').mkdir(parents=True, exist_ok=True)
    (ROOT / 'catcaptain/open/index.html').write_text(open_page(t), encoding='utf-8')
    (ROOT / 'catcaptain/assets/style.css').write_text((SOURCE / 'style.css').read_text(), encoding='utf-8')
    return 2


if __name__ == '__main__':
    print(f'built {build()} 냥반장 pages')
