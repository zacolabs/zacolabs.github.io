#!/usr/bin/env python3
"""Dayline 랜딩 페이지 생성기. build.py 가 같이 돌린다.

    python3 scripts/dayline_landing.py     (랜딩만 다시 만들 때)

dayline/landing/i18n/<언어>.json 의 문구로 /dayline/<언어>/index.html 을 만들고,
/dayline/ 에는 브라우저 언어에 맞는 랜딩으로 보내는 진입 페이지를 둔다.
문구는 JSON 에서, 모양은 dayline/landing/style.css 에서만 고친다.

구성은 Waky 랜딩(waky-landing scripts/landing/build.py)을 따른다: 히어로 · 기능 · 3컷 · FAQ · CTA.
모양은 앱의 것이다: 검은 테두리와 딱딱한 그림자의 흰 카드. 앱의 노란 바탕은 앱 화면 안과 버튼에만 쓴다.
언어 이름 · 로케일 · 글꼴은 회사 소개의 i18n(scripts/i18n/<언어>.json)에서 가져온다.
문구 파일이 있는 언어만 만든다 — 없는 언어로 온 사람은 영어로 간다.
"""
import html
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(HERE, "dayline", "landing")
OUT = os.path.join(ROOT, "dayline")
SITE = "https://zacolabs.github.io"
BASE = f"{SITE}/dayline"
ASSETS = "/dayline/assets"
ICON = "/zacolabs-assets/dayline_icon.png"

# 언어 순서 — 회사 소개(build.py ORDER)와 같다. 문구 파일이 있는 것만 쓴다.
ORDER = ["ko", "en", "ja", "zh-hans", "zh-hant", "es", "fr", "de", "it", "pt",
         "nl", "da", "pl", "ru", "ar", "id", "vi", "fil"]
DEFAULT = "en"  # x-default
# 고른 언어를 기억하는 localStorage 키. 회사 소개와 같이 쓴다 (같은 도메인, 같은 언어 코드).
STORAGE_KEY = "zacolabs-lang"

# Play 는 패키지 이름으로 주소가 정해진다. App Store 는 번들 ID 로는 주소를 만들 수 없고
# App Store Connect 의 Apple ID(앱 정보 → 일반 정보의 숫자)가 있어야 한다. None 이면 버튼이 "출시 예정"으로 나온다.
PACKAGE = "com.zacolabs.dayline"
PLAY = f"https://play.google.com/store/apps/details?id={PACKAGE}"
APPLE_ID = "6818821647"
APPLE = f"https://apps.apple.com/app/id{APPLE_ID}" if APPLE_ID else None

PLAY_PATH = "M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.208 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.041 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"
APPLE_PATH = "M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"
GLOBE = ('<svg class="globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
         'aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9'
         's-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>')


def load_art():
    """그림 위에 얹는 선을 만드는 모듈 (dayline/landing/art.py)."""
    spec = importlib.util.spec_from_file_location("dayline_art", os.path.join(SRC, "art.py"))
    art = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(art)
    return art


ART = load_art()
# 그림의 픽셀 크기 (dayline/assets/illustration/*.webp)
HERO_SIZE = 1000
STEP_SIZE = 800


def art(name, alt, size, attrs):
    """먹선 그림과 그 위에 얹는 색 선. 화면에 들어오면 선이 그려진다."""
    return (f'<div class="art" data-inview><img src="{ASSETS}/illustration/{name}.webp" alt="{e(alt)}" '
            f'width="{size}" height="{size}" {attrs} />{ART.overlay(name)}</div>')


def e(s):
    return html.escape(s, quote=True)


def codes():
    return [c for c in ORDER if os.path.exists(os.path.join(SRC, "i18n", f"{c}.json"))]


