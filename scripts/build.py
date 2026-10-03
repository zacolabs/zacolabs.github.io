#!/usr/bin/env python3
"""Zaco Labs 회사 소개 페이지 생성기.

    python3 scripts/build.py

i18n/<code>.json 의 문구로 영어는 /index.html, 다른 언어는 /<code>/index.html 을 만들고
sitemap.xml 을 다시 쓴다. 문구는 JSON 에서, 모양은 style.css 에서만 고친다.
Dayline 의 약관 · 개인정보 처리방침 · 라이선스 페이지(/dayline/)도 같이 만든다 — dayline_legal.py.
생성된 HTML 을 직접 고치면 다음 빌드에서 덮어써진다.

언어 목록 · 이름 · 로케일 · Waky 한 줄 소개(h1)는 waky-landing(scripts/landing/i18n)과 맞춘다.
"""
import datetime
import html
import json
import os

import dayline_legal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SITE = "https://zacolabs.github.io"
WAKY_LANDING = f"{SITE}/waky-landing/introduce"
# 공유 미리보기 그림. 모든 언어가 같이 쓴다. scripts/og-image.html 을 1200x630 으로 찍은 것.
OG_IMAGE = f"{SITE}/zacolabs-assets/og-image-1200x630.png"
OG_IMAGE_ALT = "Zaco Labs"

# 언어 순서 — hreflang·언어 메뉴·사이트맵이 모두 이 순서를 따른다. 영어는 주소 접두사 없이 맨 앞(/)에 둔다.
ORDER = ["ko", "en", "ja", "zh-hans", "zh-hant", "es", "fr", "de", "it", "pt",
         "nl", "da", "pl", "ru", "ar", "id", "vi", "fil"]
DEFAULT = "en"

# 고른 언어를 기억하는 localStorage 키. 맨 앞 주소(/)로 와도 이 언어로 옮긴다.
STORAGE_KEY = "zacolabs-lang"

