# zacolabs.github.io

`https://zacolabs.github.io/` 도메인 맨 앞에 두어야 하는 파일만 둔다. 랜딩 페이지는 `zacolabs/waky-landing` 저장소(`/waky-landing/`)에 있다.

- `app-ads.txt` — AdMob 이 스토어의 개발자 웹사이트 도메인 맨 앞에서만 찾는다. 게시자 `pub-7125409961311406`
- `robots.txt` — 검색엔진은 도메인 맨 앞의 이 파일만 읽는다. 랜딩 사이트맵을 여기서 알린다
- `index.html` — 회사 소개 페이지. `waky` 저장소 `waky-web` 이 내는 `/zacolabs?page=about&lang=ko` 를 그대로 떠 왔다. 주소(canonical·og:url)를 이 도메인으로 바꾸고, 그 서버(kwonho87.asuscomm.com)를 더 쓰지 않아 언어 전환 줄은 뺐다. Waky 자세히 보기는 `/waky-landing/introduce/` 로 건다
- `zacolabs-assets/` — `index.html` 이 쓰는 로고·앱 아이콘 (`waky-web/src/main/resources/zacolabs-assets/`)