def load(code):
    """랜딩 문구에 회사 소개 i18n 의 언어 이름 · 로케일 · 글꼴을 더한다."""
    with open(os.path.join(HERE, "i18n", f"{code}.json"), encoding="utf-8") as f:
        base = json.load(f)
    with open(os.path.join(SRC, "i18n", f"{code}.json"), encoding="utf-8") as f:
        d = json.load(f)
    for key in ("label", "html_lang", "hreflang", "dir", "og_locale", "font", "rights"):
        d[key] = base[key]
    d["code"] = code
    return d


def path(code):
    return f"/dayline/{code}/"


def url(code):
    return SITE + path(code)


def landing_path(code):
    """회사 소개의 카드가 거는 주소: 그 언어의 랜딩, 아직 없으면 영어."""
    return path(code if code in codes() else DEFAULT)


# ── 하루 화면 ───────────────────────────────────────────────────────
# 앱의 화면을 그림 파일이 아니라 HTML · SVG 로 그린다 — 화면에 들어올 때 선이 그려지게 하려고.
# 앱이 그리는 대로다(dayline-ios DesignSystem/PopLook.swift): 노란 바탕 위에 검은 테두리와 딱딱한 그림자의
# 흰 카드 셋 — 거리, 크림색 격자 판 위의 선, 이동수단별 나눔. 길과 거리는 스토어 그림의 것이다.
MODES = ["walking", "running", "cycling", "vehicle"]
MODE_COLOR = {"walking": "#00c97b", "running": "#ff4d26", "cycling": "#8a66ff", "vehicle": "#0a8fff"}
# 아이콘 밑의 원을 채우는 색: 검은 아이콘이 읽히게 밝힌 것
MODE_TILE = {"walking": "#00c97b", "running": "#ff7a5c", "cycling": "#b39dff", "vehicle": "#6fc1ff"}
MODE_KM = [3.1, 2.8, 7.4, 18.6]
# 이동수단 아이콘. Tabler Icons(MIT)의 walk · run · bike · car.
MODE_ICON = {
    "walking": '<path d="M12 4a1 1 0 1 0 2 0a1 1 0 1 0 -2 0"/><path d="M7 21l3 -4"/><path d="M16 21l-2 -4l-3 -3l1 -6"/><path d="M6 12l2 -3l4 -1l3 3l3 1"/>',
    "running": '<path d="M12 4a1 1 0 1 0 2 0a1 1 0 1 0 -2 0"/><path d="M4 17l5 1l.75 -1.5"/><path d="M15 21l0 -4l-4 -3l1 -6"/><path d="M7 12l0 -3l5 -1l3 3l3 1"/>',
    "cycling": '<path d="M2 18a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"/><path d="M16 18a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"/><path d="M12 19l0 -4l-3 -3l5 -4l2 3l3 0"/><path d="M16 5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0"/>',
    "vehicle": '<path d="M5 17a2 2 0 1 0 4 0a2 2 0 1 0 -4 0"/><path d="M15 17a2 2 0 1 0 4 0a2 2 0 1 0 -4 0"/><path d="M5 17h-2v-6l2 -5h9l4 5h1a2 2 0 0 1 2 2v4h-2m-4 0h-6m-6 -6h15m-6 0v-5"/>',
}
# 가 본 적 없는 하루, 100x100 위에: 걷고, 차를 타고, 자전거를 타고, 달려서 돌아온다.
ROUTE = [(12, 84), (17, 76), (25, 73), (23, 64), (31, 59), (41, 55), (52, 53), (60, 44), (65, 31), (74, 24),
         (83, 21), (90, 29), (87, 40), (78, 45), (70, 50), (64, 58), (69, 67), (79, 71), (86, 78)]
LEGS = [("walking", 0, 4), ("vehicle", 4, 9), ("cycling", 9, 13), ("running", 13, 18)]
DAY_W, DAY_H, DAY_LINE = 788, 660, 14
DAY_DRAW = 2.8  # 선을 다 그리는 데 걸리는 초
# 소수점을 쉼표로 쓰는 언어
DECIMAL_COMMA = {"es", "fr", "de", "it", "pt", "nl", "da", "pl", "ru", "id", "vi"}


