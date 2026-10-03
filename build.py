#!/usr/bin/env python3
"""Build the e16 themes.

    ./build.py                 build every theme in themes/
    ./build.py umbreon         build just themes/umbreon.py
    ./build.py --install ...   also symlink the results into ~/.e16/themes
                               the rofi themes into ~/.local/share/rofi/themes
                               the GTK3 themes into ~/.themes
                               the KDE/Qt colour schemes into ~/.local/share/color-schemes
                               and copies the YouTube Music CSS into Pear Desktop's
                               (Flatpak) config dir, where its sandbox can read it
"""

import importlib
import shutil
import sys
from pathlib import Path

import gtk
import polybar
import qt
import rofi
import ytmusic
from base import ROOT, Art, Builder

E16_THEMES = Path.home() / ".e16" / "themes"
ROFI_THEMES = Path.home() / ".local" / "share" / "rofi" / "themes"
GTK_THEMES = Path.home() / ".themes"
QT_SCHEMES = Path.home() / ".local" / "share" / "color-schemes"
PEAR_THEMES = Path.home() / ".var/app/com.github.th_ch.youtube_music/config/YouTube Music/themes"


def theme_modules(names):
    if not names:
        names = sorted(p.stem for p in (ROOT / "themes").glob("*.py") if not p.stem.startswith("_"))
    for n in names:
        mod = importlib.import_module(f"themes.{n}")
        yield next(v for v in vars(mod).values()
                   if isinstance(v, type) and issubclass(v, Art) and v is not Art and v.__module__ == mod.__name__)


def install(link, target):
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        sys.exit(f"refusing to replace non-symlink {link}")
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target)
    print(f"  linked {link} -> {target}")


def main(argv):
    do_install = "--install" in argv
    names = [a for a in argv if not a.startswith("--")]
    for cls in theme_modules(names):
        art = cls()
        out = Builder(art).build()
        rasi = rofi.build(art, out)
        pal = gtk.build(art, out)
        colors = qt.build(art, out, pal)
        ytm = ytmusic.build(art, out, pal)
        bar = polybar.build(art, out, pal)
        print(f"built {cls.NAME}: {out} (+ {rasi.name}, gtk-3.0, {colors.name}, {ytm.name}, {bar.name})")
        if do_install:
            install(E16_THEMES / out.name, out)
            install(ROFI_THEMES / rasi.name, rasi)
            install(GTK_THEMES / out.name, out)
            install(QT_SCHEMES / colors.name, colors)
            if PEAR_THEMES.parent.exists():   # copied: a symlink out of the sandbox wouldn't resolve
                PEAR_THEMES.mkdir(exist_ok=True)
                shutil.copyfile(ytm, PEAR_THEMES / ytm.name)
                print(f"  copied {ytm.name} -> {PEAR_THEMES}")


if __name__ == "__main__":
    main(sys.argv[1:])
