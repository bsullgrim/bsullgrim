"""Small SVG helpers with real text measurement (Inter) so labels wrap and fit."""
from PIL import ImageFont
from xml.sax.saxutils import escape

FONT_DIR = "/usr/share/fonts/opentype/inter/"
FAMILY = "Inter, 'Helvetica Neue', Arial, sans-serif"
MONO_FAMILY = "'DejaVu Sans Mono', Menlo, Consolas, monospace"

import os as _os
THEME = _os.environ.get("THEME", "dark")

if THEME == "light":
    PAPER = "#ffffff"; NAVY = "#1f3864"; EMPH = "#1f3864"
    NAVY_T1 = "#e8edf6"; NAVY_T2 = "#cdd8ea"; NAVY_T3 = "#9fb3d4"
    INK = "#1d2433"; MUTED = "#5b6475"; LINE = "#8a93a3"; FILL = "#f4f6fa"; STROKE = "#c3cbd8"
    AMBER = "#a3550f"; AMBER_T = "#fbefe3"; TEAL = "#1f6f78"; TEAL_T = "#e6f2f3"
    BADGE_TEXT = "#ffffff"; TRACK = "#e6e9ef"; CONTAINER = "#fafbfd"
    CHART_BG = "#fcfcfb"; GRID = "#e6e8ec"; AXIS = "#9aa1ad"; BAR = "#2a78d6"; ON_EMPH = "#dfe6f2"
else:  # matches the Minimal Mistakes dark skin (#252a34 background)
    PAPER = "#252a34"; NAVY = "#8db0ea"; EMPH = "#2d4a7a"
    NAVY_T1 = "#2c3850"; NAVY_T2 = "#34456a"; NAVY_T3 = "#55709f"
    INK = "#eaeaea"; MUTED = "#a9b1bf"; LINE = "#808a9c"; FILL = "#2f3542"; STROKE = "#4a5366"
    AMBER = "#e6a865"; AMBER_T = "#43372a"; TEAL = "#4cc6cd"; TEAL_T = "#1f3c41"
    BADGE_TEXT = "#252a34"; TRACK = "#3a4150"; CONTAINER = "#2a303b"
    CHART_BG = "#252a34"; GRID = "#363d4a"; AXIS = "#808a9c"; BAR = "#3987e5"; ON_EMPH = "#dfe6f2"
WHITE = "#ffffff"

_fonts = {}


def font(size, weight="regular", italic=False, mono=False):
    if mono:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono" + ("-Bold" if weight == "bold" else "") + ".ttf"
    else:
        name = {"regular": "Regular", "medium": "Medium", "semibold": "SemiBold", "bold": "Bold"}[weight]
        if italic:
            name = "Italic" if name == "Regular" else name + "Italic"
        path = FONT_DIR + "Inter-" + name + ".otf"
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def width(text, size, weight="regular", italic=False, mono=False):
    return font(size, weight, italic, mono).getlength(text)


def wrap(text, size, maxw, weight="regular", italic=False, mono=False):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if width(trial, size, weight, italic, mono) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for ln in lines:
        if width(ln, size, weight, italic, mono) > maxw:
            raise ValueError(f"word too wide for {maxw}px: {ln!r} @ {size}px")
    return lines


W_ATTR = {"regular": "400", "medium": "500", "semibold": "600", "bold": "700"}