# 처음 온 사람은 접속 지역의 언어로 보낸다. GitHub Pages 는 정적이라 IP 로 국가를 알 수 없으니,
# 기기의 시간대(IANA)로 지역을 가린다 — 네트워크 요청 없이 그리기 전에 옮길 수 있다.
# 여기 없는 시간대(미국 · 영국 · 인도 · 캐나다 · 스위스처럼 여러 언어를 쓰는 곳 포함)나 시간대를 모르면 영어.
TZ_LANG = {
    "ko": ["Asia/Seoul", "ROK"],
    "ja": ["Asia/Tokyo", "Japan"],
    "zh-hans": ["Asia/Shanghai", "Asia/Chongqing", "Asia/Chungking", "Asia/Harbin", "Asia/Urumqi", "Asia/Kashgar", "PRC"],
    "zh-hant": ["Asia/Taipei", "ROC", "Asia/Hong_Kong", "Hongkong", "Asia/Macau", "Asia/Macao"],
    "es": ["Europe/Madrid", "Atlantic/Canary", "Africa/Ceuta", "Africa/Malabo",
           "America/Mexico_City", "America/Cancun", "America/Merida", "America/Monterrey", "America/Matamoros",
           "America/Chihuahua", "America/Ciudad_Juarez", "America/Ojinaga", "America/Mazatlan", "America/Bahia_Banderas",
           "America/Hermosillo", "America/Tijuana", "America/Bogota", "America/Lima", "America/Santiago",
           "America/Punta_Arenas", "America/Buenos_Aires", "America/Caracas", "America/Guayaquil", "America/La_Paz",
           "America/Asuncion", "America/Montevideo", "America/Guatemala", "America/Tegucigalpa", "America/El_Salvador",
           "America/Managua", "America/Costa_Rica", "America/Panama", "America/Havana", "America/Santo_Domingo",
           "America/Puerto_Rico", "Pacific/Galapagos", "Pacific/Easter"],
    "fr": ["Europe/Paris", "Europe/Monaco", "Europe/Luxembourg", "America/Port-au-Prince", "America/Martinique",
           "America/Guadeloupe", "America/Cayenne", "Indian/Reunion", "Indian/Mayotte", "Pacific/Tahiti", "Pacific/Noumea",
           "Africa/Dakar", "Africa/Abidjan", "Africa/Bamako", "Africa/Ouagadougou", "Africa/Niamey", "Africa/Conakry",
           "Africa/Lome", "Africa/Porto-Novo", "Africa/Libreville", "Africa/Brazzaville", "Africa/Kinshasa",
           "Africa/Lubumbashi", "Africa/Douala", "Africa/Bangui", "Africa/Ndjamena", "Africa/Djibouti"],
    "de": ["Europe/Berlin", "Europe/Busingen", "Europe/Vienna", "Europe/Vaduz"],
    "it": ["Europe/Rome", "Europe/San_Marino", "Europe/Vatican"],
    "pt": ["America/Sao_Paulo", "America/Bahia", "America/Fortaleza", "America/Recife", "America/Belem",
           "America/Maceio", "America/Araguaina", "America/Manaus", "America/Cuiaba", "America/Campo_Grande",
           "America/Porto_Velho", "America/Boa_Vista", "America/Rio_Branco", "America/Eirunepe", "America/Santarem",
           "America/Noronha", "Europe/Lisbon", "Atlantic/Madeira", "Atlantic/Azores", "Africa/Luanda", "Africa/Maputo",
           "Atlantic/Cape_Verde", "Africa/Bissau", "Africa/Sao_Tome"],
    "nl": ["Europe/Amsterdam", "Europe/Brussels", "America/Paramaribo", "America/Curacao", "America/Aruba"],
    "da": ["Europe/Copenhagen", "Atlantic/Faroe"],
    "pl": ["Europe/Warsaw"],
    "ru": ["Europe/Moscow", "Europe/Kaliningrad", "Europe/Samara", "Europe/Volgograd", "Europe/Saratov",
           "Europe/Ulyanovsk", "Europe/Astrakhan", "Europe/Kirov", "Europe/Minsk", "Asia/Yekaterinburg", "Asia/Omsk",
           "Asia/Novosibirsk", "Asia/Barnaul", "Asia/Tomsk", "Asia/Novokuznetsk", "Asia/Krasnoyarsk", "Asia/Irkutsk",
           "Asia/Chita", "Asia/Yakutsk", "Asia/Khandyga", "Asia/Vladivostok", "Asia/Ust-Nera", "Asia/Magadan",
           "Asia/Sakhalin", "Asia/Srednekolymsk", "Asia/Kamchatka", "Asia/Anadyr"],
    "ar": ["Asia/Riyadh", "Asia/Dubai", "Asia/Qatar", "Asia/Bahrain", "Asia/Kuwait", "Asia/Muscat", "Asia/Aden",
           "Asia/Baghdad", "Asia/Amman", "Asia/Damascus", "Asia/Beirut", "Asia/Gaza", "Asia/Hebron", "Africa/Cairo",
           "Egypt", "Africa/Tripoli", "Libya", "Africa/Tunis", "Africa/Algiers", "Africa/Casablanca", "Africa/El_Aaiun",
           "Africa/Khartoum", "Africa/Nouakchott"],
    "id": ["Asia/Jakarta", "Asia/Pontianak", "Asia/Makassar", "Asia/Jayapura"],
    "vi": ["Asia/Ho_Chi_Minh", "Asia/Saigon"],
    "fil": ["Asia/Manila"],
}
# 도시 이름까지 다 적기엔 많은 곳은 앞부분으로 가린다
TZ_PREFIX_LANG = {"America/Argentina/": "es"}

PLAY = "https://play.google.com/store/apps/details?id=com.waky.android"
APPLE = "https://apps.apple.com/app/id6797402938"
DUIRE_KO = "https://www.duire.kr"
DUIRE_EN = "https://www.duire.kr/en"  # 두이레는 한국어 · 영어뿐이라 나머지 언어는 영어로 보낸다

