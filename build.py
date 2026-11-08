#!/usr/bin/env python3
"""
Builds the whole GitHub profile from ONE file: profile.json

    python build.py

It (re)generates:
    README.md                    the profile page itself
    assets/hero.svg              animated banner with your photo
    assets/portrait.svg          animated dot-matrix portrait
    assets/tech-stack.svg        scrolling tech-stack rows
    assets/projects.svg          animated project cards
    assets/terminal.svg          typing developer console
    assets/h-*.svg               animated section headers
    assets/footer.svg            animated wave footer

To ADD or REMOVE anything, edit profile.json and run this again.
No packages needed (Python 3.8+ standard library only).
"""
import base64
import html
import json
import math
import os
import random
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
P = json.load(open(os.path.join(ROOT, "profile.json"), encoding="utf-8"))

# ----------------------------------------------------------------- theme
BG, CARD, LINE = "#050b16", "#071525", "#16324d"
CYAN, VIOLET, PINK, GREEN = "#22d3ee", "#8b5cf6", "#ec4899", "#34f5c5"
TEXT, MUTED = "#eef4ff", "#9ab0c9"
MONO = "'Fira Code','JetBrains Mono',Consolas,'Courier New',monospace"
SANS = "Inter,'Segoe UI',Roboto,Arial,sans-serif"

TECH_COLORS = {
    "HTML5": "#e34f26", "CSS3": "#38a3e8", "JavaScript": "#f7df1e", "TypeScript": "#3b82f6",
    "Java": "#f89820", "Python": "#5aa9e6", "C#": "#a855f7", "PHP": "#8892bf",
    "React": "#61dafb", "Next.js": "#ffffff", "Node.js": "#6cc24a", "NestJS": "#e0234e",
    "Express": "#cbd5e1", "React Native": "#7dd3fc", "Flutter": "#54c5f8",
    "MySQL": "#5b9bd5", "PostgreSQL": "#6ea8e0", "MongoDB": "#4ade80", "Firebase": "#ffca28",
    "Redis": "#dc382d", "Git": "#f05032", "Docker": "#2496ed", "AWS": "#ff9900", "Figma": "#f24e1e",
    "Laravel": "#ff2d20", "Spring Boot": "#6db33f", "Angular": "#dd0031", "Vue": "#42b883",
    "Tailwind": "#38bdf8", "Kotlin": "#a97bff", "Swift": "#fa7343", "Go": "#00add8",
    "Rust": "#dea584", "Linux": "#fcc624", "GraphQL": "#e10098", "SQLite": "#7cc4f0",
}


def esc(s):
    return html.escape(str(s), quote=True)


