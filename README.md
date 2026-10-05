# zacolabs.github.io

`https://zacolabs.github.io/` 도메인 맨 앞에 두어야 하는 파일과, 따로 저장소를 두지 않은 Dayline 의 약관 페이지를 둔다. Waky 랜딩 페이지는 `zacolabs/waky-landing` 저장소(`/waky-landing/`)에 있다.

- `app-ads.txt` — AdMob 이 스토어의 개발자 웹사이트 도메인 맨 앞에서만 찾는다. 게시자 `pub-7125409961311406`
- `robots.txt` — 검색엔진은 도메인 맨 앞의 이 파일만 읽는다. 랜딩 사이트맵을 여기서 알린다
- `index.html` · `<언어>/index.html` — 회사 소개 페이지. **`scripts/build.py` 가 만든다 — 직접 고치지 말 것.** 영어는 도메인 맨 앞(`/`), 다른 17개 언어는 `/ko/` · `/ja/` … 에 둔다 (언어 목록은 waky-landing 과 같다). 옛 `/en/` 은 `/` 로 넘긴다
  - 문구는 `scripts/i18n/<언어>.json`, 모양은 `scripts/style.css` 에서 고치고 `python3 scripts/build.py` 를 돌린다. `sitemap.xml` 도 같이 다시 쓴다
  - `/` 로 온 사람의 언어: ① 오른쪽 위 언어 메뉴(두이레와 같은 모양)로 고른 언어(`localStorage` 의 `zacolabs-lang`) ② 없으면 접속 지역 — 정적 호스팅이라 IP 를 볼 수 없어 기기 시간대로 가린다(`build.py` `TZ_LANG`) ③ 모르면 영어. 검색 로봇은 옮기지 않는다
  - Waky 자세히 보기는 그 언어 랜딩으로 건다. 두이레는 한국어 · 영어뿐이라 한국어가 아니면 `duire.kr/en` 으로 보낸다
  - Dayline 카드는 아직 스토어에 나가지 않아 버튼 자리에 "출시 예정"이 나온다. 스토어 주소가 생기면 `build.py` 의 `DAYLINE_PLAY` · `DAYLINE_APPLE` 에 넣는다 — 넣은 스토어의 버튼만 나온다
- 서치 콘솔 확인 태그는 맨 앞(영어) 페이지에만 있다
- `dayline/` — Dayline 의 이용 약관 · 개인정보 처리방침 · 오픈소스 라이선스. **`scripts/dayline_legal.py` 가 만든다 — 직접 고치지 말 것** (`build.py` 가 같이 돌린다)
  - 약관 · 개인정보 처리방침의 본문은 `scripts/dayline/<문서>.<언어>.html`, 모양은 `scripts/dayline/style.css`. **이 본문이 기준이다** — 앱은 글을 따로 싣지 않고 이 주소를 연다. Waky 의 같은 페이지(`zacolabs-backend` `src/content/waky/legal`)에서 따와 Dayline 에 맞게 고친 것이라, 구조와 모양은 그쪽과 맞춘다
  - 라이선스는 언어마다 다른 글이 몇 줄뿐이라 본문 하나(`scripts/dayline/licenses.html`)의 `{{…}}` 자리에 `scripts/dayline/strings.json` 의 문구를 채운다. 문서 제목도 `strings.json` 에 있다
  - 주소도 Waky 와 같다: `/dayline/privacy.html?lang=ko&theme=light` (`terms` · `licenses` 도 같다). `?lang=` → 브라우저 언어 → 영어 순으로 언어를 정하고, `theme` 이 없으면 다크다. 언어를 고정한 주소는 `/dayline/privacy.ko.html` · `privacy.zh-hans.html` 처럼 언어 태그를 소문자로 쓴다
  - Waky 는 서버가 `?lang=` · `?theme=` 을 읽지만 여기는 정적 호스팅이라 페이지 안의 스크립트가 읽는다
  - 언어는 Dayline 앱과 같은 18개. 앱은 `?lang=` 에 앱 언어 태그(`zh-Hans`, `fil` …)를 그대로 싣는다. 한국어가 원문이고 나머지는 번역이다 — 글을 고치면 한국어부터 고치고 18개를 함께 맞춘다. 언어를 늘릴 때는 `dayline_legal.py` 의 `LANGS`, `strings.json`, 본문 파일을 더한다
  - 아랍어는 오른쪽에서 왼쪽으로 쓴다 (`dayline_legal.py` `RTL`)
  - `zacolabs` 조직에 `dayline` 이라는 이름의 저장소로 Pages 를 켜면 이 주소와 겹친다
- `zacolabs-assets/` — `index.html` 이 쓰는 로고·앱 아이콘 (`waky-web/src/main/resources/zacolabs-assets/`)
  - `dayline_icon.png` — Dayline 앱 아이콘 (`dayline-android` `store/play/icon-512.png`)
  - `og-image-1200x630.png` — 공유 미리보기 그림(모든 언어 공용). `scripts/og-image.html` 을 크롬에서 1200×630 으로 찍은 것
