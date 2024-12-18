from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QPushButton, QMessageBox, QFileDialog

from app.api.client import api_client

from app.ui.components.cards.project_card import ProjectCard
from app.ui.components.cards.empty_card import EmptyCard
from app.ui.components.tables.users_table import UserTable
from app.ui.components.tables.tasks_table import TaskTable


from app.ui.forms.projects.project_update_form import ProjectUpdateForm
from app.ui.forms.projects.project_member_management_form import ProjectMemberManagementForm
from app.ui.forms.projects.project_tasks_managents_form import ProjectTaskManagementForm


class ProjectManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client
        self.project_id = params.get('project_id')

        self.project_info = self.get_project_info()

        self.parent.statusbar.set_title(f"Управление проектом: {self.project_info.title}")

        if self.project_info:
            self.setup_ui()
        else:
            self.show_error()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Кнопки управления
        self.buttons_layout = QGridLayout()
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Редактиривать
        self.edit_button = QPushButton("Редактрировать")

        # Удалить
        self.delete_button = QPushButton("Удалить")

        # Управлять участиникми
        self.manage_member_button = QPushButton("Управлять участниками")

        # Управлять задачами
        self.manage_tasks_button = QPushButton("Управлять задачами")

        # Создать отчёт
        self.create_report_button = QPushButton("Создать отчёт")

        # Добавляем кнопки в макет
        self.buttons_layout.addWidget(self.edit_button, 0, 0)
        self.buttons_layout.addWidget(self.delete_button, 0, 1)
        self.buttons_layout.addWidget(self.manage_member_button, 0, 2)
        self.buttons_layout.addWidget(self.manage_tasks_button, 0, 3)
        self.buttons_layout.addWidget(self.create_report_button, 1, 0, 1, 4)

        # Добавляем действия на кнопки
        self.edit_button.clicked.connect(self.edit_project)
        self.delete_button.clicked.connect(self.delete_project)
        self.manage_member_button.clicked.connect(self.management_project_member)
        self.manage_tasks_button.clicked.connect(self.management_project_tasks)
        self.create_report_button.clicked.connect(self.create_report)

        # Добавление кнопок управления
        self.layout.addLayout(self.buttons_layout)

        # Основной контент
        self.content_layout = QGridLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Карточка проекта
        self.project_card = ProjectCard(self.project_info)
        self.content_layout.addWidget(self.project_card, 0, 0, 1, 1)

        # Таблица пользователей
        self.users = self.get_project_members()
        self.users_table = UserTable(
            self.users,
            parent=self,
            row_double_click_callback=self.user_row_double_click_callback
        )

        self.users_scroll_area = QScrollArea()
        self.users_scroll_area.setWidget(self.users_table)
        self.content_layout.addWidget(self.users_scroll_area, 0, 1, 1, 1)
        self.users_scroll_area.setWidgetResizable(True)

        # Таблица задач
        self.tasks = self.get_project_tasks()
        self.tasks_table = TaskTable(
            self.tasks,
            parent=self,
            row_double_click_callback=self.task_row_double_click_callback
        )

        self.tasks_scroll_area = QScrollArea()
        self.tasks_scroll_area.setWidget(self.tasks_table)
        self.content_layout.addWidget(self.tasks_scroll_area, 1, 0, 1, 2)
        self.tasks_scroll_area.setWidgetResizable(True)

        # Добавляем основной контент
        self.layout.addLayout(self.content_layout)

    def show_error(self):
        self.layout = QGridLayout()
        self.layout.addWidget(EmptyCard("Проект не найден"), 0, 0)
        self.setLayout(self.layout)

    def get_project_info(self):
        try:
            return self.client.managers.projects.get_project(self.project_id)
        except Exception as e:
            return None

    def get_project_members(self):
        try:
            return self.client.managers.projects.get_project_members(self.project_id)
        except Exception as e:
            return []

    def get_project_tasks(self):
        try:
            return self.client.managers.projects.get_project_tasks(self.project_id)
        except Exception as e:
            return []

    def edit_project(self):
        try:
            form = ProjectUpdateForm(self.project_info)
            form.exec()
            self.parent.switch_page("management_project", params={"project_id": self.project_id})
        except Exception as e:
            QMessageBox.critical(self, "Ошибка редактирования", "Потоврите попытку или попробуйте позже" + str(e))


    def delete_project(self):
        try:
            self.client.managers.projects.delete_project(self.project_id)
            self.parent.switch_page("management_projects")
        except:
            QMessageBox.critical(self, "Ошибка удаления", "Не удалось удалить задачу")

    def management_project_member(self):
        try:
            form = ProjectMemberManagementForm(self.project_id)
            form.exec()
            self.parent.switch_page("management_project", params={"project_id": self.project_id})
        except Exception as e:
            QMessageBox.critical(self, "Ошибка управления участниками", "Потоврите попытку или попробуйте позже" + str(e))

    def management_project_tasks(self):
        try:
            form = ProjectTaskManagementForm(self.project_id)
            form.exec()
            self.parent.switch_page("management_project", params={"project_id": self.project_id})
        except Exception as e:
            QMessageBox.critical(self, "Ошибка управления задачами", "Потоврите попытку или попробуйте позже" + str(e))

    def create_report(self):
        try:
            file = self.client.managers.reports.create_report_by_project(self.project_id)
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", f'Отчёт по проекту {self.project_info.title}', "Excel Files (*.xlsx);;All Files (*)")
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

    def user_row_double_click_callback(self, user_id: int):
        self.parent.switch_page("management_user", params={'user_id': user_id})

    def task_row_double_click_callback(self, task_id: int):
        self.parent.switch_page("management_task", params={'task_id': task_id})
