# charts_view.py
import customtkinter as cck
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartsView(cck.CTkFrame):
    def __init__(self, parent, get_transactions_callback):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.get_transactions = get_transactions_callback
        self.chart_canvas = None

    def draw_charts(self):
        """Отрисовка круговой диаграммы и гистограммы потоков"""
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        bg_col = "#1E1E24"
        text_col = "#E2E8F0"

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2), facecolor=bg_col)

        transactions = self.get_transactions()
        exp_by_cat = {}
        inc_total, exp_total = 0.0, 0.0

        for t in transactions:
            if t["type"] == "Расход":
                exp_total += t["amount"]
                exp_by_cat[t["cat"]] = exp_by_cat.get(t["cat"], 0) + t["amount"]
            else:
                inc_total += t["amount"]

        # Круговая диаграмма
        if exp_by_cat:
            colors = ["#38BDF8", "#F87171", "#FBBF24", "#34D399", "#A78BFA", "#F472B6", "#94A3B8"]
            ax1.pie(exp_by_cat.values(), labels=exp_by_cat.keys(), autopct="%1.1f%%",
                    colors=colors[:len(exp_by_cat)],
                    textprops={"color": text_col, "fontsize": 9},
                    wedgeprops={"edgecolor": bg_col, "linewidth": 2})
            ax1.set_title("Расходы по категориям", color=text_col, fontsize=11, weight="bold")
        else:
            ax1.text(0.5, 0.5, "Нет расходов для анализа", ha="center", va="center", color=text_col)
            ax1.axis("off")

        # Столбчатая диаграмма
        ax2.bar(["Доходы", "Расходы"], [inc_total, exp_total], color=["#34D399", "#F87171"], width=0.45)
        ax2.set_facecolor(bg_col)
        ax2.tick_params(colors=text_col)
        for spine in ax2.spines.values():
            spine.set_color(text_col)
        ax2.set_title("Соотношение потоков (₽)", color=text_col, fontsize=11, weight="bold")

        fig.tight_layout()
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