def number(n, code):
    return f"{n:.1f}".replace(".", "," if code in DECIMAL_COMMA else ".")


def curve(pts, a, b):
    """pts 의 a 에서 b 까지를 지나는 곡선. 접선에 양쪽 이웃을 써서 구간이 매끄럽게 이어진다."""
    d = f"M{pts[a][0]:.1f},{pts[a][1]:.1f}"
    for i in range(a, b):
        p0, p1, p2 = pts[i - 1] if i else pts[i], pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        d += (f" C{p1[0] + (p2[0] - p0[0]) / 6:.1f},{p1[1] + (p2[1] - p0[1]) / 6:.1f}"
              f" {p2[0] - (p3[0] - p1[0]) / 6:.1f},{p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return d


def day_card(d):
    """하루 화면. 구간마다 그려지는 때(--d)와 걸리는 시간(--t)을 길이에 맞춰 준다 — 선이 같은 빠르기로 이어지게."""
    code, t = d["code"], d["day"]
    w, h, line = DAY_W, DAY_H, DAY_LINE
    ink, edge = ART.INK, DAY_LINE + 13  # 선을 두르는 검은 테두리의 굵기
    xs, ys, pad = [p[0] for p in ROUTE], [p[1] for p in ROUTE], line * 3.4
    x0, y0, rw, rh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    k = min((w - pad * 2) / rw, (h - pad * 2) / rh)
    ox, oy = (w - rw * k) / 2, (h - rh * k) / 2
    pts = [(ox + (x - x0) * k, oy + (y - y0) * k) for x, y in ROUTE]

    def length(a, b):
        return sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** .5 for i in range(a, b))

    total = length(0, len(pts) - 1)
    timing, at = {}, 0.0
    edges = colors = ""
    for mode, a, b in LEGS:
        took = DAY_DRAW * length(a, b) / total
        timing[mode] = f"--d:{at:.2f}s;--t:{took:.2f}s"
        path = f'pathLength="1" style="{timing[mode]}" d="{curve(pts, a, b)}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
        edges += f'<path class="leg" {path} stroke="{ink}" stroke-width="{edge}"/>'
        colors += f'<path class="leg" {path} stroke="{MODE_COLOR[mode]}" stroke-width="{line}"/>'
        at += took
    step = w / 6
    grid = "".join(f'<path d="M{x * step:.1f} 0V{h}"/>' for x in range(1, 6))
    grid += "".join(f'<path d="M0 {y * step:.1f}H{w}"/>' for y in range(1, int(h / step) + 1))
    (sx, sy), (ex, ey) = pts[0], pts[-1]
    canvas = f"""<svg class="day-canvas" viewBox="0 0 {w} {h}" aria-hidden="true">
                            <g stroke="{ART.GRID}" stroke-width="3">{grid}</g>
                            {edges}
                            {colors}
                            <circle class="pin" cx="{sx:.1f}" cy="{sy:.1f}" r="{line * 1.2:.1f}" fill="#fff" stroke="{ink}" stroke-width="{line * .62:.1f}"/>
                            <circle class="pin" style="--d:{DAY_DRAW:.2f}s" cx="{ex:.1f}" cy="{ey:.1f}" r="{line * 1.2:.1f}" fill="{ART.PAGE}" stroke="{ink}" stroke-width="{line * .62:.1f}"/>
                        </svg>"""
    bar = "".join(f'<i style="flex:{km};background:{MODE_COLOR[m]};{timing[m]}"></i>' for m, km in zip(MODES, MODE_KM))
    modes = "\n".join(
        f'                            <div class="day-mode" style="{timing[m]}"><i style="background:{MODE_TILE[m]}">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="{ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{MODE_ICON[m]}</svg></i>'
        f'<b>{number(MODE_KM[i], code)}</b><span>{e(t["times"][i])}</span><span class="sr">{e(t["names"][i])}</span></div>'
        for i, m in enumerate(MODES))
    return f"""<div class="day" role="img" aria-label="{e(d["shot_alt"])}" data-inview data-draw="{DAY_DRAW}">
                    <div class="day-card day-total">
                        <p><b data-count="{sum(MODE_KM):.1f}">{number(sum(MODE_KM), code)}</b><span>{e(t["km"])}</span></p>
                        <p class="day-sub">{e(t["moving"])}</p>
                    </div>
                    <div class="day-card day-path">
                        {canvas}
                    </div>
                    <div class="day-card day-stats">
                        <div class="day-bar">{bar}</div>
                        <div class="day-modes">
{modes}
                        </div>
                    </div>
                </div>"""


