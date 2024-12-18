from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea

from app.api.client import api_client

from app.ui.components.cards.task_card import TaskCard
from app.ui.components.cards.empty_card import EmptyCard
from app.ui.components.cards.project_card import ProjectCard
from app.ui.components.tables.users_table import UserTable


class TaskPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client
        self.task_id = params.get('task_id')

        self.task_info = self.get_task_info()

        self.parent.statusbar.set_title(f"Задача: {self.task_info.title}")

        if self.task_info:
            self.setup_ui()
        else:
            self.show_error()

    def setup_ui(self):
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Карточка задачи
        self.task_card = TaskCard(self.task_info, False)
        self.layout.addWidget(self.task_card, 0, 0, 1, 1)

        # Карточка проекта
        if self.task_info.project:
            self.project_card = ProjectCard(self.task_info.project)
        else:
            self.project_card = EmptyCard("Проект отсутствует")
        self.layout.addWidget(self.project_card, 0, 1, 1, 1)

        # Таблица пользователей
        self.users = self.get_task_users()
        self.users_table = UserTable(self.users, parent=None)

        self.users_scroll_area = QScrollArea()
        self.users_scroll_area.setWidget(self.users_table)
        self.layout.addWidget(self.users_scroll_area, 2, 0, 1, 2)
        self.users_scroll_area.setWidgetResizable(True)

    def show_error(self):
        self.layout = QGridLayout()
        self.layout.addWidget(EmptyCard("Задача не найдена"), 0, 0)
        self.setLayout(self.layout)

    def get_task_info(self):
        try:
            return self.client.tasks.get_task(self.task_id)
        except Exception as e:
            return None

    def get_task_users(self):
        try:
            return self.client.tasks.get_task_assignments(self.task_id)
        except Exception as e:
            return []
