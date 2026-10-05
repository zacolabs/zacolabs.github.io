# zacolabs.github.io

`https://zacolabs.github.io/` 도메인 맨 앞에 두어야 하는 파일과, 따로 저장소를 두지 않은 Dayline 의 랜딩 · 약관 페이지를 둔다. Waky 랜딩 페이지는 `zacolabs/waky-landing` 저장소(`/waky-landing/`)에 있다.

- `app-ads.txt` — AdMob 이 스토어의 개발자 웹사이트 도메인 맨 앞에서만 찾는다. 게시자 `pub-7125409961311406`
- `robots.txt` — 검색엔진은 도메인 맨 앞의 이 파일만 읽는다. 랜딩 사이트맵을 여기서 알린다
  - AI 검색 · 어시스턴트의 크롤러(GPTBot · ClaudeBot · PerplexityBot …)도 막지 않는다고 따로 적어 둔다. 모든 로봇을 허용하는 첫 규칙만으로도 허용이지만, 뜻을 밝혀 두는 것이다
- `llms.txt` · `llms-full.txt` — AI 검색 · 에이전트에게 주는 사이트 안내(llmstxt.org 형식)와, 링크를 따라가지 않아도 되게 본문을 편 것. 영어로 쓴다. **`scripts/build.py` 가 회사 소개와 Dayline 랜딩의 영어 문구로 만든다 — 직접 고치지 말 것**
- `index.html` · `<언어>/index.html` — 회사 소개 페이지. **`scripts/build.py` 가 만든다 — 직접 고치지 말 것.** 영어는 도메인 맨 앞(`/`), 다른 17개 언어는 `/ko/` · `/ja/` … 에 둔다 (언어 목록은 waky-landing 과 같다). 옛 `/en/` 은 `/` 로 넘긴다
  - 문구는 `scripts/i18n/<언어>.json`, 모양은 `scripts/style.css` 에서 고치고 `python3 scripts/build.py` 를 돌린다. `sitemap.xml` 도 같이 다시 쓴다
  - `/` 로 온 사람의 언어: ① 오른쪽 위 언어 메뉴(두이레와 같은 모양)로 고른 언어(`localStorage` 의 `zacolabs-lang`) ② 없으면 접속 지역 — 정적 호스팅이라 IP 를 볼 수 없어 기기 시간대로 가린다(`build.py` `TZ_LANG`) ③ 모르면 영어. 검색 로봇은 옮기지 않는다
  - Waky 자세히 보기는 그 언어 랜딩으로 건다. 두이레는 한국어 · 영어뿐이라 한국어가 아니면 `duire.kr/en` 으로 보낸다
  - Dayline 자세히 보기는 그 언어의 랜딩(`/dayline/<언어>/`)으로 걸고, 그 언어의 랜딩이 아직 없으면 영어로 건다
  - Dayline 카드의 스토어 버튼은 랜딩과 같은 주소를 쓴다 (`dayline_landing.py` 의 `PLAY` · `APPLE_ID`). 주소가 있는 스토어의 버튼만 나온다
- 서치 콘솔 확인 태그는 맨 앞(영어) 페이지에만 있다
- `dayline/` — Dayline 의 이용 약관 · 개인정보 처리방침 · 오픈소스 라이선스. **`scripts/dayline_legal.py` 가 만든다 — 직접 고치지 말 것** (`build.py` 가 같이 돌린다)
  - 약관 · 개인정보 처리방침의 본문은 `scripts/dayline/<문서>.<언어>.html`, 모양은 `scripts/dayline/style.css`. **이 본문이 기준이다** — 앱은 글을 따로 싣지 않고 이 주소를 연다. Waky 의 같은 페이지(`zacolabs-backend` `src/content/waky/legal`)에서 따와 Dayline 에 맞게 고친 것이라, 구조와 모양은 그쪽과 맞춘다
  - 라이선스는 언어마다 다른 글이 몇 줄뿐이라 본문 하나(`scripts/dayline/licenses.html`)의 `{{…}}` 자리에 `scripts/dayline/strings.json` 의 문구를 채운다. 문서 제목도 `strings.json` 에 있다
  - 주소도 Waky 와 같다: `/dayline/privacy.html?lang=ko&theme=light` (`terms` · `licenses` 도 같다). `?lang=` → 브라우저 언어 → 영어 순으로 언어를 정하고, `theme` 이 없으면 다크다. 언어를 고정한 주소는 `/dayline/privacy.ko.html` · `privacy.zh-hans.html` 처럼 언어 태그를 소문자로 쓴다
  - Waky 는 서버가 `?lang=` · `?theme=` 을 읽지만 여기는 정적 호스팅이라 페이지 안의 스크립트가 읽는다
  - 언어는 Dayline 앱과 같은 18개. 앱은 `?lang=` 에 앱 언어 태그(`zh-Hans`, `fil` …)를 그대로 싣는다. 한국어가 원문이고 나머지는 번역이다 — 글을 고치면 한국어부터 고치고 18개를 함께 맞춘다. 언어를 늘릴 때는 `dayline_legal.py` 의 `LANGS`, `strings.json`, 본문 파일을 더한다
  - 아랍어는 오른쪽에서 왼쪽으로 쓴다 (`dayline_legal.py` `RTL`)
  - `zacolabs` 조직에 `dayline` 이라는 이름의 저장소로 Pages 를 켜면 이 주소와 겹친다
