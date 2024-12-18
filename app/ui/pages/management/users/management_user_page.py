from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QPushButton, QMessageBox, QFileDialog

from app.api.client import api_client

from app.ui.components.cards.user_card import UserCard
from app.ui.components.cards.empty_card import EmptyCard
from app.ui.components.tables.tasks_with_project_table import TaskTableWithProject
from app.ui.components.tables.projects_table import ProjectTable

from app.ui.forms.users.user_update_form import UserUpdateForm


class UserManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client
        self.user_id = params.get('user_id')

        self.user_info = self.get_user_info()

        self.parent.statusbar.set_title(f"Управление пользователем: {str(self.user_info.first_name + " " + self.user_info.last_name) if self.user_info else ""}")

        if self.user_info:
            self.setup_ui()
        else:
            self.show_error()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Кнопки управления
        self.buttons_layout = QGridLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Редактировать
        self.edit_button = QPushButton("Редактировать")

        # Удалить
        self.delete_button = QPushButton("Удалить")

        # Создать отчёт
        self.create_report_button = QPushButton("Создать отчёт")

        # Добавление кнопок управления
        self.buttons_layout.addWidget(self.edit_button, 0, 0)
        self.buttons_layout.addWidget(self.delete_button, 0, 1)
        self.buttons_layout.addWidget(self.create_report_button, 1, 0, 1, 2)

        # Добавление действий на кнопки
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.create_report_button.clicked.connect(self.create_report)

        # Добавление кнопок управления
        self.layout.addLayout(self.buttons_layout)

        # Основной контент
        self.content_layout = QGridLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Карточка пользователя
        self.user_card = UserCard(self.user_info)
        self.content_layout.addWidget(self.user_card, 0, 0, 1, 1)

        # Таблица проектов
        self.projects = self.get_user_projects()
        self.projects_table = ProjectTable(
            self.projects,
            row_double_click_callback=self.project_row_double_click_callback,
            parent=self,
        )

        self.projects_scroll_area = QScrollArea()
        self.projects_scroll_area.setWidget(self.projects_table)
        self.content_layout.addWidget(self.projects_scroll_area, 0, 1, 1, 2)
        self.projects_scroll_area.setWidgetResizable(True)

        # Таблица задач
        self.tasks = self.get_user_tasks()
        self.tasks_table = TaskTableWithProject(
            self.tasks,
            parent=self,
            row_double_click_callback=self.task_row_double_click_callback,
        )

        self.tasks_scroll_area = QScrollArea()
        self.tasks_scroll_area.setWidget(self.tasks_table)
        self.content_layout.addWidget(self.tasks_scroll_area, 1, 0, 1, 3)
        self.tasks_scroll_area.setWidgetResizable(True)

        self.layout.addLayout(self.content_layout)

    def show_error(self):
        self.layout = QGridLayout()
        self.layout.addWidget(EmptyCard("Задача не найдена"), 0, 0)
        self.setLayout(self.layout)

    def get_user_info(self):
        try:
            return self.client.managers.users.get_user(self.user_id)
        except Exception as e:
            return None

    def get_user_projects(self):
        try:
            return self.client.managers.users.get_user_projects(self.user_id)
        except Exception as e:
            return []

    def get_user_tasks(self):
        try:
            return self.client.managers.users.get_user_tasks(self.user_id)
        except Exception as e:
            return []

    def edit_user(self):
        try:
            form = UserUpdateForm(user_data=self.user_info, parent=self)
            form.exec()
            self.parent.switch_page("management_user", params={"user_id": self.user_id})
        except:
            QMessageBox.critical(self, "Ошибка редактирования", "Потоврите попытку или попробуйте позже")

    def delete_user(self):
        try:
            self.client.managers.users.delete_user(self.user_id)
            self.parent.switch_page("management_users")
        except:
            QMessageBox.critical(self, "Ошибка удаления", "Не удалось удалить пользователя")

    def create_report(self):
        try:
            file = self.client.managers.reports.create_report_by_user(self.user_id)
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл",
                                                       f'Отчёт по сотруднику {self.user_info.first_name} {self.user_info.last_name}',
                                                       "Excel Files (*.xlsx);;All Files (*)")
            if save_path:
                try:
                    with open(save_path, "wb") as f:
                        f.write(file)
                    QMessageBox.information(self, "Успех", "Файл успешно сохранен!")
                    return
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
            else:
                QMessageBox.warning(self, "Отмена", "Вы не выбрали место для сохранения файла.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка создания отчёта", "Попробуйте ещё раз или попробуйте позже: " + str(e))

    def task_row_double_click_callback(self, task_id: int):
        self.parent.switch_page("management_task", params={'task_id': task_id})


    def project_row_double_click_callback(self, project_id: int):
        self.parent.switch_page("management_project", params={'project_id': project_id})