def og_name(code):
    """언어별 공유 미리보기 그림(make_assets.py)이 아직 없으면 영어 것을 쓴다."""
    name = f"og-{code}.png"
    return name if os.path.exists(os.path.join(OUT, "assets", name)) else f"og-{DEFAULT}.png"


def badges(d):
    play = f'''<a class="badge" href="{PLAY}" target="_blank" rel="noopener">
                    <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{PLAY_PATH}"/></svg>
                    <span class="badge-txt"><small>GET IT ON</small><strong>Google Play</strong></span>
                </a>'''
    if APPLE:
        apple = f'''<a class="badge" href="{APPLE}" target="_blank" rel="noopener">
                    <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{APPLE_PATH}"/></svg>
                    <span class="badge-txt"><small>Download on the</small><strong>App Store</strong></span>
                </a>'''
    else:
        apple = f'''<span class="badge badge-soon">
                    <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{APPLE_PATH}"/></svg>
                    <span class="badge-txt"><small>{e(d["soon"])}</small><strong>App Store</strong></span>
                </span>'''
    return f'''<div class="stores">
                {play}
                {apple}
            </div>'''


def lang_link(d, cur_attr):
    return (f'<a href="{path(d["code"])}" lang="{d["html_lang"]}" hreflang="{d["hreflang"]}"'
            f' data-lang="{d["code"]}"{cur_attr}>{e(d["label"])}</a>')


def langnav(cur, langs):
    """푸터: 모든 언어를 일반 링크로 나열 (크롤러가 따라갈 수 있게)."""
    links = [lang_link(d, ' class="on"' if d["code"] == cur else "") for d in langs]
    return '<nav class="langs" aria-label="Language">' + "\n            ".join(links) + "</nav>"


def lang_menu(cur, langs):
    """헤더: 현재 언어를 보여 주는 드롭다운."""
    here = next(d for d in langs if d["code"] == cur)
    items = "\n".join(
        "                <li>" + lang_link(d, ' aria-current="page"' if d["code"] == cur else "") + "</li>"
        for d in langs)
    return f'''<details class="lang-menu">
            <summary aria-label="Language">{GLOBE}<span>{e(here["label"])}</span></summary>
            <ul>
{items}
            </ul>
        </details>'''