class SVG:
    def __init__(self, w, h, bg=None):
        bg = bg or PAPER
        self.w, self.h, self.parts = w, h, []
        self.parts.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>')

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill=FILL, stroke=STROKE, sw=2, rx=14, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def ellipse(self, cx, cy, rx, ry, fill=FILL, stroke=STROKE, sw=2):
        self.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size, fill=INK, weight="regular", anchor="start", italic=False, mono=False, rotate=None):
        fam = MONO_FAMILY if mono else FAMILY
        it = ' font-style="italic"' if italic else ""
        rot = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{W_ATTR[weight]}" '
                 f'fill="{fill}" text-anchor="{anchor}"{it}{rot}>{escape(s)}</text>')

    def lines(self, x, y, lines, size, lh=None, **kw):
        lh = lh or round(size * 1.28)
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size, **kw)
        return y + (len(lines) - 1) * lh

    def block(self, x, y, w, h, title=None, sub=None, tsize=32, ssize=24, fill=FILL, stroke=STROKE,
              tcolor=INK, scolor=MUTED, sw=2, rx=14, dash=None, align="middle", pad=22, tweight="bold",
              tmono=False, stereo=None, stereo_size=None, titalic=False, valign="middle"):
        """Box with an optional «stereotype», a bold title and a wrapped subtitle, centred vertically."""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, rx=rx, dash=dash)
        maxw = w - 2 * pad
        rows = []  # (lines, size, kwargs, lh)
        if stereo:
            ss = stereo_size or round(ssize * 0.9)
            rows.append(([stereo], ss, dict(fill=scolor, italic=False), round(ss * 1.25)))
        if title:
            tl = wrap(title, tsize, maxw, weight=tweight, mono=tmono, italic=titalic)
            rows.append((tl, tsize, dict(fill=tcolor, weight=tweight, mono=tmono, italic=titalic), round(tsize * 1.18)))
        if sub:
            sl = wrap(sub, ssize, maxw)
            rows.append((sl, ssize, dict(fill=scolor), round(ssize * 1.3)))
        gap = round(ssize * 0.45)
        total = sum(len(r[0]) * r[3] for r in rows) + gap * (len(rows) - 1)
        if valign == "middle":
            cy = y + (h - total) / 2
        else:
            cy = y + pad
        if align == "middle":
            tx, anchor = x + w / 2, "middle"
        else:
            tx, anchor = x + pad, "start"
        for lines_, size, kw, lh in rows:
            # baseline of first line ~ top + 0.8*size within its line box
            base = cy + lh * 0.5 + size * 0.35
            self.lines(tx, base, lines_, size, lh=lh, anchor=anchor, **kw)
            cy += len(lines_) * lh + gap
        return total

    def defs(self):
        return f'''<defs>
  <marker id="arr" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
    <path d="M1,1 L11,6 L1,11 z" fill="context-stroke"/></marker>
  <marker id="arrN" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
    <path d="M1,1 L11,6 L1,11 z" fill="{NAVY}"/></marker>
  <marker id="arrG" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="15" markerHeight="15" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
    <path d="M1,1 L11,6 L1,11 z" fill="{LINE}"/></marker>
  <marker id="arrT" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
    <path d="M1,1 L11,6 L1,11 z" fill="{TEAL}"/></marker>
  <marker id="open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="22" markerHeight="22" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M2,2 L14,8 L2,14" fill="none" stroke="{INK}" stroke-width="2"/></marker>
  <marker id="tri" viewBox="0 0 20 20" refX="18" refY="10" markerWidth="30" markerHeight="30" markerUnits="userSpaceOnUse" orient="auto">
    <path d="M2,2 L18,10 L2,18 z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/></marker>
</defs>'''

    def line(self, pts, color=LINE, sw=3, dash=None, marker=None, marker_start=None):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{marker})"' if marker else ""
        ms = f' marker-start="url(#{marker_start})"' if marker_start else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"{da}{me}{ms}/>')

    def badge(self, cx, cy, n, r=19, fill=AMBER):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
        self.text(cx, cy + 8, str(n), 22, fill=BADGE_TEXT, weight="bold", anchor="middle")

    def cylinder(self, x, y, w, h, title, sub=None, fill=FILL, stroke=STROKE, tsize=24, ssize=20):
        e = 14
        self.add(f'<path d="M{x},{y+e} L{x},{y+h-e} A{w/2},{e} 0 0 0 {x+w},{y+h-e} L{x+w},{y+e}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        self.add(f'<ellipse cx="{x+w/2}" cy="{y+e}" rx="{w/2}" ry="{e}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        tl = wrap(title, tsize, w - 24, weight="semibold")
        sl = wrap(sub, ssize, w - 24) if sub else []
        lh_t, lh_s = round(tsize * 1.2), round(ssize * 1.25)
        total = len(tl) * lh_t + len(sl) * lh_s
        cy = y + e + (h - e - total) / 2 + tsize * 0.85
        self.lines(x + w / 2, cy, tl, tsize, lh=lh_t, anchor="middle", weight="semibold")
        if sl:
            self.lines(x + w / 2, cy + len(tl) * lh_t, sl, ssize, lh=lh_s, anchor="middle", fill=MUTED)

    def svg(self):
        body = "\n".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">\n{self.defs()}\n{body}\n</svg>\n')
