# -*- coding: utf-8 -*-
"""Generate the SVG artwork used by the Runia0 GitHub profile README.

Usage: python3 tools/gen.py /path/to/runia0-site/tools
(the second path gives access to the site's cover illustrations)
"""
import os
import sys
from html import escape as e

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "..", "repo", "runia0-site", "tools"))
from covers import BUILDERS  # noqa: E402

FONT = "system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BG, LINE, TEXT, MUTED, ACC = "#050807", "#1a3326", "#e8f2ec", "#a3b8ab", "#39ff88"

LOGO = ('<rect width="64" height="64" rx="14" fill="#0b1f14"/>'
        '<path d="M17 46V18h13a8 8 0 010 16H17m12 0l9 12" fill="none" stroke="#e8f2ec" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="45" cy="38" r="7" fill="none" stroke="#39ff88" stroke-width="4"/>')


def banner():
    W, H = 1280, 360
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W + 1, 40))
    grid += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H + 1, 40))
    lines = [
        ("$", "runia0 status", TEXT),
        ("●", "frogier           playable", ACC),
        ("●", "shadow-protocol   playable", ACC),
        ("●", "sokaklarin-kanunu playable", ACC),
        ("●", "night-shift       playable", ACC),
        ("●", "iplik             pre-release", "#ffd27a"),
    ]
    term = "".join(
        f'<text y="{i*30}" class="m"><tspan x="0" fill="{c}">{e(a)}</tspan><tspan x="22" fill="{TEXT if i == 0 else MUTED}">{e(b if i == 0 else b.split()[0])}</tspan>'
        + (f'<tspan x="210" fill="{c}">{e(b.split()[1])}</tspan>' if i else "") + "</text>"
        for i, (a, b, c) in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Runia0 — Ideas into things that work.">
<style>
.s{{font-family:{FONT}}} .m{{font-family:{MONO};font-size:17px}}
.cur{{animation:b 1.1s steps(1) infinite}} @keyframes b{{50%{{opacity:0}}}}
.scan{{animation:sc 6s linear infinite}} @keyframes sc{{from{{transform:translateY(-60px)}}to{{transform:translateY({H}px)}}}}
.glow{{animation:g 4s ease-in-out infinite alternate}} @keyframes g{{from{{opacity:.35}}to{{opacity:.7}}}}
@media (prefers-reduced-motion:reduce){{.cur,.scan,.glow{{animation:none}}}}
</style>
<defs>
<radialGradient id="rg" cx=".82" cy="0" r=".7"><stop offset="0" stop-color="#1f6b43"/><stop offset="1" stop-color="#1f6b43" stop-opacity="0"/></radialGradient>
<linearGradient id="sl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset="1" stop-color="{ACC}" stop-opacity=".08"/></linearGradient>
<clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#rg)" class="glow"/>
<g stroke="#0f2219" stroke-width="1">{grid}</g>
<rect class="scan" width="{W}" height="60" fill="url(#sl)"/>
<g transform="translate(64 62)"><svg width="56" height="56" viewBox="0 0 64 64">{LOGO}</svg>
<text x="74" y="40" class="s" font-size="34" font-weight="700" fill="{TEXT}">Runia0</text></g>
<text x="64" y="196" class="s" font-size="58" font-weight="750" fill="{TEXT}" letter-spacing="-1">Ideas into things that <tspan fill="{ACC}">work.</tspan></text>
<text x="66" y="240" class="m" fill="{MUTED}">Independent by nature. Built through code.</text>
<text x="66" y="300" class="s" font-size="17" fill="{MUTED}" letter-spacing="2">SOFTWARE  ·  ARTIFICIAL INTELLIGENCE  ·  GAMES  ·  DIGITAL PRODUCTS</text>
<g transform="translate(880 66)">
<rect x="-24" y="-38" width="364" height="262" rx="12" fill="#07100b" stroke="{LINE}"/>
<circle cx="-6" cy="-20" r="5" fill="{LINE}"/><circle cx="10" cy="-20" r="5" fill="{LINE}"/><circle cx="26" cy="-20" r="5" fill="{LINE}"/>
<g transform="translate(0 20)">{term}<text x="0" y="180" class="m" fill="{ACC}">$ <tspan class="cur">▍</tspan></text></g>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>
</g>
</svg>
'''


SHOTS = os.environ.get("SHOTS", "")


def card(pid, key, title, desc, status, color, tags):
    W, H = 640, 420
    shot = os.path.join(SHOTS, pid + ".jpg") if SHOTS else ""
    if shot and os.path.exists(shot):
        import base64, io
        from PIL import Image
        im = Image.open(shot).convert("RGB").resize((800, 450))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=78, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        inner = f'<image href="data:image/jpeg;base64,{b64}" x="0" y="0" width="640" height="360" preserveAspectRatio="xMidYMid slice"/>'
    else:
        inner = BUILDERS[key]().replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg', 1)
        inner = inner.replace('width="1200" height="675"', 'x="0" y="0" width="640" height="360" preserveAspectRatio="xMidYMid slice"', 1)
    tag_svg, x = "", 28
    for t in tags:
        w = 14 + len(t) * 9
        tag_svg += f'<rect x="{x}" y="372" width="{w}" height="26" rx="6" fill="#0b1611" stroke="{LINE}"/><text x="{x+7}" y="390" class="m" font-size="14" fill="{MUTED}">{e(t)}</text>'
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{e(title)} — {e(desc)}">
<style>.s{{font-family:{FONT}}} .m{{font-family:{MONO}}}</style>
<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".3" stop-color="{BG}" stop-opacity="0"/><stop offset=".68" stop-color="{BG}" stop-opacity=".92"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="{BG}"/>
{inner}
<rect width="{W}" height="360" fill="url(#fade)"/>
<rect x="28" y="24" width="{24 + len(status)*9}" height="28" rx="14" fill="{BG}" fill-opacity=".94" stroke="{color}"/>
<text x="40" y="43" class="m" font-size="14" fill="{color}">{e(status)}</text>
<text x="28" y="290" class="s" font-size="38" font-weight="750" fill="{TEXT}">{e(title)}</text>
<text x="28" y="328" class="s" font-size="18" fill="#cbdcd2">{e(desc)}</text>
{tag_svg}
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{LINE}"/>
</g>
</svg>
'''


def stack():
    items = ["Three.js", "JavaScript", "Python", "HTML/CSS", "Web Audio API", "Capacitor", "Android",
             "Firebase", "GitHub Actions", "Playwright", "SQLite", "Roblox · Luau"]
    W = 1280
    x, y, out = 0, 0, ""
    for t in items:
        w = 34 + len(t) * 10.5
        if x + w > W:
            x, y = 0, y + 52
        out += (f'<g transform="translate({x:.0f} {y})"><rect width="{w:.0f}" height="40" rx="10" fill="#0b1611" stroke="{LINE}"/>'
                f'<circle cx="17" cy="20" r="4" fill="{ACC}"/><text x="29" y="26" class="m" font-size="17" fill="{TEXT}">{e(t)}</text></g>')
        x += w + 10
    H = y + 40
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tech stack">'
            f'<style>.m{{font-family:{MONO}}}</style>{out}</svg>\n')


