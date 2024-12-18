from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea

from app.api.client import api_client

from app.ui.components.cards.project_card import ProjectCard
from app.ui.components.cards.empty_card import EmptyCard
from app.ui.components.tables.tasks_table import TaskTable
from app.ui.components.tables.users_table import UserTable


class ProjectPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client
        self.project_id = params.get('project_id')

        self.project_info = self.get_project_info()

        self.parent.statusbar.set_title(f"проект: {self.project_info.title}")

        if self.project_info:
            self.setup_ui()
        else:
            self.show_error()

    def setup_ui(self):
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Карточка проекта
        self.project_card = ProjectCard(self.project_info)
        self.layout.addWidget(self.project_card, 0, 0, 1, 1)
        self.layout.setColumnStretch(0, 0)

        # Таблица пользователей
        self.users = self.get_project_users()
        self.users_table = UserTable(self.users)

        self.users_scroll_area = QScrollArea()
        self.users_scroll_area.setWidget(self.users_table)
        self.layout.addWidget(self.users_scroll_area, 0, 1, 1, 1)
        self.users_scroll_area.setWidgetResizable(True)

        # Таблица задач
        self.tasks = self.get_project_tasks()
        self.tasks_table = TaskTable(self.tasks)

        self.tasks_scroll_area = QScrollArea()
        self.tasks_scroll_area.setWidget(self.tasks_table)
        self.layout.addWidget(self.tasks_scroll_area, 1, 0, 1, 2)
        self.tasks_scroll_area.setWidgetResizable(True)

    def show_error(self):
        self.layout = QGridLayout()
        self.layout.addWidget(EmptyCard("Проект не найдена"), 0, 0)
        self.setLayout(self.layout)

    def get_project_info(self):
        try:
            return self.client.projects.get_project(self.project_id)
        except Exception as e:
            return None

    def get_project_users(self):
        try:
            return self.client.projects.get_project_members(self.project_id)
        except:
            return []

    def get_project_tasks(self):
        try:
            return self.client.projects.get_project_tasks(self.project_id)
        except:
            return []