- `dayline/index.html` · `dayline/<언어>/index.html` — Dayline 랜딩. **`scripts/dayline_landing.py` 가 만든다 — 직접 고치지 말 것** (`build.py` 가 같이 돌린다)
  - 구성은 Waky 랜딩(`waky-landing` `scripts/landing/`)을 따른다: 히어로 · 기능 · 3컷 · FAQ · CTA. 색은 앱 · 스토어 그림과 같은 어두운 바탕에 이동수단의 네 가지 색
  - 문구는 `scripts/dayline/landing/i18n/<언어>.json`, 모양은 `scripts/dayline/landing/style.css`. 언어 이름 · 로케일 · 글꼴은 회사 소개의 `scripts/i18n/<언어>.json` 에서 가져온다. 약관 링크의 글은 `scripts/dayline/strings.json` 의 문서 제목이다
  - **문구 파일이 있는 언어만 만든다** (지금은 앱과 같은 18개 언어 모두). 한국어가 원문이고 나머지는 번역이다 — 앱의 말(탭 · 이동수단 · 권한 이름)은 스토어 등록정보(`listing.md`)와 앱의 문자열을 따른다. 언어를 더할 때는 `<언어>.json` 을 두고 `make_assets.py` 를 돌린 뒤 빌드한다 — hreflang · 언어 메뉴 · 사이트맵 · 진입 주소가 따라 늘어난다. 언어 코드는 회사 소개와 같다 (`ko` · `ja` · `zh-hans` …)
  - `/dayline/` 로 온 사람의 언어: ① `?lang=`(앱 언어 태그 `zh-Hans` · `pt-BR`, 옛 코드 `kr` · `jp` · `in` · `tl` 도 받는다) ② 언어 메뉴로 고른 언어(`localStorage` 의 `zacolabs-lang`, 회사 소개와 같이 쓴다) ③ 브라우저 선호 언어 목록 ④ 영어
  - 검색 · 공유 · AI 검색용 표기: 제목 · 설명 · canonical · hreflang · OG(언어별 그림, `og:locale:alternate`) · 트위터 카드 · `robots`(큰 그림 미리보기 허용) · 아이폰 사파리의 앱 배너(`apple-itunes-app`). 구조화 데이터는 조직 · 사이트 · 페이지 · 경로 · 앱 · FAQ 를 `@id` 로 이은 그래프 하나다. 별점 · 리뷰는 스토어에 생기기 전이라 넣지 않는다 — 없는 값을 지어 넣지 않는다
  - `/dayline/` 진입 주소는 스크립트를 돌리지 않는 로봇도 읽게 영어 한 줄 소개와 언어 목록을 싣고, 영어 랜딩을 대표 주소(canonical)로 알린다
  - 스토어 버튼: Play 는 패키지 이름(`com.zacolabs.dayline`)으로 주소를 만든다. App Store 는 번들 ID 로는 주소를 만들 수 없어, App Store Connect 의 Apple ID(앱 정보 → 일반 정보의 숫자)를 `dayline_landing.py` 의 `APPLE_ID` 에 둔다 — `None` 이면 App Store 버튼이 링크 없이 "출시 예정"으로 나온다
  - 그림(`dayline/assets/illustration/hero.webp` · `step-1~3.webp`)은 Waky 랜딩과 같은 화풍의 먹선 그림이다. ChatGPT 의 이미지 생성으로, Waky 그림 한 장을 화풍 참고로 올려 같은 인물로 네 장을 이어 그렸다 — 다시 만드는 법은 `scripts/dayline/landing/art.py` 머리말. 글자가 없어 모든 언어 공용
  - 그림에는 색이 없고, 색은 그 위에 얹는 선뿐이다: `art.py` 의 `TRAILS` 가 그림마다 지나온 길을 이동수단의 색으로 그린다 (좌표는 그림을 1000x1000 으로 본 자리). 3번 컷은 전화기 화면에 그려져 있던 선을 흰 화면으로 덮고 다시 그린다. 그림을 바꾸면 이 좌표를 발과 땅에 맞게 고친다
  - 그림과 하루 화면의 선은 스크롤해서 화면에 들어올 때 그려진다 (`[data-inview]` 에 `.in` 이 붙는다). 스크립트가 없거나 기기가 움직임을 줄이라고 하면 처음부터 다 그려진 채다
  - 기능 옆의 **하루 화면**은 그림 파일이 아니라 `dayline_landing.py` 의 `day_card` 가 HTML · SVG 로 그린다 (길 · 거리 · 색은 스토어 그림 3번과 같다). 화면에 들어오면 선이 구간 순서대로 그려지고, 그동안 거리가 0 에서부터 올라가고 막대와 줄이 따라 나온다. 카드 안의 글(`km` · 이동 시간 · 이동수단 이름)은 문구 파일의 `day` — 스토어 그림의 `text.js` 와 맞춘다
  - `dayline/assets/og-<언어>.png`(공유 미리보기)는 `scripts/dayline/landing/make_assets.py` 가 앱 저장소의 Play 피처 그래픽에서 만든다 (`dayline-android` 가 옆에 있어야 하고 Pillow 필요). 빌드는 이걸 돌리지 않는다
- `zacolabs-assets/` — `index.html` 이 쓰는 로고·앱 아이콘 (`waky-web/src/main/resources/zacolabs-assets/`)
  - `dayline_icon.png` — Dayline 앱 아이콘 (`dayline-android` `store/play/icon-512.png`)
  - `og-image-1200x630.png` — 공유 미리보기 그림(모든 언어 공용). `scripts/og-image.html` 을 크롬에서 1200×630 으로 찍은 것