def divider():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 24" width="1280" height="24">'
            f'<line x1="0" y1="12" x2="1280" y2="12" stroke="{LINE}" stroke-width="2" stroke-dasharray="6 8"/>'
            f'<rect x="616" y="6" width="48" height="12" rx="6" fill="{ACC}"/></svg>\n')


CARDS = [
    ("frogie", "frogie", "Frogier", "3D action-platformer · 100 levels · bosses", "PLAY DEMO", ACC, ["Three.js", "Capacitor", "Android"]),
    ("shadow-protocol", "shadow", "Shadow Protocol", "Story-driven 3D sniper · 5 missions", "PLAY DEMO", ACC, ["Three.js", "Web Audio"]),
    ("sokaklarin-kanunu", "streets", "Sokakların Kanunu", "Original crime drama in Adana · 3 endings", "PLAY DEMO", ACC, ["Three.js", "Web Audio"]),
    ("iplik", "iplik", "İplik", "Turkish quotes & proverbs app · offline", "PRE-RELEASE", "#ffd27a", ["Capacitor", "Android"]),
    ("night-shift", "nightshift", "NIGHT SHIFT", "Gas station management + horror", "PLAY DEMO", ACC, ["Three.js"]),
    ("hicaz-studyosu", "hicaz", "Hicaz Studio", "One melody, eight Hicaz scales", "TRY IN BROWSER", ACC, ["Web Audio API"]),
]

if __name__ == "__main__":
    out = os.path.join(ROOT, "assets")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "banner.svg"), "w", encoding="utf-8").write(banner())
    open(os.path.join(out, "stack.svg"), "w", encoding="utf-8").write(stack())
    open(os.path.join(out, "divider.svg"), "w", encoding="utf-8").write(divider())
    for pid, key, *rest in CARDS:
        open(os.path.join(out, f"card-{pid}.svg"), "w", encoding="utf-8").write(card(pid, key, *rest))
    print("ok")
