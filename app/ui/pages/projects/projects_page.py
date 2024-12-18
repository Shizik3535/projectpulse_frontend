from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from app.api.client import api_client

from app.ui.components.tables.projects_table import ProjectTable


class ProjectsPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()
        self.parent = parent
        self.params = params
        self.client = api_client

        self.parent.statusbar.set_title("Проекты")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

        self.projects = self.get_projects()
        table_widget = ProjectTable(self.projects, row_double_click_callback=self.row_double_click_callback)
        scroll_area.setWidget(table_widget)

    def get_projects(self):
        try:
            return self.client.projects.get_user_projects()
        except Exception as e:
            return []

    def row_double_click_callback(self, project_id: int):
        self.parent.switch_page("project", params={"project_id": project_id})
