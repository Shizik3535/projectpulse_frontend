from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QWidget, QComboBox, QMessageBox, QDateEdit, QHBoxLayout

from app.api.client import api_client

from app.schemas.tasks import TaskUpdate, TaskResponseWithProject


class TaskUpdateForm(QDialog):
    def __init__(self, task_data: TaskResponseWithProject, parent=None):
        super().__init__()
        self.parent = parent
        self.client = api_client
        self.task_data = task_data

        self.setWindowTitle("Редактировать задачу")
        self.setFixedSize(400, 400)

        # Основной контейнер
        main_layout = QVBoxLayout()

        # Создаем макет
        layout = QFormLayout()

        # Название задачи
        self.title = QLineEdit()
        self.title.setText(self.task_data.title)
        layout.addRow("Название задачи:", self.title)

        # Описание задачи
        self.description = QLineEdit()
        self.description.setText(self.task_data.description or "")
        layout.addRow("Описание задачи:", self.description)

        # Дата начала задачи
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(self.task_data.start_date)
        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(self.start_date)
        layout.addRow("Дата начала:", start_date_layout)

        # Дата окончания задачи
        self.due_date = QDateEdit(calendarPopup=True)
        self.due_date.setDate(self.task_data.due_date)
        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(self.due_date)
        layout.addRow("Дата окончания:", due_date_layout)

        # Статус задачи
        self.status = QComboBox()
        layout.addRow("Статус задачи:", self.status)

        # Приоритет задачи
        self.priority = QComboBox()
        layout.addRow("Приоритет задачи:", self.priority)

        # Загрузка статусов и приоритетов
        self.get_task_statuses()
        self.get_task_priorities()

        # Кнопка для сохранения изменений
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_task)

        # Добавляем макет к окну
        main_layout.addLayout(layout)
        main_layout.addWidget(self.save_button)

        # Устанавливаем макет для окна
        self.setLayout(main_layout)

    def get_task_statuses(self):
        try:
            statuses = self.client.references.get_task_statuses()
            for status in statuses:
                self.status.addItem(status.name, status.id)

            # Установка текущего статуса
            if self.task_data.status:
                index = self.status.findText(self.task_data.status, Qt.MatchFlag.MatchExactly)
                if index != -1:
                    self.status.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения статусов", "Не удалось загрузить статусы задач: " + str(e))
            return

    def get_task_priorities(self):
        try:
            priorities = self.client.references.get_task_priorities()
            for priority in priorities:
                self.priority.addItem(priority.name, priority.id)

            # Установка текущего приоритета
            if self.task_data.priority:
                index = self.priority.findText(self.task_data.priority, Qt.MatchFlag.MatchExactly)
                if index != -1:
                    self.priority.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения приоритетов", "Не удалось загрузить приоритеты задач" + str(e))
            return

    def save_task(self):
        try:
            title = self.title.text().strip()
            description = self.description.text().strip()
            start_date = self.start_date.date().toPyDate()
            due_date = self.due_date.date().toPyDate()
            status_id = self.status.currentData()
            priority_id = self.priority.currentData()

            if not title or not status_id or not priority_id:
                QMessageBox.critical(self, "Ошибка сохранения", "Не все обязательные поля заполнены")
                return

            task = TaskUpdate(
                title=title,
                description=description,
                start_date=start_date.strftime('%Y-%m-%d'),
                due_date=due_date.strftime('%Y-%m-%d'),
                status_id=status_id,
                priority_id=priority_id,
                project_id=self.task_data.project.id if self.task_data.project else None
            )

            # Здесь предполагается, что `update_task` реализует API для обновления задачи
            self.client.managers.tasks.update_task(task_id=self.task_data.id, task_data=task)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка редактирования задачи", f"Попробуйте ещё раз, ошибка: {str(e)}")
            return