# 서치 콘솔 확인 태그. 도메인 맨 앞(한국어) 페이지에만 둔다.
VERIFY = [
    "3JNaFd6fvPNBA7NMsjDxFkAvM1aAESN3FrJCD46fIfc",
    "j4UymJXi-PpVcq8t-553W-iBpZxQchNTUFjvLdqMrXU",
    "rAAo91osYvOPP0Yz3pm0CsJnhYeOqQEqn37xbCX3l0Q",
]

PLAY_PATH = "M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594zM1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924zm12.208 10.065l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.041 10.973zm0 2.067l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"
APPLE_PATH = "M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"
WEB_PATH = "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM3.6 9h16.8M3.6 15h16.8M12 3c2.3 2.5 3.5 5.5 3.5 9s-1.2 6.5-3.5 9c-2.3-2.5-3.5-5.5-3.5-9s1.2-6.5 3.5-9z"


def e(s):
    return html.escape(s, quote=True)


def load(code):
    with open(os.path.join(HERE, "i18n", f"{code}.json"), encoding="utf-8") as f:
        return json.load(f)


def path(code):
    return "/" if code == DEFAULT else f"/{code}/"


def url(code):
    return SITE + path(code)


def waky_url(t):
    return f"{WAKY_LANDING}/{t['waky_slug']}/"


def duire_url(code):
    return DUIRE_KO if code == "ko" else DUIRE_EN


def alternates(langs):
    rows = [f'<link rel="alternate" hreflang="{langs[c]["hreflang"]}" href="{url(c)}" />' for c in ORDER]
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{url(DEFAULT)}" />')
    return "\n".join(rows)


def lang_menu(langs, code):
    items = []
    for c in ORDER:
        t = langs[c]
        cur = ' aria-current="page"' if c == code else ""
        items.append(
            f'            <li><a href="{path(c)}" lang="{t["html_lang"]}" hreflang="{t["hreflang"]}" '
            f'data-lang="{c}"{cur}>{e(t["label"])}</a></li>'
        )
    label = langs[code]["label"]
    return f'''<header class="top">
    <details class="lang-menu">
        <summary aria-label="Language: {e(label)}">
            <svg class="globe" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="7.25"/><path d="M2.75 10h14.5M10 2.75c2.1 2.3 3 4.7 3 7.25s-.9 4.95-3 7.25c-2.1-2.3-3-4.7-3-7.25s.9-4.95 3-7.25Z"/></svg>
            <span>{e(label)}</span>
            <svg class="chev" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m5.5 8 4.5 4.5L14.5 8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </summary>
        <ul aria-label="Language">
{chr(10).join(items)}
        </ul>
    </details>
</header>'''


