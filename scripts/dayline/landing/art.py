#!/usr/bin/env python3
"""Dayline 랜딩의 그림 위에 얹는 선(SVG)을 만든다. dayline_landing.py 가 불러 쓴다.

그림(dayline/assets/illustration/*.webp)은 Waky 랜딩과 같은 화풍의 먹선 그림이고, 색이 없다.
색은 이 선뿐이다 — 지나온 길을 이동수단의 색으로, 앱이 그리는 것과 같은 굵은 선으로 그림 위에 얹는다.
선은 그림이 화면에 들어올 때 그려진다 (모양은 style.css 의 .leg · .pin, 켜는 것은 페이지의 스크립트).

그림을 다시 만들 때: 그림은 ChatGPT 의 이미지 생성으로 만들었다. Waky 의 그림 한 장을 화풍 참고로 올리고
"같은 화풍의 새 인물 — 높이 묶은 머리, 가로 줄무늬 티셔츠, 검은 반바지, 흰 운동화. 흰 격자 종이에 먹선만,
볼의 옅은 분홍 말고는 색 없이, 글자 없이, 정사각형" 으로 한 대화 안에서 네 장을 이어 그린다
(달리기 / 집을 나서 걷기 / 운전 / 소파에서 전화기 보기). 선을 얹을 땅과 왼쪽은 비워 달라고 한다.
받은 그림은 바탕을 흰색으로 맞추고 히어로 1000px, 3컷 800px WebP 로 줄인다.
그림이 바뀌면 아래 TRAILS 의 좌표(그림을 1000x1000 으로 본 자리)를 사람의 발과 땅에 맞게 고친다.
"""

INK = "#111113"
PAPER = "#ffffff"
# 앱의 라이트 팔레트 (dayline-ios Assets.xcassets Mode*.colorset)
WALK, RUN, CYCLE, CAR, HERE = "#00c97b", "#ff4d26", "#6a45ff", "#0a8fff", "#007aff"
SIZE = 1000  # 좌표계. 그림은 모두 정사각형이다.

# 그림마다: 선의 굵기, 다 그리는 데 걸리는 초, 구간(색, 시작점, 이어지는 곡선들), 끝의 표시.
# 곡선은 SVG 의 C(조절점 둘과 끝점) 또는 L(끝점). 끝 표시 "here" 는 지금 위치(파란 점), "stop" 은 도착(검은 점).
TRAILS = {
    # 걸어서 나와(초록) 달린다(주황). 선은 왼쪽 빈 종이에서 발 아래로 들어온다.
    "hero": dict(width=22, seconds=1.9, end="here", legs=[
        (WALK, (115, 190), [("C", (300, 190), (370, 300), (290, 400)), ("C", (215, 495), (90, 510), (125, 640))]),
        (RUN, (125, 640), [("C", (155, 790), (270, 945), (470, 945)), ("L", (760, 945))]),
    ]),
    # 문 앞에서 시작해 걷는다.
    "step-1": dict(width=22, seconds=1.2, end="here", legs=[
        (WALK, (300, 818), [("C", (325, 905), (385, 950), (480, 950)), ("L", (645, 950))]),
    ]),
    # 걷고(초록) 뛰다가(주황) 차를 탄다(파랑). 파란 선은 차 바퀴 아래를 지난다.
    "step-2": dict(width=22, seconds=1.9, end="here", legs=[
        (WALK, (95, 170), [("C", (230, 170), (260, 290), (190, 360))]),
        (RUN, (190, 360), [("C", (120, 430), (70, 540), (130, 640))]),
        (CAR, (130, 640), [("C", (190, 760), (300, 852), (430, 852)), ("L", (700, 852))]),
    ]),
    # 전화기 화면 속 하루의 선: 도보, 차량, 자전거, 달리기. 그림에 그려진 선을 앱의 선 보기 같은 격자 판으로 덮고
    # 다시 그린다. 판(x, y, 가로, 세로, 모서리)은 화면 안쪽(631~946, 168~799)에 둘레를 18 씩 남긴 자리다.
    "step-3": dict(width=17, seconds=2.2, end="stop", cover=(649, 190, 279, 591, 24), legs=[
        (WALK, (668, 686), [("C", (690, 650), (704, 628), (700, 596)), ("C", (696, 566), (716, 548), (742, 540))]),
        (CAR, (742, 540), [("C", (776, 530), (806, 524), (818, 494)), ("C", (830, 464), (796, 432), (800, 398))]),
        (CYCLE, (800, 398), [("C", (804, 372), (822, 362), (846, 354))]),
        (RUN, (846, 354), [("C", (876, 344), (902, 326), (902, 290))]),
    ]),
}


