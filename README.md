# zacolabs.github.io

`https://zacolabs.github.io/` 도메인 맨 앞에 두어야 하는 파일만 둔다. 랜딩 페이지는 `zacolabs/waky-landing` 저장소(`/waky-landing/`)에 있다.

- `app-ads.txt` — AdMob 이 스토어의 개발자 웹사이트 도메인 맨 앞에서만 찾는다. 게시자 `pub-7125409961311406`
- `robots.txt` — 검색엔진은 도메인 맨 앞의 이 파일만 읽는다. 랜딩 사이트맵을 여기서 알린다
- `index.html` · `<언어>/index.html` — 회사 소개 페이지. **`scripts/build.py` 가 만든다 — 직접 고치지 말 것.** 영어는 도메인 맨 앞(`/`), 다른 17개 언어는 `/ko/` · `/ja/` … 에 둔다 (언어 목록은 waky-landing 과 같다). 옛 `/en/` 은 `/` 로 넘긴다
  - 문구는 `scripts/i18n/<언어>.json`, 모양은 `scripts/style.css` 에서 고치고 `python3 scripts/build.py` 를 돌린다. `sitemap.xml` 도 같이 다시 쓴다
  - `/` 로 온 사람의 언어: ① 오른쪽 위 언어 메뉴(두이레와 같은 모양)로 고른 언어(`localStorage` 의 `zacolabs-lang`) ② 없으면 접속 지역 — 정적 호스팅이라 IP 를 볼 수 없어 기기 시간대로 가린다(`build.py` `TZ_LANG`) ③ 모르면 영어. 검색 로봇은 옮기지 않는다
  - Waky 자세히 보기는 그 언어 랜딩으로 건다. 두이레는 한국어 · 영어뿐이라 한국어가 아니면 `duire.kr/en` 으로 보낸다
- 서치 콘솔 확인 태그는 맨 앞(영어) 페이지에만 있다
- `zacolabs-assets/` — `index.html` 이 쓰는 로고·앱 아이콘 (`waky-web/src/main/resources/zacolabs-assets/`)
