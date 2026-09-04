import xml.etree.ElementTree as ET
from tkinter import messagebox
import customtkinter as cck
import requests

CBR_URL = "https://cbr.ru"


def fetch_cbr_rates():
    """Получение официальных курсов валют ЦБ РФ"""
    rates = {"RUB": 1.0}
    try:
        resp = requests.get(CBR_URL, timeout=4)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for valute in root.findall("Valute"):
                char_code = valute.find("CharCode").text
                if char_code in ["USD", "EUR", "CNY", "KZT", "BYN"]:
                    nom = float(valute.find("Nominal").text)
                    val = float(valute.find("Value").text.replace(",", "."))
                    rates[char_code] = val / nom
    except Exception:
        # Резервные курсы на случай отсутствия сети
        rates.update(
            {"USD": 92.5, "EUR": 100.2, "CNY": 12.8, "KZT": 0.21, "BYN": 28.4}
        )
    return rates


class FinancialToolsView(cck.CTkScrollableFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.rates = fetch_cbr_rates()
        self._build_ui()

    def _build_ui(self):
        # 1. Конвертер валют ЦБ РФ
        c_box = cck.CTkFrame(self, corner_radius=10)
        c_box.pack(fill="x", pady=6, padx=5)
        cck.CTkLabel(
            c_box,
            text="💱 Конвертер валют (Курсы ЦБ РФ)",
            font=cck.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(10, 6))

        r1 = cck.CTkFrame(c_box, fg_color="transparent")
        r1.pack(fill="x", padx=15, pady=(0, 8))
        self.c_amt = cck.CTkEntry(r1, placeholder_text="Сумма", width=110)
        self.c_amt.pack(side="left", padx=(0, 6))

        curr_keys = list(self.rates.keys())
        self.c_from = cck.CTkComboBox(r1, values=curr_keys, width=80)
        self.c_from.set("USD")
        self.c_from.pack(side="left", padx=4)

        cck.CTkLabel(r1, text="➔").pack(side="left", padx=4)

        self.c_to = cck.CTkComboBox(r1, values=curr_keys, width=80)
        self.c_to.set("RUB")
        self.c_to.pack(side="left", padx=4)

        cck.CTkButton(
            r1, text="Расчет", width=80, command=self._convert_action
        ).pack(side="left", padx=8)

        self.c_res = cck.CTkLabel(
            c_box, text="Результат: 0.00", font=cck.CTkFont(size=13)
        )
        self.c_res.pack(anchor="w", padx=15, pady=(0, 10))

        # 2. Калькулятор инфляции
        i_box = cck.CTkFrame(self, corner_radius=10)
        i_box.pack(fill="x", pady=6, padx=5)
        cck.CTkLabel(
            i_box,
            text="📈 Калькулятор инфляции",
            font=cck.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(10, 6))

        r2 = cck.CTkFrame(i_box, fg_color="transparent")
        r2.pack(fill="x", padx=15, pady=(0, 8))
        self.inf_amt = cck.CTkEntry(r2, placeholder_text="Сумма (₽)", width=110)
        self.inf_amt.pack(side="left", padx=(0, 6))
        self.inf_pct = cck.CTkEntry(
            r2, placeholder_text="Инфляция %", width=95
        )
        self.inf_pct.pack(side="left", padx=4)
        self.inf_yrs = cck.CTkEntry(r2, placeholder_text="Лет", width=70)
        self.inf_yrs.pack(side="left", padx=4)
        cck.CTkButton(
            r2, text="Оценить", width=80, command=self._inflation_action
        ).pack(side="left", padx=8)

        self.inf_res = cck.CTkLabel(
            i_box, text="—", font=cck.CTkFont(size=12), justify="left"
        )
        self.inf_res.pack(anchor="w", padx=15, pady=(0, 10))

        # 3. Кредитный и депозитный калькулятор
        l_box = cck.CTkFrame(self, corner_radius=10)
        l_box.pack(fill="x", pady=6, padx=5)
        cck.CTkLabel(
            l_box,
            text="💳 Кредитный / Депозитный калькулятор",
            font=cck.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(10, 6))

        r3 = cck.CTkFrame(l_box, fg_color="transparent")
        r3.pack(fill="x", padx=15, pady=(0, 8))
        self.calc_mode = cck.CTkSegmentedButton(
            r3, values=["Кредит", "Вклад"], width=130
        )
        self.calc_mode.set("Кредит")
        self.calc_mode.pack(side="left", padx=(0, 8))

        self.calc_sum = cck.CTkEntry(
            r3, placeholder_text="Сумма (₽)", width=110
        )
        self.calc_sum.pack(side="left", padx=4)
        self.calc_rate = cck.CTkEntry(r3, placeholder_text="Ставка %", width=85)
        self.calc_rate.pack(side="left", padx=4)
        self.calc_months = cck.CTkEntry(
            r3, placeholder_text="Месяцев", width=80
        )
        self.calc_months.pack(side="left", padx=4)

        cck.CTkButton(
            r3, text="Посчитать", width=90, command=self._credit_deposit_action
        ).pack(side="left", padx=8)

        self.calc_res = cck.CTkLabel(
            l_box, text="—", font=cck.CTkFont(size=12), justify="left"
        )
        self.calc_res.pack(anchor="w", padx=15, pady=(0, 10))

    def _convert_action(self):
        try:
            val = float(self.c_amt.get().strip().replace(",", "."))
            fr, to = self.c_from.get(), self.c_to.get()
            res = (val * self.rates[fr]) / self.rates[to]
            self.c_res.configure(
                text=f"{val:,.2f} {fr} = {res:,.2f} {to}", text_color="#3B8ED0"
            )
        except Exception:
            messagebox.showwarning("Ошибка", "Введите корректную сумму!")

    def _inflation_action(self):
        try:
            amt = float(self.inf_amt.get().strip().replace(",", "."))
            rate = float(self.inf_pct.get().strip().replace(",", "."))
            yrs = int(self.inf_yrs.get().strip())
            real_val = amt / ((1 + rate / 100) ** yrs)
            lost = amt - real_val
            self.inf_res.configure(
                text=f"Через {yrs} лет реальная ценность капитала: {real_val:,.2f} ₽ (потери: -{lost:,.2f} ₽)"
            )
        except Exception:
            messagebox.showwarning("Ошибка", "Проверьте введённые данные!")

    def _credit_deposit_action(self):
        try:
            s = float(self.calc_sum.get().strip().replace(",", "."))
            r = float(self.calc_rate.get().strip().replace(",", ".")) / 100 / 12
            m = int(self.calc_months.get().strip())

            if self.calc_mode.get() == "Кредит":
                # Аннуитетный платеж
                pmt = s * (r * (1 + r) ** m) / ((1 + r) ** m - 1)
                total = pmt * m
                self.calc_res.configure(
                    text=f"Платеж: {pmt:,.2f} ₽/мес | Всего к возврату: {total:,.2f} ₽ | Переплата: {total - s:,.2f} ₽"
                )
            else:
                # Вклад с ежемесячной капитализацией
                final = s * ((1 + r) ** m)
                profit = final - s
                self.calc_res.configure(
                    text=f"Итог через {m} мес: {final:,.2f} ₽ | Начисленные проценты: +{profit:,.2f} ₽"
                )
        except Exception:
            messagebox.showwarning(
                "Ошибка", "Заполните сумму, ставку и срок в месяцах!"
            )