def svg(w, h, body, defs="", style="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"<title>{esc(title)}</title>\n<defs>{defs}</defs>\n"
        + (f"<style>{style}</style>\n" if style else "")
        + body
        + "\n</svg>\n"
    )


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def fmt(vals):
    return ";".join(f"{v:.4f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v) for v in vals)


def timeline(attr, v0, v1, ts, te, tr, T):
    """SMIL animation: sit at v0, ease to v1 between ts..te, hold until tr, snap back, loop every T seconds."""
    tr = min(tr, T - 0.05)
    kt = [0, ts / T, te / T, tr / T, min(tr / T + 0.003, 0.999), 1]
    vals = [v0, v0, v1, v1, v0, v0]
    return (
        f'<animate attributeName="{attr}" values="{fmt(vals)}" keyTimes="{fmt(kt)}" '
        f'dur="{T:.2f}s" repeatCount="indefinite"/>'
    )


def pop(ts, tr, T, fade=0.35):
    """Opacity 0 -> 1 at ts, back to 0 at tr, looping."""
    return timeline("opacity", 0, 1, ts, ts + fade, tr, T)


# ------------------------------------------------------------ data bits
def avatar_b64():
    p = os.path.join(ASSETS, "avatar.jpg")
    if not os.path.exists(p):
        return None
    return base64.b64encode(open(p, "rb").read()).decode()


def portrait_data():
    p = os.path.join(ASSETS, "portrait.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p))


# ------------------------------------------------------------------ hero
def build_hero():
    W, H = 1200, 460
    rnd = random.Random(7)
    cx, cy = 955, 262
    first, last = esc(P["first_name"]), esc(P["last_name"])
    role = f'{P["role"]} at {P["company"]}'
    sub = f'{P["location"]}  |  Building {P["building"]}'

    defs = f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06111f"/><stop offset=".5" stop-color="#071a2e"/><stop offset="1" stop-color="#0b1020"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="shimmer" gradientUnits="objectBoundingBox" spreadMethod="reflect" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}"/>
  <animate attributeName="x1" values="0;1;0" dur="7s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="1;2;1" dur="7s" repeatCount="indefinite"/>
</linearGradient>
<radialGradient id="gridfade" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#gridfade)"/></mask>
<pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
  <path d="M44 0H0V44" fill="none" stroke="#1d3f66" stroke-width="1" opacity=".55"/>
  <animateTransform attributeName="patternTransform" type="translate" values="0 0;44 44" dur="9s" repeatCount="indefinite"/>
</pattern>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="avatar"><circle cx="{cx}" cy="{cy}" r="124"/></clipPath>
"""
    css = """
.in{opacity:0;animation:in .9s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes in{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.fl{animation:fl 5s ease-in-out infinite}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.bl{animation:bl 1.1s steps(1) infinite}
@keyframes bl{50%{opacity:0}}
"""
    b = [f'<g clip-path="url(#frame)">', f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    # drifting colour blobs
    for (x0, y0, r, col, dur, op) in [(180, 120, 190, CYAN, 22, .30), (620, 420, 210, VIOLET, 27, .32), (1040, 150, 200, PINK, 31, .26)]:
        b.append(
            f'<circle cx="{x0}" cy="{y0}" r="{r}" fill="{col}" opacity="{op}" filter="url(#blur)">'
            f'<animate attributeName="cx" values="{x0};{x0 + 140};{x0 - 80};{x0}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{y0};{y0 - 70};{y0 + 60};{y0}" dur="{dur + 5}s" repeatCount="indefinite"/></circle>'
        )
    b.append(f'<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)"/>')
    # twinkling particles
    for _ in range(34):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(90, H - 30)
        r = rnd.choice([1.2, 1.6, 2.0, 2.6])
        col = rnd.choice([CYAN, VIOLET, PINK, "#ffffff"])
        d = rnd.uniform(5, 11)
        b.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" opacity="0">'
            f'<animate attributeName="cy" values="{y:.0f};{y - 70:.0f}" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.9;0" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>'
        )
    b.append("</g>")
    # frame + window bar
    b.append(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="27" fill="none" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<rect x="38" y="30" width="{W - 76}" height="40" rx="18" fill="#081425" stroke="{LINE}"/>')
    b.append(f'<circle cx="1080" cy="50" r="5" fill="#60a5fa"/><circle cx="1104" cy="50" r="5" fill="#a78bfa"/><circle cx="1128" cy="50" r="5" fill="#f472b6"/>')
    b.append(
        f'<text x="62" y="57" fill="{GREEN}" font-family="{MONO}" font-size="22" font-weight="700">~/{esc(P["github"])}  &gt;  profile --ultimate</text>'
    )
    # left text
    b.append(f'<g class="in" style="animation-delay:.1s"><text x="70" y="150" fill="{CYAN}" font-family="{MONO}" font-size="30" font-weight="700">&gt; whoami</text></g>')
    b.append(f'<g class="in" style="animation-delay:.3s"><text x="68" y="226" fill="{TEXT}" font-family="{SANS}" font-size="68" font-weight="800" letter-spacing="-1">{first}</text></g>')
    b.append(f'<g class="in" style="animation-delay:.5s"><text x="68" y="296" fill="url(#shimmer)" font-family="{SANS}" font-size="68" font-weight="800" letter-spacing="-1">{last}</text></g>')
    b.append(f'<g class="in" style="animation-delay:.8s"><text x="70" y="338" fill="#dbe6ff" font-family="{MONO}" font-size="24">{esc(role)}</text>'
             f'<text x="70" y="370" fill="{MUTED}" font-family="{MONO}" font-size="19">{esc(sub)}</text></g>')
    # typing line
    lines = P["typing_lines"]
    D = 3.9
    T = D * len(lines)
    cw, fs = 15.6, 26
    tx, ty = 100, 424
    b.append(f'<text x="70" y="{ty}" fill="{GREEN}" font-family="{MONO}" font-size="{fs}" font-weight="700">&gt;</text>')
    clips = []
    for i, line in enumerate(lines):
        n = len(line)
        wpx = n * cw
        ts = i * D + 0.2
        te = ts + min(n * 0.065, D * 0.55)
        tr = i * D + D - 0.3
        clips.append(f'<clipPath id="tc{i}"><rect x="{tx}" y="{ty - 28}" width="0" height="38">{timeline("width", 0, wpx, ts, te, tr, T)}</rect></clipPath>')
        b.append(
            f'<text x="{tx}" y="{ty}" textLength="{wpx:.0f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#tc{i})" '
            f'fill="#c7f4ff" font-family="{MONO}" font-size="{fs}">{esc(line)}</text>'
        )
        b.append(
            f'<rect x="{tx}" y="{ty - 24}" width="3" height="30" fill="{CYAN}" opacity="0">'
            f'{timeline("x", tx, tx + wpx, ts, te, tr, T)}{pop(ts, tr + 0.2, T, 0.05)}</rect>'
        )
    defs += "".join(clips)
    # avatar + rings
    b.append(f'<circle cx="{cx}" cy="{cy}" r="135" fill="url(#ring)" opacity=".5" filter="url(#blur)"><animate attributeName="opacity" values=".25;.6;.25" dur="4s" repeatCount="indefinite"/></circle>')
    img = avatar_b64()
    if img:
        b.append(
            f'<g class="in" style="animation-delay:.4s">'
            f'<image x="{cx - 124}" y="{cy - 124}" width="248" height="248" clip-path="url(#avatar)" preserveAspectRatio="xMidYMid slice" '
            f'href="data:image/jpeg;base64,{img}" xlink:href="data:image/jpeg;base64,{img}"/></g>'
        )
    b.append(f'<circle cx="{cx}" cy="{cy}" r="124" fill="none" stroke="url(#ring)" stroke-width="3"/>')
    b.append(
        f'<g transform="translate({cx} {cy})">'
        f'<circle r="140" fill="none" stroke="url(#ring)" stroke-width="3" stroke-linecap="round" stroke-dasharray="190 690"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="7s" repeatCount="indefinite"/></circle>'
        f'<circle r="154" fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="3 12" opacity=".7"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="30s" repeatCount="indefinite"/></circle>'
        f'<circle r="168" fill="none" stroke="{PINK}" stroke-width="1" stroke-dasharray="40 120" opacity=".6"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="18s" repeatCount="indefinite"/></circle>'
        f'<g><circle cx="168" cy="0" r="6" fill="{CYAN}" filter="url(#glow)"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/></g>'
        f'<g><circle cx="-154" cy="0" r="5" fill="{PINK}" filter="url(#glow)"/><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="13s" repeatCount="indefinite"/></g>'
        f"</g>"
    )
    # floating chips
    chips = P.get("floating_chips", [])
    spots = [(cx + 78, cy - 176), (cx + 112, cy + 122), (cx - 262, cy - 128)]
    for i, text in enumerate(chips[:3]):
        wch = len(text) * 9.6 + 36
        x, y = spots[i]
        x = min(x, W - 30 - wch)
        b.append(
            f'<g class="fl" style="animation-delay:{i * 1.3}s"><g transform="translate({x:.0f} {y})">'
            f'<rect width="{wch:.0f}" height="34" rx="17" fill="#081425" stroke="url(#ring)" stroke-width="1.5"/>'
            f'<circle cx="18" cy="17" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>'
            f'<text x="30" y="23" fill="{TEXT}" font-family="{MONO}" font-size="15" font-weight="600">{esc(text)}</text></g></g>'
        )
    # bottom sweep line
    b.append(f'<rect x="40" y="{H - 26}" width="{W - 80}" height="3" rx="1.5" fill="{LINE}"/>')
    b.append(
        f'<rect x="40" y="{H - 26}" width="260" height="3" rx="1.5" fill="url(#acc)" filter="url(#glow)">'
        f'<animate attributeName="x" values="40;{W - 300};40" dur="6s" repeatCount="indefinite"/></rect>'
    )
    write("assets/hero.svg", svg(W, H, "\n".join(b), defs, css, f'{P["name"]} - {role}'))


# -------------------------------------------------------------- portrait
def build_portrait():
    d = portrait_data()
    if not d:
        return False
    n, rows_n, hexes = d["cols"], d["rows"], d["hex"]
    cell, pad, top = 7.6, 26, 58
    W = int(n * cell + pad * 2)
    H = int(rows_n * cell + top + 30)
    defs = f"""
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/></linearGradient>
<filter id="glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="inner"><rect x="12" y="{top - 14}" width="{W - 24}" height="{H - top - 2}" rx="10"/></clipPath>
"""
    T = 6.0
    css = (
        ".r{opacity:0;animation:sw %.1fs ease-in-out infinite both}"
        "@keyframes sw{0%%{opacity:.35}12%%{opacity:1}35%%{opacity:.62}100%%{opacity:.35}}" % T
    )
    b = [
        f'<rect width="{W}" height="{H}" rx="20" fill="{CARD}"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="19" fill="none" stroke="{LINE}" stroke-width="2"/>',
        f'<text x="{pad}" y="34" fill="{GREEN}" font-family="{MONO}" font-size="15" font-weight="700">// portrait.dots</text>',
        f'<circle cx="{W - 80}" cy="29" r="5" fill="#60a5fa"/><circle cx="{W - 56}" cy="29" r="5" fill="#a78bfa"/><circle cx="{W - 32}" cy="29" r="5" fill="#f472b6"/>',
        '<g clip-path="url(#inner)">',
    ]
    for y in range(rows_n):
        dots = []
        for x in range(n):
            hx = hexes[y * n + x]
            r_, g_, b_ = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
            lum = (0.299 * r_ + 0.587 * g_ + 0.114 * b_) / 255
            # lift dark tones so a dark suit/hair stays visible on the dark card
            lift = lambda v: int(255 * (v / 255) ** 0.62)
            hx = "%02x%02x%02x" % (lift(r_), lift(g_), lift(b_))
            rad = cell * (0.27 + 0.25 * lum ** 0.6)
            dots.append(f'<circle cx="{pad + x * cell + cell / 2:.1f}" cy="{top + y * cell + cell / 2:.1f}" r="{rad:.1f}" fill="#{hx}"/>')
        b.append(f'<g class="r" style="animation-delay:{y * 0.09:.2f}s">' + "".join(dots) + "</g>")
    b.append("</g>")
    b.append(
        f'<g clip-path="url(#inner)"><rect x="12" y="{top - 14}" width="{W - 24}" height="46" fill="url(#scan)" opacity=".6">'
        f'<animate attributeName="y" values="{top - 60};{H - 30};{top - 60}" dur="{T}s" repeatCount="indefinite"/></rect>'
        f'<rect x="12" y="{top - 14}" width="{W - 24}" height="2" fill="{CYAN}" filter="url(#glow)">'
        f'<animate attributeName="y" values="{top - 14};{H - 14};{top - 14}" dur="{T}s" repeatCount="indefinite"/></rect></g>'
    )
    for (x, y, sx, sy) in [(12, top - 14, 1, 1), (W - 12, top - 14, -1, 1), (12, H - 16, 1, -1), (W - 12, H - 16, -1, -1)]:
        b.append(f'<path d="M{x} {y + 16 * sy}V{y}H{x + 16 * sx}" fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round"/>')
    write("assets/portrait.svg", svg(W, H, "\n".join(b), defs, css, f'Dot-matrix portrait of {P["name"]}'))
    return True


# ------------------------------------------------------------- tech rows
def build_tech():
    rows = []
    for g in P["tech"]:
        items = []
        for name in g["items"]:
            col = TECH_COLORS.get(name, VIOLET)
            items.append((name, col, len(name) * 11.8 + 58))
        rows.append((g["group"], items))
    W, ph, gap, rgap = 1200, 46, 16, 18
    top = 26
    H = top * 2 + len(rows) * ph + (len(rows) - 1) * rgap
    defs = f"""
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".09" stop-color="#fff"/><stop offset=".91" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="fade"><rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
"""
    b = [
        f'<rect width="{W}" height="{H}" rx="22" fill="{CARD}"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="21" fill="none" stroke="{LINE}" stroke-width="2"/>',
        '<g mask="url(#fade)">',
    ]
    for r, (gname, items) in enumerate(rows):
        y = top + r * (ph + rgap)
        one = sum(w for _, _, w in items) + gap * len(items)
        k = max(2, math.ceil((W + one) / one) + 1)
        pills, x = [], 0
        for _ in range(k):
            for name, col, w in items:
                pills.append(
                    f'<g transform="translate({x:.0f} {y})"><rect width="{w:.0f}" height="{ph}" rx="14" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/>'
                    f'<circle cx="24" cy="{ph / 2}" r="5.5" fill="{col}"/>'
                    f'<text x="40" y="{ph / 2 + 7}" fill="{TEXT}" font-family="{SANS}" font-size="20" font-weight="700">{esc(name)}</text></g>'
                )
                x += w + gap
        dur = one / 42
        frm, to = (0, -one) if r % 2 == 0 else (-one, 0)
        b.append(
            f'<g><animateTransform attributeName="transform" type="translate" values="{frm} 0;{to:.0f} 0" dur="{dur:.1f}s" repeatCount="indefinite"/>'
            + "".join(pills)
            + "</g>"
        )
    b.append("</g>")
    write("assets/tech-stack.svg", svg(W, H, "\n".join(b), defs, "", "Technology stack: " + ", ".join(i for g in P["tech"] for i in g["items"])))


# --------------------------------------------------------------- projects
def build_projects():
    prs = P["projects"]
    if not prs:
        return False
    W, gap = 1200, 24
    cols = 2 if len(prs) > 1 else 1
    cw_ = (W - gap * (cols - 1)) // cols
    inner = cw_ - 72
    chars = int(inner / 9.4)

    def layout(p):
        desc = textwrap.wrap(p["description"], chars)[:3]
        rows, x, cur = 1, 0, []
        pos = []
        for t in p.get("tags", []):
            w = len(t) * 9.4 + 30
            if x + w > inner and x > 0:
                rows += 1
                x = 0
            pos.append((t, x, rows - 1, w))
            x += w + 10
        return desc, pos, rows

    laid = [layout(p) for p in prs]
    ch = max(150 + 27 * len(d) + 40 + 44 * r + 26 for d, _, r in laid)
    nrows = math.ceil(len(prs) / cols)
    H = nrows * ch + (nrows - 1) * gap
    defs = f"""
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1c33"/><stop offset="1" stop-color="#08111f"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""
    css = ".in{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}@keyframes in{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"
    b = []
    for i, (p, (desc, pos, trows)) in enumerate(zip(prs, laid)):
        x0 = (i % cols) * (cw_ + gap)
        y0 = (i // cols) * (ch + gap)
        nm = p["name"]
        nfs = 28 if len(nm) <= 30 else 22
        g = [f'<g class="in" style="animation-delay:{i * 0.25:.2f}s"><g transform="translate({x0} {y0})">']
        g.append(f'<rect width="{cw_}" height="{ch}" rx="22" fill="url(#cardbg)" stroke="{LINE}" stroke-width="2"/>')
        g.append(
            f'<rect x="1" y="1" width="{cw_ - 2}" height="{ch - 2}" rx="21" fill="none" stroke="url(#acc)" stroke-width="3" pathLength="1000" stroke-dasharray="130 870" stroke-linecap="round" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" values="0;-1000" dur="{7 + i}s" repeatCount="indefinite"/></rect>'
        )
        g.append(f'<text x="{cw_ - 34}" y="86" text-anchor="end" fill="#13304f" font-family="{MONO}" font-size="78" font-weight="800">{i + 1:02d}</text>')
        sw = len(p.get("status", "")) * 9 + 46
        if p.get("status"):
            g.append(
                f'<rect x="36" y="32" width="{sw:.0f}" height="30" rx="15" fill="{GREEN}" fill-opacity=".1" stroke="{GREEN}" stroke-opacity=".5"/>'
                f'<circle cx="54" cy="47" r="4.5" fill="{GREEN}"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>'
                f'<text x="68" y="52" fill="{GREEN}" font-family="{MONO}" font-size="14" font-weight="700">{esc(p["status"])}</text>'
            )
        g.append(f'<text x="36" y="108" fill="{TEXT}" font-family="{SANS}" font-size="{nfs}" font-weight="800">{esc(nm)}</text>')
        for j, line in enumerate(desc):
            g.append(f'<text x="36" y="{146 + j * 27}" fill="{MUTED}" font-family="{SANS}" font-size="17">{esc(line)}</text>')
        ty = 146 + 27 * len(desc) + 26
        for t, px, prow, w in pos:
            col = TECH_COLORS.get(t, CYAN)
            g.append(
                f'<g transform="translate({36 + px:.0f} {ty + prow * 44})"><rect width="{w:.0f}" height="32" rx="10" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55"/>'
                f'<text x="{w / 2:.0f}" y="21" text-anchor="middle" fill="{TEXT}" font-family="{MONO}" font-size="15" font-weight="600">{esc(t)}</text></g>'
            )
        g.append("</g></g>")
        b.append("".join(g))
    write("assets/projects.svg", svg(W, H, "\n".join(b), defs, css, "Featured projects: " + ", ".join(p["name"] for p in prs)))
    return True


# ---------------------------------------------------------------- terminal
def build_terminal():
    items = P["console"]
    W, lh = 1000, 36
    head, pad = 54, 30
    H = head + pad + len(items) * lh * 2 + 24 + 30
    fs, cw = 21, 12.6
    T = len(items) * 3.4 + 3.5
    defs = ""
    b = [
        f'<rect width="{W}" height="{H}" rx="20" fill="#06101d"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="19" fill="none" stroke="{LINE}" stroke-width="2"/>',
        f'<path d="M1 {head}H{W - 1}" stroke="{LINE}"/>',
        f'<circle cx="34" cy="27" r="7" fill="#ff5f57"/><circle cx="60" cy="27" r="7" fill="#febc2e"/><circle cx="86" cy="27" r="7" fill="#28c840"/>',
        f'<text x="{W / 2}" y="33" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="15">{esc(P["github"])} -- developer_console</text>',
    ]
    y = head + pad + 14
    for i, it in enumerate(items):
        ts = 0.5 + i * 3.4
        cmd = it["cmd"]
        typed = len(cmd) * 0.07
        te = ts + typed
        tr = T - 0.6
        wpx = len(cmd) * cw
        x0 = 72
        defs += f'<clipPath id="k{i}"><rect x="{x0}" y="{y - 24}" width="0" height="34">{timeline("width", 0, wpx, ts, te, tr, T)}</rect></clipPath>'
        b.append(f'<g opacity="0">{pop(ts, tr, T, 0.05)}<text x="32" y="{y}" fill="{GREEN}" font-family="{MONO}" font-size="{fs}" font-weight="700">$</text></g>')
        b.append(f'<text x="{x0}" y="{y}" textLength="{wpx:.0f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#k{i})" fill="{TEXT}" font-family="{MONO}" font-size="{fs}">{esc(cmd)}</text>')
        b.append(
            f'<g opacity="0">{pop(te + 0.25, tr, T, 0.4)}<text x="32" y="{y + lh}" fill="{CYAN}" font-family="{MONO}" font-size="{fs}">{esc(it["out"])}</text></g>'
        )
        y += lh * 2
    b.append(
        f'<g><text x="32" y="{y}" fill="{GREEN}" font-family="{MONO}" font-size="{fs}" font-weight="700">$</text>'
        f'<rect x="58" y="{y - 20}" width="11" height="24" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect></g>'
    )
    write("assets/terminal.svg", svg(W, H, "\n".join(b), defs, "", "Developer console"))


# ---------------------------------------------------------- section header
def build_header(slug, num, title, label):
    W, H = 1200, 76
    defs = f"""
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-20%" y="-300%" width="140%" height="700%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""
    css = ".in{opacity:0;animation:in .8s cubic-bezier(.2,.8,.2,1) forwards}@keyframes in{from{opacity:0;transform:translateX(-18px)}to{opacity:1;transform:none}}"
    body = f"""
<rect width="{W}" height="{H}" rx="18" fill="{CARD}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="{LINE}" stroke-width="2"/>
<g class="in"><rect x="20" y="14" width="64" height="40" rx="12" fill="#0b1c33" stroke="url(#acc)" stroke-width="2"/>
<text x="52" y="42" text-anchor="middle" fill="{CYAN}" font-family="{MONO}" font-size="22" font-weight="800">{esc(num)}</text></g>
<g class="in" style="animation-delay:.15s"><text x="104" y="44" fill="{TEXT}" font-family="{SANS}" font-size="30" font-weight="800">{esc(title)}</text></g>
<text x="{W - 28}" y="41" text-anchor="end" fill="#4b6a8f" font-family="{MONO}" font-size="18">{esc(label)}</text>
<rect x="24" y="{H - 14}" width="{W - 48}" height="2" rx="1" fill="{LINE}"/>
<rect x="24" y="{H - 14.5}" width="240" height="3" rx="1.5" fill="url(#beam)" filter="url(#glow)"><animate attributeName="x" values="24;{W - 264};24" dur="5s" repeatCount="indefinite"/></rect>
"""
    write(f"assets/h-{slug}.svg", svg(W, H, body, defs, css, title))


# ------------------------------------------------------------------ footer
def build_footer():
    W, H = 1200, 220
    defs = f"""
<linearGradient id="w1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="bgf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06111f"/><stop offset="1" stop-color="#0b1020"/></linearGradient>
<clipPath id="fr"><rect width="{W}" height="{H}" rx="26"/></clipPath>
"""

    def wave(base, amp, k, phase):
        pts = []
        for x in range(0, 2 * W + 20, 20):
            y = base + amp * math.sin(2 * math.pi * k * x / W + phase)
            pts.append(f"{x},{y:.1f}")
        return "M" + " L".join(pts) + f" L{2 * W + 20},{H} L0,{H} Z"

    waves = ""
    for i, (base, amp, k, op, dur) in enumerate([(120, 16, 1, .28, 14), (136, 14, 1, .42, 10), (156, 11, 2, .85, 7)]):
        d = wave(base, amp, k, i * 1.7)
        waves += f'<path d="{d}" fill="url(#w1)" opacity="{op}"><animateTransform attributeName="transform" type="translate" values="0 0;-{W} 0" dur="{dur}s" repeatCount="indefinite"/></path>'
    body = f"""
<g clip-path="url(#fr)"><rect width="{W}" height="{H}" fill="url(#bgf)"/>
<text x="{W / 2}" y="62" text-anchor="middle" fill="{TEXT}" font-family="{SANS}" font-size="30" font-weight="800">Thanks for stopping by</text>
<text x="{W / 2}" y="96" text-anchor="middle" fill="{CYAN}" font-family="{MONO}" font-size="20">{esc(P["footer_text"])}</text>
{waves}</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="25" fill="none" stroke="{LINE}" stroke-width="2"/>
"""
    write("assets/footer.svg", svg(W, H, body, defs, "", "Footer"))


# ------------------------------------------------------------------ README
def build_readme():
    u = P["github"]
    L = P["links"]
    badges = " ".join(
        f'[![{esc(l["label"])}](https://img.shields.io/badge/{l["label"].replace(" ", "%20").replace("-", "--")}-{l["color"]}?style=for-the-badge'
        + (f'&logo={l["logo"]}&logoColor=white' if l.get("logo") else "")
        + f')]({l["url"]})'
        for l in L
    )
    facts = [
        ("Role", P["role"]),
        ("Company", f'[{P["company"]}]({P["company_url"]})'),
        ("Building", P["building"]),
        ("Location", P["location"]),
    ]
    facts_md = "\n".join(f"| **{k}** | {v} |" for k, v in facts)
    interests = "\n".join(f"- {i}" for i in P["interests"])
    has_portrait = os.path.exists(os.path.join(ASSETS, "portrait.svg"))
    about_cell = f"""{P["about"]}

| | |
|:--|:--|
{facts_md}

**Interests**

{interests}
"""
    if has_portrait:
        about = f"""<table>
<tr>
<td width="46%" valign="top">

<img src="assets/portrait.svg" alt="Dot-matrix portrait of {esc(P["name"])}" width="100%" />

</td>
<td valign="top">

{about_cell}
</td>
</tr>
</table>"""
    else:
        about = about_cell

    tech_text = "\n".join(f"- **{g['group']}:** {', '.join(g['items'])}" for g in P["tech"])
    focus = "\n".join(f"| **{f['area']}** | {f['text']} |" for f in P["focus"])
    h = lambda s, t: f'<img src="assets/h-{s}.svg" alt="{esc(t)}" width="100%" />'

    md = f"""<!-- GENERATED by build.py from profile.json - edit profile.json, then run: python build.py -->
<div align="center">

<img src="assets/hero.svg" width="100%" alt="{esc(P["name"])} - {esc(P["role"])} at {esc(P["company"])} - Building {esc(P["building"])}" />

{badges}

</div>

<br/>

{h("about", "About me")}

{about}

<br/>

{h("tech", "Tech stack")}

<div align="center">
<img src="assets/tech-stack.svg" width="100%" alt="Technology stack" />
</div>

<details>
<summary><b>Text version of the tech stack</b></summary>

{tech_text}

</details>

<br/>

{h("focus", "Current focus")}

| Area | What I'm focused on |
|:--|:--|
{focus}

<br/>

{h("projects", "Featured projects")}

<img src="assets/projects.svg" width="100%" alt="Featured projects" />

<br/>

{h("activity", "GitHub activity")}

<div align="center">

<img height="170" src="https://github-readme-stats.vercel.app/api?username={u}&show_icons=true&theme=tokyonight&hide_border=true&border_radius=12" alt="GitHub stats" />
<img height="170" src="https://streak-stats.demolab.com/?user={u}&theme=tokyonight&hide_border=true&border_radius=12" alt="GitHub streak" />

<img src="https://github-readme-activity-graph.vercel.app/graph?username={u}&theme=tokyo-night&hide_border=true&radius=12" width="100%" alt="GitHub activity graph" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{u}/{u}/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{u}/{u}/output/github-snake.svg" />
  <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/{u}/{u}/output/github-snake-dark.svg" width="100%" />
</picture>

</div>

> Stats cards are third-party services reading the public activity of **@{u}**; the snake needs the workflow in `.github/workflows/snake.yml` to run once.

<br/>

{h("console", "Developer console")}

<div align="center">
<img src="assets/terminal.svg" width="100%" alt="Developer console" />
</div>

<br/>

{h("connect", "Connect with me")}

<div align="center">

{badges}

<br/><br/>

<img src="https://komarev.com/ghpvc/?username={u}&label=Profile%20Views&color=8B5CF6&style=for-the-badge" alt="Profile views" />

</div>

<br/>

<img src="assets/footer.svg" width="100%" alt="Thanks for stopping by" />
"""
    write("README.md", md)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    build_hero()
    build_portrait()
    build_tech()
    build_projects()
    build_terminal()
    for slug, num, title, label in [
        ("about", "01", "About me", "about_me"),
        ("tech", "02", "Tech stack", "programming_languages_and_technologies"),
        ("focus", "03", "Current focus", "current_focus"),
        ("projects", "04", "Featured projects", "featured_projects"),
        ("activity", "05", "GitHub activity", "github_activity"),
        ("console", "06", "Developer console", "developer_console"),
        ("connect", "07", "Connect with me", "connect_with_me"),
    ]:
        build_header(slug, num, title, label)
    build_footer()
    build_readme()
    print("Built README.md and assets/*.svg from profile.json")


if __name__ == "__main__":
    main()
