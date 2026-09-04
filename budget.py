# budget.py
import os
import sys
from tkinter import ttk
import customtkinter as cck

from budget_view import BudgetView
from charts_view import ChartsView
from config_manager import load_settings, save_settings
from crypto_utils import load_data, save_data
from themes import ThemeManager
from tools import FinancialToolsView

cck.set_appearance_mode("dark")
cck.set_default_color_theme("blue")

DEFAULT_CATEGORIES = [
    "Продукты",
    "Транспорт",
    "Кафе",
    "Жилье",
    "Здоровье",
    "Зарплата",
    "Другое",
]


def get_resource_path(relative_path):
  """Возвращает корректный путь к файлу как в PyCharm, так и внутри собранного .exe"""
  try:
    base_path = sys._MEIPASS
  except AttributeError:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)


class BudgetApp(cck.CTk):

  def __init__(self):
    super().__init__()
    self.title("FinTrack Pro — Управление личными финансами")
    self.geometry("1080x700")
    self.minsize(960, 620)

    # 1. Установка иконки окна и панели задач
    icon_path = get_resource_path("app_icon.ico")
    if os.path.exists(icon_path):
      try:
        self.iconbitmap(icon_path)
      except Exception:
        pass

    # 2. Загрузка конфигурации из settings.json
    cfg = load_settings()
    self.current_theme = cfg.get("theme", "dark")
    self.ui_scale = cfg.get("scale", 1.0)
    self.table_font_size = cfg.get("font_size", 11)
    self.currency_symbol = cfg.get("currency_symbol", "₽")
    self.currency_code = cfg.get("currency_code", "RUB")
    self.animations_enabled = cfg.get("animations_enabled", True)

    # 3. Загрузка базы транзакций
    raw = load_data()
    if isinstance(raw, dict):
      self.transactions = raw.get("transactions", [])
      self.categories = raw.get("categories", DEFAULT_CATEGORIES.copy())
    else:
      self.transactions = raw if isinstance(raw, list) else []
      self.categories = DEFAULT_CATEGORIES.copy()

    self.theme_manager = ThemeManager(self)

    # 4. Вкладки интерфейса со скруглением без артефактов
    self.tabs = cck.CTkTabview(
        self,
        corner_radius=12,
        fg_color="transparent",
        segmented_button_fg_color="#1E1E24",
        segmented_button_selected_color="#2563EB",
        segmented_button_selected_hover_color="#1D4ED8",
        segmented_button_unselected_color="#1E1E24",
        segmented_button_unselected_hover_color="#2A2A32",
        command=self._on_tab_change,
    )
    self.tabs._segmented_button.configure(corner_radius=10)
    self.tabs.pack(fill="both", expand=True, padx=12, pady=(4, 10))

    tab_b = self.tabs.add("📊 Бюджет и операции")
    tab_c = self.tabs.add("📈 Аналитика и графики")
    tab_t = self.tabs.add("🛠 Калькуляторы и ЦБ РФ")

    # 5. Инициализация экранов
    self.budget_view = BudgetView(tab_b, self)
    self.charts_view = ChartsView(tab_c, lambda: self.transactions)
    FinancialToolsView(tab_t)

    # 6. Применение настроек: тема -> шрифт -> таблица
    self.theme_manager.apply(self.current_theme)
    self.set_table_font_size(self.table_font_size, save=False)
    self.budget_view.update_table(animate=False)

    # Безопасное применение масштаба после загрузки GUI
    if self.ui_scale != 1.0:
      self.after(50, lambda: cck.set_widget_scaling(self.ui_scale))

  def _on_tab_change(self):
    if self.tabs.get() == "📈 Аналитика и графики":
      self.charts_view.draw_charts()

  def set_table_font_size(self, size, save=True):
    self.table_font_size = size
    style = ttk.Style()
    row_height = int(size * 2.2)
    style.configure("Treeview", font=("Segoe UI", size), rowheight=row_height)
    style.configure("Treeview.Heading", font=("Segoe UI", size, "bold"))

    if hasattr(self, "budget_view") and hasattr(self.budget_view, "tree"):
      self.budget_view.tree.configure(style="Treeview")

    if save:
      self.save_app_settings()

  def set_ui_scale(self, scale):
    self.ui_scale = scale
    cck.set_widget_scaling(scale)
    self.save_app_settings()

  def set_currency(self, symbol, code):
    self.currency_symbol = symbol
    self.currency_code = code
    self.budget_view.update_table(animate=False)
    self.save_app_settings()

  def save_app_settings(self):
    save_settings({
        "theme": self.current_theme,
        "scale": self.ui_scale,
        "font_size": self.table_font_size,
        "currency_symbol": self.currency_symbol,
        "currency_code": self.currency_code,
        "animations_enabled": self.animations_enabled,
    })

  def save_all(self):
    save_data({
        "transactions": self.transactions,
        "categories": self.categories,
    })


if __name__ == "__main__":
  app = BudgetApp()
  app.mainloop()