def json_ld(t, code):
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Zaco Labs",
        "url": url(code),
        "logo": f"{SITE}/zacolabs-assets/logo.png",
        "email": "zaco.labs@gmail.com",
        "description": t["org_description"],
        "inLanguage": t["html_lang"],
        "makesOffer": [{
            "@type": "Offer",
            "itemOffered": {
                "@type": "SoftwareApplication",
                "name": "Waky",
                "applicationCategory": "LifestyleApplication",
                "operatingSystem": "Android, iOS",
                "description": t["waky_ld"],
                "url": waky_url(t),
            },
        }, {
            "@type": "Offer",
            "itemOffered": {
                "@type": "Service",
                "name": t["duire_ld_name"],
                "description": t["duire_ld"],
                "url": duire_url(code),
            },
        }],
    }
    # </script> 로 끊기지 않게
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def head_script(code):
    """맨 앞(/) 영어 페이지에서만: 메뉴로 고른 언어 → 없으면 접속 지역(시간대) 언어로 옮긴다. 모르면 영어 그대로.
    검색 로봇은 옮기지 않는다 — 영어 페이지가 다른 언어로 색인되지 않게."""
    if code != DEFAULT:
        return ""
    codes = json.dumps(ORDER)
    tz = json.dumps({z: c for c, zones in TZ_LANG.items() for z in zones}, separators=(",", ":"))
    prefixes = json.dumps(TZ_PREFIX_LANG, separators=(",", ":"))
    return f'''<script>
    (function () {{
        var CODES = {codes}, DEF = "{DEFAULT}";
        var TZ = {tz};
        var TZ_PREFIX = {prefixes};
        function go(l) {{
            if (l && l !== DEF && CODES.indexOf(l) !== -1) location.replace("/" + l + "/" + location.search + location.hash);
        }}
        var saved = null;
        try {{ saved = localStorage.getItem("{STORAGE_KEY}"); }} catch (err) {{}}
        if (CODES.indexOf(saved) !== -1) return go(saved);
        if (/bot|crawl|spider|slurp|mediapartners|facebookexternalhit|lighthouse/i.test(navigator.userAgent)) return;
        var zone = "";
        try {{ zone = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; }} catch (err) {{}}
        var l = TZ[zone];
        if (!l) for (var p in TZ_PREFIX) if (zone.indexOf(p) === 0) l = TZ_PREFIX[p];
        go(l);
    }})();
</script>
'''


def page(langs, code, css):
    t = langs[code]
    title = f"Zaco Labs — {t['tagline']}"
    verify = "".join(f'<meta name="google-site-verification" content="{v}" />\n' for v in VERIFY) if code == DEFAULT else ""
    about = "<br />\n        ".join(e(line) for line in t["about"])
    style = css.replace("$FONT", t["font"])
    return f'''<!DOCTYPE html>
<html lang="{t["html_lang"]}" dir="{t["dir"]}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
{verify}<title>{e(title)}</title>
<meta name="description" content="{e(t["description"])}" />
<meta name="theme-color" content="#0a0a0a" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Zaco Labs" />
<meta property="og:locale" content="{t["og_locale"]}" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(t["og_description"])}" />
<meta property="og:url" content="{url(code)}" />
<meta property="og:image" content="{OG_IMAGE}" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{e(OG_IMAGE_ALT)}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="/zacolabs-assets/logo.png" />
<link rel="apple-touch-icon" href="/zacolabs-assets/logo.png" />
<link rel="canonical" href="{url(code)}" />
{alternates(langs)}
{head_script(code)}<script type="application/ld+json">
{json_ld(t, code)}
</script>
<style>
{style}</style>
</head>
<body>
<div class="glow"></div>

{lang_menu(langs, code)}

<main>
    <div class="mark">
        <!-- Zaco Labs CI (waky-android resources/ci_512.png) -->
        <img src="/zacolabs-assets/logo.png?v=20260723" alt="{e(t["logo_alt"])}" width="128" height="128" />
    </div>

    <h1 class="wordmark">Zaco Labs</h1>
    <p class="tagline">{e(t["tagline"])}</p>

    <div class="divider"></div>

    <p class="about">
        {about}
    </p>

    <section class="products">
        <h2>Products</h2>
        <div class="cards">
            <article class="card">
                <div class="card-head">
                    <img class="card-ico" src="/zacolabs-assets/app_icon.png" alt="{e(t["waky_icon_alt"])}" width="52" height="52" />
                    <div class="card-name">
                        <h3>Waky</h3>
                        <p class="kind">{e(t["waky_kind"])}</p>
                    </div>
                    <a class="card-more" href="{waky_url(t)}" target="_blank" rel="noopener">{e(t["learn_more"])}</a>
                </div>
                <p class="card-title">{e(t["waky_title"])}</p>
                <p class="card-body">{e(t["waky_body"])}</p>
                <div class="card-actions">
                    <a class="badge" href="{PLAY}" target="_blank" rel="noopener">
                        <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{PLAY_PATH}"/></svg>
                        <span class="badge-txt"><small>GET IT ON</small><strong>Google Play</strong></span>
                    </a>
                    <a class="badge" href="{APPLE}" target="_blank" rel="noopener">
                        <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{APPLE_PATH}"/></svg>
                        <span class="badge-txt"><small>Download on the</small><strong>App Store</strong></span>
                    </a>
                </div>
            </article>
            <article class="card">
                <div class="card-head">
                    <img class="card-ico" src="/zacolabs-assets/duire_icon.png" alt="{e(t["duire_icon_alt"])}" width="52" height="52" />
                    <div class="card-name">
                        <h3>{e(t["duire_name"])}</h3>
                        <p class="kind">{e(t["duire_kind"])}</p>
                    </div>
                    <a class="card-more" href="{duire_url(code)}" target="_blank" rel="noopener">{e(t["learn_more"])}</a>
                </div>
                <p class="card-title">{e(t["duire_title"])}</p>
                <p class="card-body">{e(t["duire_body"])}</p>
                <div class="card-actions">
                    <a class="badge" href="{duire_url(code)}" target="_blank" rel="noopener">
                        <svg class="badge-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="{WEB_PATH}"/></svg>
                        <span class="badge-txt"><small>{e(t["web_start"])}</small><strong>duire.kr</strong></span>
                    </a>
                </div>
            </article>
        </div>
    </section>
</main>

<footer>
    <div class="row"><a href="mailto:zaco.labs@gmail.com">zaco.labs@gmail.com</a></div>
    <div class="row">© <span id="year">{datetime.date.today().year}</span> Zaco Labs. {e(t["rights"])}</div>
</footer>

<script>
    (function () {{
        document.getElementById('year').textContent = new Date().getFullYear();
        // 언어 메뉴: 고른 언어를 기억하고, 바깥을 누르거나 Esc 면 닫는다
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
            if (ev.key === 'Escape' && menu.open) {{ menu.open = false; menu.querySelector('summary').focus(); }}
        }});
    }})();
</script>
</body>
</html>
'''


