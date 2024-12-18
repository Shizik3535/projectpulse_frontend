from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QMessageBox

from app.api.client import api_client

from app.ui.components.tables.tasks_with_project_table import TaskTableWithProject

from app.ui.forms.tasks.task_create_form import TaskCreateForm


class TasksManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client

        self.parent.statusbar.set_title("Управление задачами")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Кнопка добавления пользователя
        self.add_task_button = QPushButton("Добавить задачу")
        self.add_task_button.clicked.connect(self.add_task)

        # Таблица пользователей
        self.tasks = self.get_tasks()
        self.table_widget = TaskTableWithProject(
            self.tasks,
            row_double_click_callback=self.row_double_click_callback,
            parent=self.parent
        )

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.table_widget)

        layout.addWidget(self.add_task_button)
        layout.addWidget(self.scroll_area)

    def add_task(self):
        try:
            form = TaskCreateForm(self)
            form.exec()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка добавления задачи", f"Потоврите попытку или попробуйте позже: {str(e)}")

    def get_tasks(self):
        try:
            return self.client.managers.tasks.get_tasks()
        except Exception as e:
            print(e)
            return []

    def row_double_click_callback(self, task_id: int):
        self.parent.switch_page("management_task", params={'task_id': task_id})