PAGE_SCRIPT = f"""<script>
    document.getElementById('year').textContent = new Date().getFullYear();
    (function () {{
        // 직접 고른 언어는 기억해 두고, 진입 주소(/dayline/)의 자동 이동에서 우선한다.
        document.querySelectorAll('a[data-lang]').forEach(function (a) {{
            a.addEventListener('click', function () {{
                try {{ localStorage.setItem('{STORAGE_KEY}', a.getAttribute('data-lang')); }} catch (err) {{}}
            }});
        }});
        var menu = document.querySelector('.lang-menu');
        document.addEventListener('click', function (ev) {{
            if (menu.open && !menu.contains(ev.target)) menu.open = false;
        }});
        document.addEventListener('keydown', function (ev) {{
            if (ev.key === 'Escape') menu.open = false;
        }});

        // 그림과 하루 화면이 화면에 들어오면(.in) 선이 그려진다. 한 번만 한다.
        if (!document.documentElement.classList.contains('anim')) return;
        // 하루 화면은 그동안 거리를 0 에서부터 올린다 — 선과 같은 시계(프레임 시각)로 센다
        var day = document.querySelector('.day'), num = day.querySelector('[data-count]');
        var end = parseFloat(num.getAttribute('data-count')), shown = num.textContent;
        var comma = shown.indexOf(',') !== -1, ms = parseFloat(day.getAttribute('data-draw')) * 1000;
        function write(n) {{ num.textContent = n.toFixed(1).replace('.', comma ? ',' : '.'); }}
        function count(start, now) {{
            var p = Math.min(1, (now - start) / ms);
            if (p < 1) {{ write(end * p); requestAnimationFrame(function (t) {{ count(start, t); }}); }}
            else num.textContent = shown;
        }}
        write(0);
        var io = new IntersectionObserver(function (entries) {{
            entries.forEach(function (entry) {{
                if (!entry.isIntersecting) return;
                io.unobserve(entry.target);
                entry.target.classList.add('in');
                if (entry.target === day) requestAnimationFrame(function (t) {{ count(t, t); }});
            }});
        }}, {{ threshold: 0.45 }});
        document.querySelectorAll('[data-inview]').forEach(function (el) {{ io.observe(el); }});
    }})();
</script>"""


# 그림과 하루 화면의 선은 화면에 들어올 때 그려진다. 스크립트가 돌지 않거나 움직임을 줄이라고 한 기기에서는
# 처음부터 다 그려진 채로 보이게, 숨겨 두는 모양(.anim)은 여기서 켠 뒤에만 먹는다.
HEAD_SCRIPT = """<script>
    if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches)
        document.documentElement.classList.add('anim');
</script>"""


def ld(obj):
    # </script> 로 끊기지 않게
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(
        obj, ensure_ascii=False, indent=2).replace("</", "<\\/")


def alternates(langs):
    rows = [f'<link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x["code"])}" />' for x in langs]
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{url(DEFAULT)}" />')
    return "\n".join(rows)


