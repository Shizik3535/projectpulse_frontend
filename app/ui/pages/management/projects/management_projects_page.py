from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QMessageBox

from app.api.client import api_client

from app.ui.components.tables.projects_table import ProjectTable

from app.ui.forms.projects.project_create_form import ProjectCreateForm


class ProjectsManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client

        self.parent.statusbar.set_title("Управление проектами")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Кнопка добавления пользователя
        self.add_project_button = QPushButton("Добавить проект")
        self.add_project_button.clicked.connect(self.add_project)

        # Таблица пользователей
        self.projects = self.get_projects()
        self.table_widget = ProjectTable(
            self.projects,
            row_double_click_callback=self.row_double_click_callback,
            parent=self.parent
        )

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.table_widget)

        layout.addWidget(self.add_project_button)
        layout.addWidget(self.scroll_area)

    def add_project(self):
        try:
            form = ProjectCreateForm(self)
            form.exec()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка добавления проекта", f"Потоврите попытку или попробуйте позже: {str(e)}")

    def get_projects(self):
        try:
            return self.client.managers.projects.get_projects()
        except Exception as e:
            print(e)
            return []

    def row_double_click_callback(self, project_id: int):
        self.parent.switch_page("management_project", params={'project_id': project_id})
