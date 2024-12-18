from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QScrollArea, QPushButton, QMessageBox, QFileDialog

from app.api.client import api_client

from app.ui.components.cards.task_card import TaskCard
from app.ui.components.cards.project_card import ProjectCard
from app.ui.components.cards.empty_card import EmptyCard
from app.ui.components.tables.users_table import UserTable

from app.ui.forms.tasks.task_update_form import TaskUpdateForm
from app.ui.forms.tasks.task_assignments_management_form import TaskAssignmentsManagementForm


class TaskManagementPage(QWidget):
    def __init__(self, params=None, parent=None):
        super().__init__()

        self.params = params
        self.parent = parent
        self.client = api_client
        self.task_id = params.get('task_id')

        self.task_info = self.get_task_info()

        self.parent.statusbar.set_title(f"Управление задачей: {self.task_info.title}")

        if self.task_info:
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
        self.manage_assignments_button = QPushButton("Управлять участниками")

        # Создать отчёт
        self.create_report_button = QPushButton("Создать отчёт")

        # Добавляем кнопки в макет
        self.buttons_layout.addWidget(self.edit_button, 0, 0)
        self.buttons_layout.addWidget(self.delete_button, 0, 1)
        self.buttons_layout.addWidget(self.manage_assignments_button, 0, 2)
        self.buttons_layout.addWidget(self.create_report_button, 1, 0, 1, 3)

        # Добавляем действия на кнопки
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.manage_assignments_button.clicked.connect(self.management_task_assignments)
        self.create_report_button.clicked.connect(self.create_report)

        # Добавление кнопок управления
        self.layout.addLayout(self.buttons_layout)

        # Основной контент
        self.content_layout = QGridLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Карточка задачи
        self.task_card = TaskCard(self.task_info, True)
        self.content_layout.addWidget(self.task_card, 0, 0, 1, 1)

        # Карточка проекта
        if self.task_info.project:
            self.project_card = ProjectCard(self.task_info.project)
        else:
            self.project_card = EmptyCard("Проект отсутствует")
        self.content_layout.addWidget(self.project_card, 0, 1, 1, 1)

        # Таблица пользователей
        self.users = self.get_task_assignments()
        self.users_table = UserTable(
            self.users,
            parent=self,
            row_double_click_callback=self.user_row_double_click_callback
        )

        self.users_scroll_area = QScrollArea()
        self.users_scroll_area.setWidget(self.users_table)
        self.content_layout.addWidget(self.users_scroll_area, 2, 0, 1, 2)
        self.users_scroll_area.setWidgetResizable(True)

        # Добавляем основной контент
        self.layout.addLayout(self.content_layout)

    def show_error(self):
        self.layout = QGridLayout()
        self.layout.addWidget(EmptyCard("Задача не найдена"), 0, 0)
        self.setLayout(self.layout)

    def get_task_info(self):
        try:
            return self.client.managers.tasks.get_task(self.task_id)
        except Exception as e:
            return None

    def get_task_assignments(self):
        try:
            return self.client.managers.tasks.get_task_assignments(self.task_id)
        except Exception as e:
            return []

    def edit_task(self):
        try:
            form = TaskUpdateForm(self.task_info)
            form.exec()
            self.parent.switch_page("management_task", params={"task_id": self.task_id})
        except Exception as e:
            QMessageBox.critical(self, "Ошибка редактирования", "Потоврите попытку или попробуйте позже" + str(e))

    def delete_task(self):
        try:
            self.client.managers.tasks.delete_task(self.task_id)
            self.parent.switch_page("management_tasks")
        except:
            QMessageBox.critical(self, "Ошибка удаления", "Не удалось удалить задачу")

    def management_task_assignments(self):
        try:
            form = TaskAssignmentsManagementForm(self.task_id)
            form.exec()
            self.parent.switch_page("management_task", params={"task_id": self.task_id})
        except Exception as e:
            QMessageBox.critical(self, "Ошибка управления участниками", "Потоврите попытку или попробуйте позже" + str(e))

    def create_report(self):
        try:
            file = self.client.managers.reports.create_report_by_task(self.task_id)
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", f'Отчёт по задаче {self.task_info.title}', "Excel Files (*.xlsx);;All Files (*)")
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