def page(d, langs, css, legal):
    code = d["code"]
    canon = url(code)
    og_image = f"{SITE}{ASSETS}/{og_name(code)}"

    home = SITE + ("/" if code == DEFAULT else f"/{code}/")  # 회사 소개의 같은 언어
    org, site = f"{SITE}/#organization", f"{SITE}/#website"
    # 검색엔진과 AI 검색이 "누가 만든 무슨 앱의 어느 페이지인지"를 한 번에 읽게, 서로 @id 로 잇는다.
    # 별점 · 리뷰는 스토어에 생기기 전이라 넣지 않는다 (없는 값을 지어 넣지 않는다).
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": org, "name": "Zaco Labs", "url": SITE + "/",
         "logo": {"@type": "ImageObject", "url": f"{SITE}/zacolabs-assets/logo.png"},
         "email": "zaco.labs@gmail.com"},
        {"@type": "WebSite", "@id": site, "url": SITE + "/", "name": "Zaco Labs", "publisher": {"@id": org}},
        {"@type": "WebPage", "@id": canon + "#webpage", "url": canon, "name": d["title"],
         "description": d["description"], "inLanguage": d["html_lang"], "isPartOf": {"@id": site},
         "about": {"@id": canon + "#app"}, "breadcrumb": {"@id": canon + "#breadcrumb"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": og_image, "width": 1200, "height": 630}},
        {"@type": "BreadcrumbList", "@id": canon + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Zaco Labs", "item": home},
            {"@type": "ListItem", "position": 2, "name": "Dayline", "item": canon}]},
        {"@type": "MobileApplication", "@id": canon + "#app", "name": "Dayline",
         "description": d["app_description"], "url": canon, "image": SITE + ICON,
         "applicationCategory": "LifestyleApplication", "operatingSystem": "Android, iOS",
         "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": d["currency"]},
         "featureList": [f["title"] for f in d["features"]],
         "inLanguage": [x["hreflang"] for x in langs],
         "downloadUrl": [u for u in (PLAY, APPLE) if u], "sameAs": [u for u in (PLAY, APPLE) if u],
         "publisher": {"@id": org}, "author": {"@id": org}},
        {"@type": "FAQPage", "@id": canon + "#faq", "inLanguage": d["html_lang"],
         "isPartOf": {"@id": canon + "#webpage"},
         "mainEntity": [{"@type": "Question", "name": f["q"],
                         "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                        for f in d["faqs"]]},
    ]}
    locales = "\n".join(f'<meta property="og:locale:alternate" content="{x["og_locale"]}" />'
                        for x in langs if x["code"] != code)
    # 아이폰 사파리의 앱 배너. 앱이 스토어에 나온 뒤에만 보인다.
    app_banner = f'\n<meta name="apple-itunes-app" content="app-id={APPLE_ID}" />' if APPLE_ID else ""

    feats = "\n".join(
        f'''                <li>
                    <h3>{e(f["title"])}</h3>
                    <p>{e(f["text"])}</p>
                </li>''' for f in d["features"])

    steps = "\n".join(
        f'''                <li>
                    {art(f"step-{i + 1}", s["alt"], STEP_SIZE, 'loading="lazy"')}
                    <div class="step-body">
                        <h3>{e(s["title"])}</h3>
                        <p>{e(s["text"])}</p>
                    </div>
                </li>''' for i, s in enumerate(d["steps"]))

    faqs = "\n".join(
        f'''                <details>
                    <summary>{e(f["q"])}</summary>
                    <div class="answer">{e(f["a"])}</div>
                </details>''' for f in d["faqs"])

    dir_attr = ' dir="rtl"' if d["dir"] == "rtl" else ""
    return f'''<!DOCTYPE html>
<html lang="{d["html_lang"]}"{dir_attr}>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(d["title"])}</title>
<meta name="description" content="{e(d["description"])}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<meta name="author" content="Zaco Labs" />
<meta name="application-name" content="Dayline" />
<meta name="apple-mobile-web-app-title" content="Dayline" />{app_banner}
<meta name="theme-color" content="#ffffff" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Dayline" />
<meta property="og:locale" content="{d["og_locale"]}" />
{locales}
<meta property="og:title" content="{e(d["og_title"])}" />
<meta property="og:description" content="{e(d["og_description"])}" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:alt" content="{e(d["og_title"])}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{e(d["og_title"])}" />
<meta name="twitter:description" content="{e(d["og_description"])}" />
<meta name="twitter:image" content="{og_image}" />
<meta name="twitter:image:alt" content="{e(d["og_title"])}" />
<link rel="icon" href="{ICON}" />
<link rel="apple-touch-icon" href="{ICON}" />
<link rel="canonical" href="{canon}" />
{alternates(langs)}
{ld(graph)}
{HEAD_SCRIPT}
<style>{css.replace("{{FONT}}", d["font"])}</style>
</head>
<body>

<header class="site">
    <div class="wrap">
        <a class="brand" href="{path(code)}">
            <img src="{ICON}" alt="" width="30" height="30" />
            <span>Dayline</span>
        </a>
        {lang_menu(code, langs)}
    </div>
</header>

<main>
    <div class="wrap">
        <section class="hero">
            <div class="hero-copy">
                <p class="eyebrow">{e(d["eyebrow"])}</p>
                <h1>{e(d["h1"])}</h1>
                <p class="lede">{e(d["lede"])}</p>
                {badges(d)}
                <p class="note">{e(d["note"])}</p>
            </div>
            <div class="hero-art">
                {art("hero", d["hero_alt"], HERO_SIZE, 'fetchpriority="high"')}
            </div>
        </section>

        <section id="features">
            <h2>{e(d["features_title"])}</h2>
            <p class="section-lede">{e(d["features_lede"])}</p>
            <div class="feature-wrap">
                <ul class="feature-list">
{feats}
                </ul>
                <figure class="shot">
                    {day_card(d)}
                    <figcaption>{e(d["shot_caption"])}</figcaption>
                </figure>
            </div>
        </section>

        <section id="story">
            <h2>{e(d["story_title"])}</h2>
            <p class="section-lede">{e(d["story_lede"])}</p>
            <ol class="steps">
{steps}
            </ol>
        </section>

        <section id="faq">
            <h2>{e(d["faq_title"])}</h2>
            <p class="section-lede">{e(d["faq_lede"])}</p>
            <div class="faq-list">
{faqs}
            </div>
        </section>
    </div>

    <section class="cta">
        <div class="wrap">
            <h2>{e(d["cta_title"])}</h2>
            <p>{e(d["cta_text"])}</p>
            {badges(d)}
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
</body>
</html>
'''


# ── 진입 주소 ───────────────────────────────────────────────────────
# /dayline/ 은 브라우저 언어에 맞는 페이지로 보낸다. 스크립트를 돌리지 않는 로봇은 영어 한 줄 소개와 언어 목록을 읽고,
# 검색엔진에는 영어 랜딩이 대표 주소(canonical)라고 알린다.
# 우선순위: ?lang= → 직접 고른 언어(localStorage) → 브라우저 선호 언어 목록 → en
# 언어 표기는 약관 페이지(dayline_legal.py)와 같게 읽는다: 앱 언어 태그(zh-Hans · fil …), 옛 코드(kr · jp · in · tl), 지역이 붙은 태그(pt-BR).
def entry_page(langs):
    d = next(x for x in langs if x["code"] == DEFAULT)
    links = "\n            ".join(
        f'<a href="{path(x["code"])}" lang="{x["html_lang"]}" hreflang="{x["hreflang"]}">{e(x["label"])}</a>'
        for x in langs)
    og_image = f'{SITE}{ASSETS}/og-{DEFAULT}.png'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(d["og_title"])}</title>
