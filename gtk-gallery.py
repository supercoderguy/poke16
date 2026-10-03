#!/usr/bin/env python3
"""A GTK3 widget gallery for screenshotting the themes (driven by preview-gtk.sh).

    gtk-gallery.py            main window + an unfocused "backdrop" window
    gtk-gallery.py --menu     ...and pop the File menu open after a moment
    gtk-gallery.py --backdrop ...and force the second window's unfocused state
"""

import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk  # noqa: E402


def controls():
    g = Gtk.Grid(column_spacing=12, row_spacing=10, margin=14)
    row = 0

    def add(label, *widgets):
        nonlocal row
        g.attach(Gtk.Label(label=label, xalign=0), 0, row, 1, 1)
        box = Gtk.Box(spacing=8)
        for w in widgets:
            box.pack_start(w, False, False, 0)
        g.attach(box, 1, row, 1, 1)
        row += 1

    sug = Gtk.Button(label="Suggested")
    sug.get_style_context().add_class("suggested-action")
    tog = Gtk.ToggleButton(label="Toggled", active=True)
    dis = Gtk.Button(label="Disabled", sensitive=False)
    tip = Gtk.Button(label="Hover me", tooltip_text="A themed tooltip")
    add("Buttons", Gtk.Button(label="Button"), sug, tog, dis, tip)

    e1 = Gtk.Entry(text="Some text")
    e2 = Gtk.Entry(placeholder_text="Placeholder")
    spin = Gtk.SpinButton.new_with_range(0, 100, 1)
    spin.set_value(42)
    combo = Gtk.ComboBoxText()
    for t in ("Combo box", "Second", "Third"):
        combo.append_text(t)
    combo.set_active(0)
    add("Entries", e1, e2, spin, combo)

    c1 = Gtk.CheckButton(label="Checked", active=True)
    c2 = Gtk.CheckButton(label="Unchecked")
    r1 = Gtk.RadioButton(label="Radio on")
    r2 = Gtk.RadioButton(label="Radio off", group=r1)
    add("Choices", c1, c2, r1, r2)

    s1, s2 = Gtk.Switch(active=True), Gtk.Switch(active=False)
    add("Switches", s1, s2)

    scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
    scale.set_value(60)
    scale.set_size_request(220, -1)
    scale.set_draw_value(False)
    add("Slider", scale)

    prog = Gtk.ProgressBar(fraction=0.65)
    prog.set_size_request(220, -1)
    level = Gtk.LevelBar(value=0.4)
    level.set_size_request(120, -1)
    add("Progress", prog, level)
    return g


def file_list():
    store = Gtk.ListStore(str, str, str)
    for row in (("Documents", "Folder", "—"), ("Pictures", "Folder", "—"), ("notes.txt", "Text", "2 KB"),
                ("wallpaper.png", "Image", "4.1 MB"), ("theme.css", "Stylesheet", "18 KB"),
                ("music.ogg", "Audio", "6.3 MB"), ("archive.tar", "Archive", "120 MB")):
        store.append(row)
    tv = Gtk.TreeView(model=store)
    for i, title in enumerate(("Name", "Type", "Size")):
        tv.append_column(Gtk.TreeViewColumn(title, Gtk.CellRendererText(), text=i))
    tv.get_selection().select_path(Gtk.TreePath(2))
    sw = Gtk.ScrolledWindow(shadow_type=Gtk.ShadowType.IN, margin=14)
    sw.add(tv)
    return sw


def main():
    win = Gtk.Window(title="Widget gallery")
    hb = Gtk.HeaderBar(title="Widget gallery", subtitle="GTK3 theme preview", show_close_button=True)
    hb.pack_start(Gtk.Button.new_from_icon_name("document-open-symbolic", Gtk.IconSize.BUTTON))
    win.set_titlebar(hb)

    menubar = Gtk.MenuBar()
    file_item = Gtk.MenuItem(label="File")
    menu = Gtk.Menu()
    for label in ("New window", "Open…", "Save"):
        menu.append(Gtk.MenuItem(label=label))
    menu.append(Gtk.SeparatorMenuItem())
    menu.append(Gtk.CheckMenuItem(label="Show hidden files", active=True))
    sub = Gtk.MenuItem(label="Recent")
    sm = Gtk.Menu()
    sm.append(Gtk.MenuItem(label="wallpaper.png"))
    sub.set_submenu(sm)
    menu.append(sub)
    menu.append(Gtk.MenuItem(label="Disabled item", sensitive=False))
    menu.append(Gtk.MenuItem(label="Quit"))
    file_item.set_submenu(menu)
    menubar.append(file_item)
    for label in ("Edit", "View", "Help"):
        menubar.append(Gtk.MenuItem(label=label))

    nb = Gtk.Notebook()
    nb.append_page(controls(), Gtk.Label(label="Controls"))
    nb.append_page(file_list(), Gtk.Label(label="Files"))
    tv = Gtk.TextView(margin=14)
    tv.get_buffer().set_text("A text view.\nSelect some of this text to see the selection colour.")
    nb.append_page(tv, Gtk.Label(label="Text"))

    paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
    paned.pack1(nb, True, False)
    paned.pack2(file_list(), True, False)
    paned.set_position(560)

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    box.pack_start(menubar, False, False, 0)
    box.pack_start(paned, True, True, 0)
    win.add(box)
    win.set_default_size(900, 470)
    win.move(40, 40)
    win.connect("destroy", Gtk.main_quit)

    other = Gtk.Window(title="Backdrop")
    ohb = Gtk.HeaderBar(title="Unfocused window", show_close_button=True)
    other.set_titlebar(ohb)
    other.add(Gtk.Label(label="This window does not have focus.", margin=24))
    other.set_default_size(330, 120)
    other.move(900, 560)

    other.show_all()
    win.show_all()
    win.present()
    if "--backdrop" in sys.argv:
        # headless X gives GTK no focus changes, so force the unfocused look
        def backdrop(w):
            w.set_state_flags(Gtk.StateFlags.BACKDROP, False)
            if isinstance(w, Gtk.Container):
                w.forall(backdrop)
        # GTK recomputes the flag from the (absent) focus state after mapping,
        # so keep re-applying it
        GLib.timeout_add(300, lambda: backdrop(other) or True)

    if "--menu" in sys.argv:
        def pop():
            menubar.select_item(file_item)
            file_item.activate()
            return False
        GLib.timeout_add(1500, pop)
    Gtk.main()


if __name__ == "__main__":
    main()
