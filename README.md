# zacolabs.github.io

`https://zacolabs.github.io/` 도메인 맨 앞에 두어야 하는 파일만 둔다. 랜딩 페이지는 `zacolabs/waky-landing` 저장소(`/waky-landing/`)에 있다.

- `app-ads.txt` — AdMob 이 스토어의 개발자 웹사이트 도메인 맨 앞에서만 찾는다. 게시자 `pub-7125409961311406`
- `robots.txt` — 검색엔진은 도메인 맨 앞의 이 파일만 읽는다. 랜딩 사이트맵을 여기서 알린다
- `index.html` · `<언어>/index.html` — 회사 소개 페이지. **`scripts/build.py` 가 만든다 — 직접 고치지 말 것.** 한국어는 도메인 맨 앞(`/`), 다른 17개 언어는 `/en/` · `/ja/` … 에 둔다 (언어 목록은 waky-landing 과 같다)
  - 문구는 `scripts/i18n/<언어>.json`, 모양은 `scripts/style.css` 에서 고치고 `python3 scripts/build.py` 를 돌린다. `sitemap.xml` 도 같이 다시 쓴다
  - 오른쪽 위 언어 메뉴(두이레와 같은 모양)로 고른 언어는 `localStorage` 의 `zacolabs-lang` 에 남고, 다음에 `/` 로 오면 그 언어로 옮긴다. 처음 온 사람은 옮기지 않는다
  - Waky 자세히 보기는 한국어면 `/waky-landing/introduce/`(랜딩이 언어를 고른다), 다른 언어면 그 언어 랜딩으로 건다. 두이레는 한국어 · 영어뿐이라 다른 언어는 `duire.kr/en` 으로 보낸다
- `zacolabs-assets/` — `index.html` 이 쓰는 로고·앱 아이콘 (`waky-web/src/main/resources/zacolabs-assets/`)