<meta name="description" content="{e(d["description"])}" />
<link rel="canonical" href="{url(DEFAULT)}" />
<meta name="theme-color" content="#ffffff" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Dayline" />
<meta property="og:title" content="{e(d["og_title"])}" />
<meta property="og:description" content="{e(d["og_description"])}" />
<meta property="og:url" content="{BASE}/" />
<meta property="og:image" content="{og_image}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{e(d["og_title"])}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="{ICON}" />
{alternates(langs)}
<script>
    (function () {{
        var CODES = {json.dumps([x["code"] for x in langs])};
        var OLD = {{ kr: "ko", jp: "ja", "in": "id", tl: "fil" }};
        function pick(v) {{
            v = String(v || "").trim().toLowerCase().replace(/_/g, "-");
            if (!v) return null;
            if (v === "zh" || v.indexOf("zh-") === 0) {{
                if (v.indexOf("hant") !== -1) v = "zh-hant";
                else if (v.indexOf("hans") !== -1) v = "zh-hans";
                else v = /-(tw|hk|mo)$/.test(v) ? "zh-hant" : "zh-hans";
            }} else {{
                v = v.split("-")[0];
                v = OLD[v] || v;
            }}
            return CODES.indexOf(v) !== -1 ? v : null;
        }}
        var params = new URLSearchParams(location.search);
        var prefs = [params.get("lang")];
        try {{ prefs.push(localStorage.getItem("{STORAGE_KEY}")); }} catch (err) {{}}
        prefs = prefs.concat(navigator.languages || [navigator.language || navigator.userLanguage]);
        var dest = "{DEFAULT}";
        for (var i = 0; i < prefs.length; i++) {{
            var c = pick(prefs[i]);
            if (c) {{ dest = c; break; }}
        }}
        params.delete("lang");
        var qs = params.toString();
        location.replace("/dayline/" + dest + "/" + (qs ? "?" + qs : "") + location.hash);
    }})();
