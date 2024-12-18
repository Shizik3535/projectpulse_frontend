from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QMessageBox

from app.api.client import api_client

from app.ui.components.tables.users_table import UserTable

from app.ui.forms.users.user_create_form import UserCreateForm


class UsersManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client

        self.parent.statusbar.set_title("Управление пользователями")

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Кнопка добавления пользователя
        self.add_user_button = QPushButton("Добавить пользователя")
        self.add_user_button.clicked.connect(self.add_user)

        # Таблица пользователей
        self.users = self.get_users()
        self.table_widget = UserTable(self.users, row_double_click_callback=self.row_double_click_callback, parent=self.parent)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.table_widget)

        layout.addWidget(self.add_user_button)
        layout.addWidget(self.scroll_area)

    def add_user(self):
        try:
            form = UserCreateForm(self)
            form.exec()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка добавления пользователя", f"Потоврите попытку или попробуйте позже: {str(e)}")

    def get_users(self):
        try:
            return self.client.managers.users.get_users()
        except Exception as e:
            return []

    def row_double_click_callback(self, user_id: int):
        self.parent.switch_page("management_user", params={'user_id': user_id})
