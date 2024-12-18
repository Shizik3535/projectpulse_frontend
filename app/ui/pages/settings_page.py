from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from qt_material import apply_stylesheet

from app.core.settings import app_settings  # Импортируйте настройки приложения, если необходимо


class SettingsPage(QFrame):
    def __init__(self, params=None, parent=None):
        super().__init__()
        self.parent = parent
        self.params = params

        self.parent.statusbar.set_title("Настройки")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        # Заголовок
        title_label = QLabel("Выберите тему:")
        layout.addWidget(title_label)

        self.themes_dict = {
            "Светлая Голубая": "light_blue",
            "Светлая Зелёная": "light_lightgreen",
            "Светлая Розовая": "light_pink",
            "Светлая Фиолетовая": "light_purple",
            "Светлая Красная": "light_red",
            "Тёмная Амбер": "dark_amber",
            "Тёмная Голубая": "dark_blue",
            "Тёмная Циан": "dark_cyan",
            "Тёмная Зелёная": "dark_lightgreen",
            "Тёмная Розовая": "dark_pink",
            "Тёмная Фиолетовая": "dark_purple",
            "Тёмная Красная": "dark_red",
            "Тёмная Бирюзовая": "dark_teal",
            "Тёмная Жёлтая": "dark_yellow",
        }

        # Выпадающий список для выбора темы
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.themes_dict.keys())  # Добавляем русские названия в список
        layout.addWidget(self.theme_combo)

        # Устанавливаем тему из настроек по умолчанию, если она есть
        current_theme = app_settings.value('theme')
        if current_theme:
            # Находим соответствующее русское название темы
            for key, value in self.themes_dict.items():
                if value == current_theme:
                    self.theme_combo.setCurrentText(key)
                    break

        # Подключаем сигнал для отслеживания изменений в выпадающем списке
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)

        layout.addStretch()

        # Кнопка выхода
        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.on_exit_button_click)
        layout.addWidget(exit_button)

    def on_theme_changed(self, index):
        """Обработчик для изменения темы"""
        selected_theme = self.theme_combo.currentText()
        real_theme = self.themes_dict[selected_theme]
        app_settings.setValue('theme', real_theme)
        try:
            apply_stylesheet(self.parent, f"{real_theme}.xml")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось применить тему: {str(e)}")

    def on_exit_button_click(self):
        app_settings.remove("token")
        self.parent.close()
