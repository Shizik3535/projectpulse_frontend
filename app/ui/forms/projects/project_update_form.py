from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QWidget, QComboBox, QMessageBox, QDateEdit, QHBoxLayout

from app.api.client import api_client

from app.schemas.projects import ProjectResponse, ProjectUpdate


class ProjectUpdateForm(QDialog):
    def __init__(self, project_data: ProjectResponse, parent=None):
        super().__init__()
        self.parent = parent
        self.client = api_client
        self.project_data = project_data
        print(project_data.id)

        self.setWindowTitle("Редактировать проект")
        self.setFixedSize(400, 400)

        # Основной контейнер
        main_layout = QVBoxLayout()

        # Создаем макет
        layout = QFormLayout()

        # Название проекта
        self.title = QLineEdit()
        self.title.setText(self.project_data.title)
        layout.addRow("Название проекта:", self.title)

        # Описание проекта
        self.description = QLineEdit()
        self.description.setText(self.project_data.description or "")
        layout.addRow("Описание проекта:", self.description)

        # Дата начала проекта
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(self.project_data.start_date)
        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(self.start_date)
        layout.addRow("Дата начала:", start_date_layout)

        # Дата окончания проекта
        self.due_date = QDateEdit(calendarPopup=True)
        self.due_date.setDate(self.project_data.due_date)
        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(self.due_date)
        layout.addRow("Дата окончания:", due_date_layout)

        # Статус проекта
        self.status = QComboBox()
        layout.addRow("Статус проекта:", self.status)

        # Загрузка статусов и приоритетов
        self.get_project_statuses()

        # Кнопка для сохранения изменений
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_project)

        # Добавляем макет к окну
        main_layout.addLayout(layout)
        main_layout.addWidget(self.save_button)

        # Устанавливаем макет для окна
        self.setLayout(main_layout)

    def get_project_statuses(self):
        try:
            statuses = self.client.references.get_project_statuses()
            for status in statuses:
                self.status.addItem(status.name, status.id)

            # Установка текущего статуса
            if self.project_data.status:
                index = self.status.findText(self.project_data.status, Qt.MatchFlag.MatchExactly)
                if index != -1:
                    self.status.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения статусов", "Не удалось загрузить статусы задач: " + str(e))
            return

    def save_project(self):
        try:
            title = self.title.text().strip()
            description = self.description.text().strip()
            start_date = self.start_date.date().toPyDate()
            due_date = self.due_date.date().toPyDate()
            status_id = self.status.currentData()

            if not title or not status_id:
                QMessageBox.critical(self, "Ошибка сохранения", "Не все обязательные поля заполнены")
                return

            project = ProjectUpdate(
                title=title,
                description=description,
                start_date=start_date.strftime('%Y-%m-%d'),
                due_date=due_date.strftime('%Y-%m-%d'),
                status_id=status_id,
            )

            # Здесь предполагается, что `update_task` реализует API для обновления задачи
            self.client.managers.projects.update_project(project_id=self.project_data.id, project_data=project)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка редактирования задачи", f"Попробуйте ещё раз, ошибка: {str(e)}")
            return
