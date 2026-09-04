import customtkinter as cck
from tkinter import ttk

THEMES = {
    "dark": {
        "mode": "dark",
        "bg": "#242424",
        "card": "#2B2B2B",
        "tree_bg": "#2A2D32",
        "tree_fg": "#FFFFFF",
        "tree_head": "#1F2326",
        "select": "#1F538D"
    },
    "amoled": {
        "mode": "dark",
        "bg": "#000000",
        "card": "#121212",
        "tree_bg": "#0A0A0A",
        "tree_fg": "#FFFFFF",
        "tree_head": "#1A1A1A",
        "select": "#2A2A2A"
    },
    "dark_blue": {
        "mode": "dark",
        "bg": "#0A1628",
        "card": "#12233D",
        "tree_bg": "#0F1F35",
        "tree_fg": "#C8DCF0",
        "tree_head": "#1A2F4A",
        "select": "#1A3A5C"
    }
}

class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.current = "dark"

    def apply(self, name):
        if name not in THEMES:
            name = "dark"
        self.current = name
        cfg = THEMES[name]

        cck.set_appearance_mode(cfg["mode"])
        if hasattr(self.app, "configure"):
            self.app.configure(fg_color=cfg["bg"])
        if hasattr(self.app, "left_panel") and self.app.left_panel:
            self.app.left_panel.configure(fg_color=cfg["card"])

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=cfg["tree_bg"],
                        foreground=cfg["tree_fg"],
                        rowheight=26,
                        fieldbackground=cfg["tree_bg"],
                        borderwidth=0)
        style.map("Treeview", background=[("selected", cfg["select"])])
        style.configure("Treeview.Heading",
                        background=cfg["tree_head"],
                        foreground=cfg["tree_fg"],
                        relief="flat")