def cubic_length(p0, p1, p2, p3, steps=24):
    """곡선의 길이를 잘게 나눠 잰다 — 구간마다 걸리는 시간을 길이에 맞추려고."""
    total, prev = 0.0, p0
    for i in range(1, steps + 1):
        t = i / steps
        u = 1 - t
        x = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
        y = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
        total += ((x - prev[0]) ** 2 + (y - prev[1]) ** 2) ** .5
        prev = (x, y)
    return total


def leg_path(start, segments):
    """구간의 SVG 경로와 길이, 끝점."""
    d, at, length = f"M{start[0]} {start[1]}", start, 0.0
    for kind, *pts in segments:
        if kind == "C":
            d += " C" + " ".join(f"{x} {y}" for x, y in pts)
            length += cubic_length(at, *pts)
        else:
            d += f" L{pts[0][0]} {pts[0][1]}"
            length += ((pts[0][0] - at[0]) ** 2 + (pts[0][1] - at[1]) ** 2) ** .5
        at = pts[-1]
    return d, length, at


def overlay(name):
    """그림 name 위에 얹을 SVG. 구간마다 그려지는 때(--d)와 걸리는 시간(--t)을 길이에 맞춰 준다."""
    t = TRAILS[name]
    width = t["width"]
    legs = [(color, start) + leg_path(start, segments) for color, start, segments in t["legs"]]
    total = sum(length for _, _, _, length, _ in legs)
    s, at = "", 0.0
    if "cover" in t:
        x, y, w, h, r = t["cover"]
        step = w / 6
        grid = "".join(f'<path d="M{x + i * step:.1f} {y}v{h}"/>' for i in range(1, 6))
        grid += "".join(f'<path d="M{x} {y + i * step:.1f}h{w}"/>' for i in range(1, int(h / step) + 1))
        s += (f'<clipPath id="{name}-cover"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{PAPER}"/>'
              f'<g clip-path="url(#{name}-cover)" stroke="rgba(0,0,0,.09)" stroke-width="2.5">{grid}</g>'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" stroke="rgba(0,0,0,.16)" stroke-width="2.5"/>')
    for color, _, d, length, _ in legs:
        took = t["seconds"] * length / total
        s += (f'<path class="leg" pathLength="1" style="--d:{at:.2f}s;--t:{took:.2f}s" d="{d}" fill="none" '
              f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
        at += took
    sx, sy = legs[0][1]
    ex, ey = legs[-1][4]
    r = width * .72
    s += f'<circle class="pin" cx="{sx}" cy="{sy}" r="{r:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="{r * .62:.1f}"/>'
    if t["end"] == "here":
        s += (f'<g class="pin" style="--d:{at:.2f}s"><circle class="halo" cx="{ex}" cy="{ey}" r="{r * 2.6:.1f}" fill="{HERE}" opacity=".18"/>'
              f'<circle cx="{ex}" cy="{ey}" r="{r * 1.1:.1f}" fill="{HERE}" stroke="{PAPER}" stroke-width="{r * .45:.1f}"/></g>')
    else:
        s += f'<circle class="pin" style="--d:{at:.2f}s" cx="{ex}" cy="{ey}" r="{r:.1f}" fill="{INK}" stroke="{PAPER}" stroke-width="{r * .4:.1f}"/>'
    return f'<svg class="trail" viewBox="0 0 {SIZE} {SIZE}" aria-hidden="true">{s}</svg>'
