from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea

from app.api.client import api_client

from app.ui.components.cards.user_card import UserCard
from app.ui.components.tables.projects_table import ProjectTable
from app.ui.components.tables.tasks_with_project_table import TaskTableWithProject


class HomePage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()
        self.params = params
        self.parent = parent
        self.client = api_client

        self.user_data = api_client.auth.get_user_info()

        self.parent.statusbar.set_title("Главная")

        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Карточка пользователя
        self.user_card = UserCard(self.user_data)
        self.layout.addWidget(self.user_card, 0, 0, 1, 1)

        # Таблица проектов
        self.projects = self.get_projects()
        self.projects_table = ProjectTable(
            self.projects,
            row_double_click_callback=self.project_row_double_click_callback,
            parent=self
        )

        self.projects_scroll_area = QScrollArea()
        self.projects_scroll_area.setWidget(self.projects_table)
        self.layout.addWidget(self.projects_scroll_area, 0, 1, 1, 2)
        self.projects_scroll_area.setWidgetResizable(True)

        # таблица задач
        self.tasks = self.get_tasks()
        self.tasks_table = TaskTableWithProject(
            self.tasks,
            row_double_click_callback=self.task_row_double_click_task_callback,
            parent=self
        )

        self.tasks_scroll_area = QScrollArea()
        self.tasks_scroll_area.setWidget(self.tasks_table)
        self.layout.addWidget(self.tasks_scroll_area, 1, 0, 1, 3)
        self.tasks_scroll_area.setWidgetResizable(True)

    def get_projects(self):
        try:
            return self.client.projects.get_user_projects()
        except Exception as e:
            return []

    def get_tasks(self):
        try:
            return self.client.tasks.get_user_tasks()
        except Exception as e:
            return []

    def task_row_double_click_task_callback(self, task_id: int):
        self.parent.switch_page("task", params={"task_id": task_id})

    def project_row_double_click_callback(self, project_id: int):
        self.parent.switch_page("project", params={"project_id": project_id})