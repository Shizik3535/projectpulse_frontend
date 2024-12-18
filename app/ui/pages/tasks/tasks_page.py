from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from app.api.client import api_client

from app.ui.components.tables.tasks_with_project_table import TaskTableWithProject


class TasksPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client

        self.parent.statusbar.set_title("Задачи")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

        self.tasks = self.get_tasks()
        table_widget = TaskTableWithProject(self.tasks, row_double_click_callback=self.row_double_click_callback)
        scroll_area.setWidget(table_widget)

    def get_tasks(self):
        try:
            return self.client.tasks.get_user_tasks()
        except Exception as e:
            return []

    def row_double_click_callback(self, task_id: int):
        self.parent.switch_page("task", params={"task_id": task_id})
