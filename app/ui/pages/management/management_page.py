from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import Qt


class ManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()
        self.parent = parent
        self.params = params

        self.parent.statusbar.set_title("Управление")

        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Создаем кнопки
        self.button_users = QPushButton("Пользователи")
        self.button_tasks = QPushButton("Задачи")
        self.button_projects = QPushButton("Проекты")
        self.button_reports = QPushButton("Отчёты")

        # Настройка размеров кнопок
        self.button_users.setFixedSize(250, 50)
        self.button_tasks.setFixedSize(250, 50)
        self.button_projects.setFixedSize(505, 50)

        # Добавление кнопок в layout
        self.layout.addWidget(self.button_users, 0, 0)
        self.layout.addWidget(self.button_tasks, 0, 1)
        self.layout.addWidget(self.button_projects, 1, 0, 1, 2)

        # Устанавливаем выравнивание по центру
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Настройка контейнера
        self.setLayout(self.layout)

        # Связка кнопок с функциями
        self.button_users.clicked.connect(self.on_button_users_clicked)
        self.button_tasks.clicked.connect(self.on_button_tasks_clicked)
        self.button_projects.clicked.connect(self.on_button_projects_clicked)

        # Функции для каждой кнопки

    def on_button_users_clicked(self):
        self.parent.switch_page("management_users")

    def on_button_tasks_clicked(self):
        self.parent.switch_page("management_tasks")

    def on_button_projects_clicked(self):
        self.parent.switch_page("management_projects")
