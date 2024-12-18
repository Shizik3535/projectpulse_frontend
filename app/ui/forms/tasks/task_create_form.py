from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QMessageBox, QDateEdit, QHBoxLayout
)
from PyQt6.QtCore import QDate

from app.api.client import api_client

from app.schemas.tasks import TaskCreate


class TaskCreateForm(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.client = api_client

        self.setWindowTitle("Добавить задачу")
        self.setFixedSize(400, 350)

        # Основной контейнер
        main_layout = QVBoxLayout()

        # Создаем макет
        layout = QFormLayout()

        # Название
        self.title = QLineEdit()
        layout.addRow("Название:", self.title)

        # Описание
        self.description = QLineEdit()
        layout.addRow("Описание:", self.description)

        # Дата начала
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())

        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(self.start_date)
        layout.addRow("Дата начала:", start_date_layout)

        # Дата окончания
        self.due_date = QDateEdit(calendarPopup=True)
        self.due_date.setDate(QDate.currentDate())

        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(self.due_date)
        layout.addRow("Дата окончания:", due_date_layout)

        # Сохранить кнопка
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_task)

        # Добавляем макет к окну
        main_layout.addLayout(layout)
        main_layout.addWidget(self.save_button)

        # Устанавливаем макет для окна
        self.setLayout(main_layout)

    def save_task(self):
        try:
            title = self.title.text().strip()
            description = self.description.text().strip()
            start_date = self.start_date.date().toPyDate()
            due_date = self.due_date.date().toPyDate()

            if not title:
                QMessageBox.critical(self, "Ошибка сохранения", "Название задачи обязательно")
                return

            task = TaskCreate(
                title=title,
                description=description,
                start_date=start_date.strftime('%Y-%m-%d'),
                due_date=due_date.strftime('%Y-%m-%d'),
            )
            self.client.managers.tasks.create_task(task)
            self.parent.parent.switch_page("management_tasks")
            self.close()
        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка создания новой задачи",
                f"Попробуйте снова или через некоторое время. Ошибка: {str(e)}"
            )
