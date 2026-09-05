# settings.py
import customtkinter as cck


class SettingsWindow(cck.CTkToplevel):
    def __init__(self, parent, theme_manager):
        super().__init__(parent)
        self.parent = parent
        self.tm = theme_manager

        self.title("Параметры приложения")
        self.geometry("420x680")
        self.minsize(380, 560)
        self.transient(parent)
        self.grab_set()

        # Кнопка закрытия зафиксирована внизу
        btn_close = cck.CTkButton(self, text="Готово", command=self.destroy, height=36)
        btn_close.pack(side="bottom", fill="x", padx=16, pady=12)

        scroll = cck.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=12, pady=(12, 0))

        # 0. СЕКЦИЯ ЭКСПОРТА ДАННЫХ
        exp_box = cck.CTkFrame(scroll, corner_radius=10,
                               fg_color="#1E3A8A" if self.tm.current != "light" else "#DBEAFE")
        exp_box.pack(fill="x", pady=6)
        cck.CTkLabel(exp_box, text="📊 Отчёты и экспорт", font=cck.CTkFont(weight="bold")).pack(pady=(8, 2))

        btn_export = cck.CTkButton(
            exp_box,
            text="📥 Выгрузить историю в Excel (.xlsx)",
            command=self._on_export,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=34,
            font=cck.CTkFont(weight="bold")
        )
        btn_export.pack(padx=20, pady=(4, 12), fill="x")

        # 1. Темы оформления
        t_box = cck.CTkFrame(scroll, corner_radius=10)
        t_box.pack(fill="x", pady=6)
        cck.CTkLabel(t_box, text="🎨 Тема оформления", font=cck.CTkFont(weight="bold")).pack(pady=(8, 4))
        self.t_var = cck.StringVar(value=self.tm.current)
        for label, val in [("Тёмная (стандарт)", "dark"), ("AMOLED (глубокий чёрный)", "amoled"),
                           ("Тёмно-синяя", "dark_blue")]:
            cck.CTkRadioButton(t_box, text=label, variable=self.t_var, value=val, command=self._on_theme).pack(
                anchor="w", padx=20, pady=4)
        cck.CTkLabel(t_box, text="").pack(pady=1)

        # 2. Размер шрифта таблицы истории
        f_box = cck.CTkFrame(scroll, corner_radius=10)
        f_box.pack(fill="x", pady=6)
        cck.CTkLabel(f_box, text="🔤 Размер шрифта истории транзакций", font=cck.CTkFont(weight="bold")).pack(
            pady=(8, 2))
        self.f_lbl = cck.CTkLabel(f_box, text=f"{self.parent.table_font_size} pt")
        self.f_slider = cck.CTkSlider(f_box, from_=9, to=18, number_of_steps=9, command=self._on_font_change)
        self.f_slider.set(self.parent.table_font_size)
        self.f_slider.pack(fill="x", padx=16, pady=4)
        self.f_lbl.pack(pady=(0, 6))

        # 3. Масштаб интерфейса
        s_box = cck.CTkFrame(scroll, corner_radius=10)
        s_box.pack(fill="x", pady=6)
        cck.CTkLabel(s_box, text="🔍 Масштаб всего окна", font=cck.CTkFont(weight="bold")).pack(pady=(8, 2))
        self.s_lbl = cck.CTkLabel(s_box, text=f"{int(self.parent.ui_scale * 100)}%")
        self.s_slider = cck.CTkSlider(s_box, from_=0.8, to=1.3, number_of_steps=5, command=self._on_scale)
        self.s_slider.set(self.parent.ui_scale)
        self.s_slider.pack(fill="x", padx=16, pady=4)
        self.s_lbl.pack(pady=(0, 6))

        # 4. Основная валюта
        c_box = cck.CTkFrame(scroll, corner_radius=10)
        c_box.pack(fill="x", pady=6)
        cck.CTkLabel(c_box, text="💰 Основная валюта", font=cck.CTkFont(weight="bold")).pack(pady=(8, 4))
        self.cur_opt = cck.CTkOptionMenu(c_box, values=["₽ (RUB)", "$ (USD)", "€ (EUR)", "¥ (CNY)"],
                                         command=self._on_curr_change)
        self.cur_opt.set(f"{self.parent.currency_symbol} ({self.parent.currency_code})")
        self.cur_opt.pack(padx=20, pady=(0, 10), fill="x")

        # 5. Анимация счетчиков
        a_box = cck.CTkFrame(scroll, corner_radius=10)
        a_box.pack(fill="x", pady=6)
        self.anim_switch = cck.CTkSwitch(a_box, text="Плавная анимация счетчиков", command=self._on_anim_toggle)
        if self.parent.animations_enabled:
            self.anim_switch.select()
        else:
            self.anim_switch.deselect()
        self.anim_switch.pack(padx=16, pady=10, anchor="w")

    def _on_export(self):
        self.parent.export_to_csv()

    def _on_theme(self):
        theme = self.t_var.get()
        self.tm.apply(theme)
        self.parent.current_theme = theme
        self.parent.set_table_font_size(self.parent.table_font_size, save=False)
        self.parent.save_app_settings()

    def _on_font_change(self, val):
        size = int(round(float(val)))
        self.f_lbl.configure(text=f"{size} pt")
        self.parent.set_table_font_size(size)

    def _on_scale(self, val):
        scale = round(float(val), 1)
        self.s_lbl.configure(text=f"{int(scale * 100)}%")
        self.parent.set_ui_scale(scale)

    def _on_curr_change(self, val):
        parts = val.split()
        sym = parts[0]
        code = parts[1].replace("(", "").replace(")", "")
        self.parent.set_currency(sym, code)

    def _on_anim_toggle(self):
        self.parent.animations_enabled = (self.anim_switch.get() == 1)
        self.parent.save_app_settings()
