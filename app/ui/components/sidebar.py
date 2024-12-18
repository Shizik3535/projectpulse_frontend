from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton


class SideBar(QFrame):
    def __init__(self, role: str, parent=None):
        super().__init__(parent)

        self.role = role
        self.parent = parent
        self.setFixedWidth(200)

        # Контейнер
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Кнопки меню
        self.home_button = QPushButton("Главная")
        self.projects_button = QPushButton("Проекты")
        self.tasks_button = QPushButton("Задачи")
        if self.role in ["Менеджер"]:
            self.management_button = QPushButton("Управление")
        self.settings_button = QPushButton("Настройки")

        # Добавление кнопок в контейнер
        self.layout.addWidget(self.home_button)
        self.layout.addWidget(self.projects_button)
        self.layout.addWidget(self.tasks_button)
        if self.role in ["Менеджер"]:
            self.layout.addWidget(self.management_button)
        self.layout.addStretch()
        self.layout.addWidget(self.settings_button)

        # Установка обработчиков событий
        self.home_button.clicked.connect(lambda: self.parent.switch_page("home"))
        self.projects_button.clicked.connect(lambda: self.parent.switch_page("projects"))
        self.tasks_button.clicked.connect(lambda: self.parent.switch_page("tasks"))
        if self.role in ["Менеджер"]:
            self.management_button.clicked.connect(lambda: self.parent.switch_page("management"))
        self.settings_button.clicked.connect(lambda: self.parent.switch_page("settings"))