def moved_stub():
    """옛 /en/ 주소. 영어가 맨 앞(/)으로 옮겨 왔으니 그리로 보낸다. 영어 주소로 온 것이니 영어를 고른 것으로 남긴다."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Zaco Labs</title>
<meta name="robots" content="noindex" />
<link rel="canonical" href="{url(DEFAULT)}" />
<script>
    try {{ localStorage.setItem("{STORAGE_KEY}", "{DEFAULT}"); }} catch (err) {{}}
    location.replace("/" + location.search + location.hash);
</script>
<meta http-equiv="refresh" content="0; url=/" />
</head>
<body></body>
</html>
'''


def sitemap(langs):
    today = datetime.date.today().isoformat()
    links = "\n".join(
        f'    <xhtml:link rel="alternate" hreflang="{langs[c]["hreflang"]}" href="{url(c)}" />' for c in ORDER
    ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url(DEFAULT)}" />'
    urls = "\n".join(f'''  <url>
    <loc>{url(c)}</loc>
    <lastmod>{today}</lastmod>
{links}
  </url>''' for c in ORDER)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{urls}
</urlset>
'''


def main():
    langs = {c: load(c) for c in ORDER}
    keys = set(langs[DEFAULT])
    for c, t in langs.items():
        missing = keys - set(t)
        if missing:
            raise SystemExit(f"{c}.json 에 빠진 문구: {', '.join(sorted(missing))}")
    with open(os.path.join(HERE, "style.css"), encoding="utf-8") as f:
        css = f.read()
    for c in ORDER:
        out_dir = ROOT if c == DEFAULT else os.path.join(ROOT, c)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(langs, c, css))
    os.makedirs(os.path.join(ROOT, DEFAULT), exist_ok=True)
    with open(os.path.join(ROOT, DEFAULT, "index.html"), "w", encoding="utf-8") as f:
        f.write(moved_stub())
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap(langs))
    print(f"built {len(ORDER)} pages")
    print(f"built {dayline_legal.build()} dayline legal pages")


if __name__ == "__main__":
    main()
