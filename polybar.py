"""Matching polybar colours, built from the same art as everything else.

The bar is styled as the theme's e16 title bar: its gradient (sampled from the
rendered header art), the accent stripe along the bottom edge, the title text
colour and font, and a glyph standing in for the emblem (polybar can't show
images).  The shared layout lives in polybar/config.ini, which includes
~/.config/polybar/theme.ini - a symlink to one of these files.

Output: <out_dir>/polybar/<Name>.ini
"""

from pathlib import Path

from gtk import mix, pixel, readable

GLYPHS = dict(
    Umbreon="☾", Koraidon="✹", Miraidon="⚡", Armarouge="✦", Sylveon="♡", Red="◓",
    Mimikyu="∿", Gastly="☁", Kalos="❖", Alola="☀", Lunala="☽", Rayquaza="✶",
    Lucario="◉", Pikachu="ϟ", Darkrai="◐", Paldea="✿", Cyndaquil="✺", Academy="◆",
    Eon="▲", Mewtwo="◍", Giratina="♛", Zoroark="❂", Greninja="✣", Galar="⚔",
)


def _font(pango, size):
    """'pango:DejaVu Serif Condensed Bold 9' -> 'DejaVu Serif Condensed:style=Bold:size=10'"""
    words = pango.removeprefix("pango:").split()[:-1]
    styles = {"thin", "light", "regular", "medium", "semibold", "bold", "extrabold", "black", "heavy", "italic"}
    fam = [w for w in words if w.lower() not in styles]
    sty = [w for w in words if w.lower() in styles]
    return f"{' '.join(fam)}:style={' '.join(sty) or 'Regular'}:size={size}"


def build(art, out_dir, pal):
    """pal: the dict gtk.build() returned.  Returns the .ini path."""
    a, T = art, art.TEXT
    hdr = pal["assets"] / "header-bg.png"          # 16 x 34: the title bar, scaled to header height
    top = pixel(hdr, 8, 6, pal["bg"])
    mid = pixel(hdr, 8, 14, pal["bg"])
    bot = pixel(hdr, 8, 24, pal["bg"])
    stripe = pixel(hdr, 8, 30, pal["bg"])           # the band along the bottom of the title bar
    fg = readable(mid, [T["title_active"], T["title_inactive"], "#ffffff", "#111111"])
    dim = mix(fg, mid, 0.4)
    accent = pal["accent"]
    if abs(sum(int(accent[i:i + 2], 16) for i in (1, 3, 5)) - sum(int(mid[i:i + 2], 16) for i in (1, 3, 5))) < 120:
        accent = readable(mid, [pal["link"], stripe, fg])   # accent too close to the bar: use something that shows

    text = f"""; {a.NAME} - polybar colours generated alongside the e16 theme (see polybar.py)

[theme]
name = {a.NAME}
glyph = {GLYPHS.get(a.NAME, "●")}
font-text = {_font(a.FONTS["menu"], 10)};2
font-title = {_font(a.FONTS["border"], 10)};2

[colors]
bg-top = {top}
bg-mid = {mid}
bg-bottom = {bot}
stripe = {stripe}
fg = {fg}
dim = {dim}
accent = {accent}
urgent = #e5484d
warn = #e5a50a
"""
    path = Path(out_dir) / "polybar" / f"{a.NAME}.ini"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path
