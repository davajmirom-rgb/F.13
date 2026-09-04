import customtkinter as cck
from tkinter import ttk, messagebox
from datetime import datetime
from animations import animate_number
from settings import SettingsWindow

class BudgetView(cck.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.pack(fill="both", expand=True)

        self.cur_bal = 0.0
        self.cur_inc = 0.0
        self.cur_exp = 0.0

        self._build_ui()

    def _build_ui(self):
        # Левая колонка ввода
        self.left_panel = cck.CTkFrame(self, width=310, corner_radius=12)
        self.left_panel.pack(side="left", fill="y", padx=(6, 12), pady=6)
        self.left_panel.pack_propagate(False)

        cck.CTkLabel(self.left_panel, text="💳 Добавить запись", font=cck.CTkFont(size=17, weight="bold")).pack(pady=(14, 8))

        self.type_var = cck.StringVar(value="Расход")
        cck.CTkSegmentedButton(self.left_panel, values=["Расход", "Доход"], variable=self.type_var).pack(padx=16, pady=(0, 10), fill="x")

        cck.CTkLabel(self.left_panel, text="Сумма операции:", font=cck.CTkFont(size=12)).pack(padx=16, anchor="w")
        self.amt_in = cck.CTkEntry(self.left_panel, placeholder_text="0.00", height=35)
        self.amt_in.pack(padx=16, pady=(2, 8), fill="x")

        cat_top = cck.CTkFrame(self.left_panel, fg_color="transparent")
        cat_top.pack(fill="x", padx=16, pady=(2, 0))
        cck.CTkLabel(cat_top, text="Категория:", font=cck.CTkFont(size=12)).pack(side="left")

        cat_row = cck.CTkFrame(self.left_panel, fg_color="transparent")
        cat_row.pack(fill="x", padx=16, pady=(2, 8))
        self.cat_in = cck.CTkComboBox(cat_row, values=self.app.categories, height=35)
        self.cat_in.pack(side="left", fill="x", expand=True, padx=(0, 4))
        cck.CTkButton(cat_row, text="+", width=34, height=35, command=self.add_custom_cat).pack(side="left", padx=2)
        cck.CTkButton(cat_row, text="✕", width=34, height=35, fg_color="#7B241C", hover_color="#641E16", command=self.del_custom_cat).pack(side="left", padx=2)

        cck.CTkLabel(self.left_panel, text="Описание:", font=cck.CTkFont(size=12)).pack(padx=16, anchor="w")
        self.desc_in = cck.CTkEntry(self.left_panel, placeholder_text="Краткая заметка", height=35)
        self.desc_in.pack(padx=16, pady=(2, 14), fill="x")

        cck.CTkButton(self.left_panel, text="✨ Внести запись", command=self.add_tx,
                       fg_color="#2563EB", hover_color="#1D4ED8", height=38, font=cck.CTkFont(weight="bold")).pack(padx=16, pady=(0, 8), fill="x")

        cck.CTkButton(self.left_panel, text="⚙️ Параметры и шрифты", command=lambda: SettingsWindow(self.app, self.app.theme_manager),
                       fg_color="gray25", hover_color="gray35", height=34).pack(side="bottom", padx=16, pady=16, fill="x")

        # Правая колонка
        self.right_panel = cck.CTkFrame(self, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(0, 6), pady=6)

        cards = cck.CTkFrame(self.right_panel, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 8))

        self.card_bal = cck.CTkFrame(cards, corner_radius=10)
        self.card_bal.pack(side="left", fill="both", expand=True, padx=(0, 5))
        cck.CTkLabel(self.card_bal, text="БАЛАНС", font=cck.CTkFont(size=10, weight="bold"), text_color="gray60").pack(pady=(8, 0))
        self.lbl_bal = cck.CTkLabel(self.card_bal, text="0.00", font=cck.CTkFont(size=19, weight="bold"), text_color="#38BDF8")
        self.lbl_bal.pack(pady=(0, 8))

        self.card_inc = cck.CTkFrame(cards, corner_radius=10)
        self.card_inc.pack(side="left", fill="both", expand=True, padx=5)
        cck.CTkLabel(self.card_inc, text="ДОХОДЫ", font=cck.CTkFont(size=10, weight="bold"), text_color="gray60").pack(pady=(8, 0))
        self.lbl_inc = cck.CTkLabel(self.card_inc, text="+0.00", font=cck.CTkFont(size=19, weight="bold"), text_color="#4ADE80")
        self.lbl_inc.pack(pady=(0, 8))

        self.card_exp = cck.CTkFrame(cards, corner_radius=10)
        self.card_exp.pack(side="left", fill="both", expand=True, padx=(5, 0))
        cck.CTkLabel(self.card_exp, text="РАСХОДЫ", font=cck.CTkFont(size=10, weight="bold"), text_color="gray60").pack(pady=(8, 0))
        self.lbl_exp = cck.CTkLabel(self.card_exp, text="-0.00", font=cck.CTkFont(size=19, weight="bold"), text_color="#F87171")
        self.lbl_exp.pack(pady=(0, 8))

        p_box = cck.CTkFrame(self.right_panel, corner_radius=8, height=26)
        p_box.pack(fill="x", pady=(0, 8))
        p_box.pack_propagate(False)

        self.lbl_ratio = cck.CTkLabel(p_box, text="Нагрузка расходов: 0%", font=cck.CTkFont(size=11))
        self.lbl_ratio.pack(side="left", padx=12)
        self.prog_bar = cck.CTkProgressBar(p_box, width=150, height=7, progress_color="#F87171")
        self.prog_bar.pack(side="right", padx=12, pady=9)
        self.prog_bar.set(0)

        # Контейнер таблицы с темным скроллбаром CustomTkinter (без белых артефактов)
        tbl_box = cck.CTkFrame(self.right_panel, corner_radius=10)
        tbl_box.pack(fill="both", expand=True)

        cols = ("date", "type", "cat", "amount", "desc")
        self.tree = ttk.Treeview(tbl_box, columns=cols, show="headings", selectmode="browse")
        for c, h, w in [("date", "Дата", 95), ("type", "Тип", 75), ("cat", "Категория", 110), ("amount", "Сумма", 100), ("desc", "Описание", 180)]:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center" if c in ("date", "type") else "w")

        # Тёмный скроллбар CustomTkinter
        scroll = cck.CTkScrollbar(tbl_box, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(4, 0), pady=4)
        scroll.pack(side="right", fill="y", padx=(2, 4), pady=4)

        cck.CTkButton(self.right_panel, text="🗑️ Удалить запись", fg_color="#991B1B", hover_color="#7F1D1D",
                       command=self.del_tx, height=30).pack(fill="x", pady=(6, 0))

    def update_table(self, animate=True):
        for r in self.tree.get_children():
            self.tree.delete(r)

        inc, exp = 0.0, 0.0
        sym = self.app.currency_symbol

        for t in self.app.transactions:
            sign = "+" if t["type"] == "Доход" else "-"
            self.tree.insert("", "end", values=(t["date"], t["type"], t["cat"], f"{sign}{t['amount']:,.2f} {sym}", t["desc"]))
            if t["type"] == "Доход":
                inc += t["amount"]
            else:
                exp += t["amount"]

        bal = inc - exp

        if animate and self.app.animations_enabled:
            animate_number(self, self.lbl_bal, self.cur_bal, bal, suffix=f" {sym}")
            animate_number(self, self.lbl_inc, self.cur_inc, inc, prefix="+", suffix=f" {sym}")
            animate_number(self, self.lbl_exp, self.cur_exp, exp, prefix="-", suffix=f" {sym}")
        else:
            self.lbl_bal.configure(text=f"{bal:,.2f} {sym}")
            self.lbl_inc.configure(text=f"+{inc:,.2f} {sym}")
            self.lbl_exp.configure(text=f"-{exp:,.2f} {sym}")

        self.cur_bal, self.cur_inc, self.cur_exp = bal, inc, exp
        ratio = (exp / inc) if inc > 0 else (1.0 if exp > 0 else 0.0)
        self.prog_bar.set(min(ratio, 1.0))
        self.lbl_ratio.configure(text=f"Нагрузка расходов: {ratio * 100:.1f}%")

    def add_tx(self):
        try:
            val = float(self.amt_in.get().strip().replace(",", "."))
            if val <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Введите положительное число!")
            return

        self.app.transactions.insert(0, {
            "date": datetime.now().strftime("%d.%m %H:%M"),
            "type": self.type_var.get(),
            "cat": self.cat_in.get() or "Другое",
            "amount": val,
            "desc": self.desc_in.get().strip() or "-"
        })
        self.app.save_all()
        self.update_table(animate=True)
        self.amt_in.delete(0, "end")
        self.desc_in.delete(0, "end")

    def del_tx(self):
        sel = self.tree.selection()
        if not sel: return
        del self.app.transactions[self.tree.index(sel)]
        self.app.save_all()
        self.update_table(animate=True)

    def add_custom_cat(self):
        dialog = cck.CTkInputDialog(text="Название новой категории:", title="Категория")
        val = dialog.get_input()
        if val:
            val = val.strip()
            if val and val not in self.app.categories:
                self.app.categories.append(val)
                self.cat_in.configure(values=self.app.categories)
                self.cat_in.set(val)
                self.app.save_all()

    def del_custom_cat(self):
        curr = self.cat_in.get()
        if curr in ["Зарплата", "Другое"]:
            messagebox.showwarning("Внимание", "Базовые категории удалить нельзя.")
            return
        if curr in self.app.categories:
            self.app.categories.remove(curr)
            self.cat_in.configure(values=self.app.categories)
            self.cat_in.set(self.app.categories if self.app.categories else "Другое")
            self.app.save_all()