</script>
<noscript><meta http-equiv="refresh" content="0; url={path(DEFAULT)}" /></noscript>
<style>
    html, body {{ margin: 0; min-height: 100%; background: #fff; color: #3F3F45;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    .box {{ min-height: 100vh; display: flex; flex-direction: column; align-items: center;
        justify-content: center; gap: 14px; text-align: center; padding: 24px; box-sizing: border-box; }}
    .box h1 {{ margin: 0; font-size: 22px; color: #111113; }}
    .box p {{ margin: 0; max-width: 520px; line-height: 1.6; font-size: 15px; }}
    .box nav {{ max-width: 560px; line-height: 2.1; font-size: 14px; }}
    .box a {{ color: #111113; text-decoration: none; margin: 0 7px; white-space: nowrap; }}
    .box a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
    <div class="box">
        <h1>Dayline</h1>
        <p>{e(d["lede"])}</p>
        <nav aria-label="Language">
            {links}
        </nav>
    </div>
</body>
</html>
"""


def llms_links():
    """llms.txt 의 Dayline 줄들. build.py 가 쓴다."""
    d = load(DEFAULT)
    langs = [load(c) for c in codes() if c != DEFAULT]
    others = ", ".join(f'[{x["label"]}]({url(x["code"])})' for x in langs)
    return f"""- [Dayline]({url(DEFAULT)}): {d["app_description"]} Free on iOS and Android.
- [Dayline privacy policy]({SITE}/dayline/privacy.en.html): what Dayline collects and what never leaves the device
- [Dayline terms of service]({SITE}/dayline/terms.en.html)
- [Dayline community rules]({SITE}/dayline/community.en.html): what may be posted to the feed of days, reporting and blocking
- Dayline in other languages: {others}"""


def llms_full():
    """llms-full.txt 의 Dayline 장: 랜딩의 영어 본문을 그대로 마크다운으로."""
    d = load(DEFAULT)
    stores = [f"- Google Play: {PLAY}"] + ([f"- App Store: {APPLE}"] if APPLE else [])
    feats = "\n".join(f'- **{f["title"]}.** {f["text"]}' for f in d["features"])
    steps = "\n".join(f'{i + 1}. **{x["title"]}.** {x["text"]}' for i, x in enumerate(d["steps"]))
    faqs = "\n\n".join(f'### {f["q"]}\n\n{f["a"]}' for f in d["faqs"])
    return f"""## Dayline

{d["lede"]}

- Type: mobile app for iOS and Android, by Zaco Labs
- Price: free, with one ad below the tab bar
- Account: none. The movement record is stored on the device; only a day the user chooses to post sends its line's shape, distance, duration and date to the server, never the map or coordinates
- Languages: {len(codes())}
- Page: {url(DEFAULT)}
{chr(10).join(stores)}
- Privacy policy: {SITE}/dayline/privacy.en.html
- Contact: zaco.labs@gmail.com

### {d["features_title"]}

{feats}

### {d["story_title"]}

{steps}

## Dayline: {d["faq_title"].lower()}

{faqs}
"""


def sitemap_urls(today):
    """build.py 가 sitemap.xml 에 같이 싣는다."""
    langs = [load(c) for c in codes()]
    links = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{x["hreflang"]}" href="{url(x["code"])}" />' for x in langs
    ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url(DEFAULT)}" />'
    return "\n".join(f'''  <url>
    <loc>{url(x["code"])}</loc>
    <lastmod>{today}</lastmod>
{links}
  </url>''' for x in langs)


def build():
    langs = [load(c) for c in codes()]
    keys = set(next(x for x in langs if x["code"] == DEFAULT))
    for d in langs:
        missing = keys - set(d)
        if missing:
            raise SystemExit(f"dayline/landing/i18n/{d['code']}.json 에 빠진 문구: {', '.join(sorted(missing))}")
    with open(os.path.join(SRC, "style.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(HERE, "dayline", "strings.json"), encoding="utf-8") as f:
        legal = json.load(f)
    for d in langs:
        out = os.path.join(OUT, d["code"])
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(d, langs, css, legal[d["code"]]))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(entry_page(langs))
    return len(langs)


if __name__ == "__main__":
    print(f"built {build()} dayline landing pages")
