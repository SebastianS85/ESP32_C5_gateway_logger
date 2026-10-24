import sys
import logging

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication


def _windows_prefers_light_mode():
    if sys.platform != "win32":
        return False

    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        ) as key:
            return bool(winreg.QueryValueEx(key, "AppsUseLightTheme")[0])
    except FileNotFoundError:
        return False
    except OSError:
        logging.warning("Unable to read Windows app theme preference; using dark theme", exc_info=True)
        return False


def apply_system_theme(app):
    light = _windows_prefers_light_mode()
    app.setProperty("canAnalyserLightTheme", light)
    app.setStyle("Fusion")

    colors = {
        "window": "#f4f6f8" if light else "#1b1b1b",
        "window_text": "#202833" if light else "#cccccc",
        "base": "#ffffff" if light else "#141414",
        "alternate": "#edf1f5" if light else "#1b1b1b",
        "text": "#202833" if light else "#e0e0e0",
        "button": "#e6ebf0" if light else "#2c2c2c",
        "button_text": "#202833" if light else "#e0e0e0",
        "highlight": "#cfe5ff" if light else "#2c3e50",
        "highlighted_text": "#15283d" if light else "#ffffff",
        "tooltip": "#fffbe8" if light else "#2c2c2c",
        "tooltip_text": "#202833" if light else "#e0e0e0",
        "disabled_text": "#8993a0" if light else "#666666",
        "border": "#c7d0da" if light else "#383838",
        "muted": "#586575" if light else "#aaaaaa",
        "accent": "#087a59" if light else "#00dd99",
        "table_text": "#183e5c" if light else "#00e5ff",
        "surface": "#e9eef3" if light else "#222222",
        "tab": "#e4e9ef" if light else "#222222",
        "pane": "#ffffff" if light else "#161616",
        "input": "#ffffff" if light else "#141414",
        "selection": "#d9eaff" if light else "#2c3e50",
        "selection_text": "#15283d" if light else "#ffffff",
        "grid": "#d5dce4" if light else "#242424",
        "disabled_bg": "#edf0f3" if light else "#181818",
        "disabled_border": "#d7dde4" if light else "#242424",
        "disabled_button_text": "#9aa3ad" if light else "#555555",
        "focus": "#2d7dd2" if light else "#6ec5ff",
        "stats": "#8a4b00" if light else "#ffb74d",
    }

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(colors["window"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["window_text"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(colors["base"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["alternate"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
    palette.setColor(QPalette.ColorRole.Button, QColor(colors["button"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["button_text"]))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["tooltip"]))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["tooltip_text"]))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["highlight"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["highlighted_text"]))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors["muted"]))
    palette.setColor(QPalette.ColorRole.Link, QColor(colors["accent"]))
    palette.setColor(QPalette.ColorRole.Mid, QColor(colors["border"]))
    for group in (QPalette.ColorGroup.Disabled,):
        palette.setColor(group, QPalette.ColorRole.WindowText, QColor(colors["disabled_text"]))
        palette.setColor(group, QPalette.ColorRole.Text, QColor(colors["disabled_text"]))
        palette.setColor(group, QPalette.ColorRole.ButtonText, QColor(colors["disabled_button_text"]))
    app.setPalette(palette)

    app.setStyleSheet(f"""
        QMainWindow, QWidget {{ background-color: {colors["window"]}; color: {colors["window_text"]}; font-family: "Segoe UI", sans-serif; }}
        QToolTip {{ background-color: {colors["tooltip"]}; color: {colors["tooltip_text"]}; border: 1px solid {colors["border"]}; padding: 4px; }}
        QPushButton {{ background-color: {colors["button"]}; color: {colors["button_text"]}; border: 1px solid {colors["border"]}; border-radius: 4px; padding: 6px 10px; font-weight: bold; font-size: 11px; }}
        QPushButton:hover {{ background-color: {colors["surface"]}; border-color: {colors["focus"]}; }}
        QPushButton:pressed {{ background-color: {colors["alternate"]}; }}
        QPushButton:checked {{ background-color: #d28e00; color: #111111; border-color: #b87a00; }}
        QPushButton#btnSendOnce {{ background-color: #1769aa; color: #ffffff; border-color: #145b94; }}
        QPushButton#btnSendOnce:hover {{ background-color: #0e5c9e; }}
        QPushButton#btnStartCyclic {{ background-color: #238636; color: #ffffff; border-color: #1c6e2c; }}
        QPushButton#btnStartCyclic:hover {{ background-color: #1d742e; }}
        QPushButton#btnStopCyclic {{ background-color: #b4232f; color: #ffffff; border-color: #9c1c27; }}
        QPushButton#btnStopCyclic:hover {{ background-color: #991b25; }}
        QPushButton#btnExport {{ background-color: #d28e00; color: #111111; border-color: #b87a00; }}
        QPushButton#btnExport:hover {{ background-color: #e5a417; }}
        QPushButton:disabled {{ background-color: {colors["disabled_bg"]}; color: {colors["disabled_button_text"]}; border-color: {colors["disabled_border"]}; }}
        QLineEdit, QComboBox {{ background-color: {colors["input"]}; color: {colors["text"]}; border: 1px solid {colors["border"]}; border-radius: 3px; padding: 4px; selection-background-color: {colors["highlight"]}; selection-color: {colors["highlighted_text"]}; }}
        QLineEdit:focus, QComboBox:focus {{ border-color: {colors["focus"]}; }}
        QComboBox QAbstractItemView {{ background-color: {colors["base"]}; color: {colors["text"]}; selection-background-color: {colors["highlight"]}; selection-color: {colors["highlighted_text"]}; }}
        QCheckBox {{ spacing: 5px; }}
        QCheckBox::indicator {{ width: 14px; height: 14px; }}
        QTabWidget::pane {{ border: 1px solid {colors["border"]}; background-color: {colors["pane"]}; }}
        QTabBar::tab {{ background-color: {colors["tab"]}; color: {colors["muted"]}; padding: 7px 14px; border-top-left-radius: 3px; border-top-right-radius: 3px; margin-right: 2px; }}
        QTabBar::tab:selected {{ background-color: {colors["pane"]}; color: {colors["window_text"]}; font-weight: bold; }}
        QTabBar::tab:hover {{ color: {colors["window_text"]}; }}
        QGroupBox {{ border: 1px solid {colors["border"]}; border-radius: 4px; margin-top: 8px; font-weight: bold; color: {colors["muted"]}; }}
        QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 4px; }}
        QTableView, QTableWidget {{ background-color: {colors["base"]}; alternate-background-color: {colors["alternate"]}; color: {colors["table_text"]}; gridline-color: {colors["grid"]}; outline: none; border: 1px solid {colors["border"]}; selection-background-color: {colors["selection"]}; selection-color: {colors["selection_text"]}; }}
        QTableView::item:selected, QTableWidget::item:selected {{ background-color: {colors["selection"]}; color: {colors["selection_text"]}; }}
        QHeaderView::section {{ background-color: {colors["surface"]}; color: {colors["window_text"]}; padding: 5px; border: 1px solid {colors["border"]}; }}
        QScrollArea {{ border: none; background-color: transparent; }}
        QScrollBar:vertical, QScrollBar:horizontal {{ background-color: {colors["alternate"]}; border: none; }}
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{ background-color: {colors["border"]}; border-radius: 4px; min-height: 24px; min-width: 24px; }}
        QFrame#chartControlBar {{ background-color: {colors["surface"]}; border: 1px solid {colors["border"]}; border-radius: 6px; }}
        QLineEdit.chartInput {{ background-color: {colors["input"]}; color: {colors["text"]}; border: 1px solid {colors["border"]}; font-weight: bold; }}
        QLineEdit.chartInput:focus {{ border: 1px solid {colors["focus"]}; }}
        QTableWidget#statsTable {{ color: {colors["stats"]}; }}
        QLabel#speedLabel {{ color: {colors["stats"]}; }}
        QLabel#statusLabel {{ font-weight: bold; padding: 4px; border-radius: 4px; }}
        QLabel#statusLabel[connected="true"] {{ background-color: #238636; color: #ffffff; }}
        QLabel#statusLabel[connected="false"] {{ background-color: #b4232f; color: #ffffff; }}
        QLineEdit#ipInput[connected="true"] {{ border-color: #238636; }}
        QLineEdit#ipInput[connected="false"] {{ border-color: #b4232f; }}
    """)
