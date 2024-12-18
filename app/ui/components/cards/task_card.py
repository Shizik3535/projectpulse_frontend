from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

from app.api.client import api_client

from app.schemas.tasks import TaskResponse


class TaskCard(QFrame):
    def __init__(self, task: TaskResponse, manager_mode: bool):
        super().__init__()
        self.task = task
        self.manager_mode = manager_mode
        self.client = api_client

        # Основной layout карточки
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Заголовок задачи
        self.title_label = QLabel(f"Название: {self.task.title}")
        self.layout.addWidget(self.title_label)

        # Описание задачи
        self.description_label = QLabel(f'Описание: {self.task.description or "Отсутствует"}')
        self.description_label.setWordWrap(True)
        self.layout.addWidget(self.description_label)

        # Даты задачи
        self.dates_label = QLabel(self._format_dates())
        self.layout.addWidget(self.dates_label)

        # Приоритет задачи
        self.priority_label = QLabel(f"Приоритет: {self.task.priority}")
        self.layout.addWidget(self.priority_label)

        # Статус задачи
        self.status_label = QLabel(f"Статус: {self.task.status}")
        self.layout.addWidget(self.status_label)

        if not self.manager_mode:
            # Кнопки управления статусом
            self.button_layout = QHBoxLayout()
            self.layout.addLayout(self.button_layout)

            self.planned_button = QPushButton("Запланирована")
            self.planned_button.clicked.connect(self.set_planned_status)
            self.button_layout.addWidget(self.planned_button)

            self.in_progress_button = QPushButton("В работе")
            self.in_progress_button.clicked.connect(self.set_in_progress_status)
            self.button_layout.addWidget(self.in_progress_button)

            self.completed_button = QPushButton("Завершена")
            self.completed_button.clicked.connect(self.set_completed_status)
            self.button_layout.addWidget(self.completed_button)

    def _format_dates(self):
        start_date = self.task.start_date.strftime("%d.%m.%Y") if self.task.start_date else "Не указана"
        due_date = self.task.due_date.strftime("%d.%m.%Y") if self.task.due_date else "Не указана"
        return f"Начало: {start_date} | Срок: {due_date}"

    def set_planned_status(self):
        self.task.status = "Запланирована"
        self.client.tasks.change_task_status(self.task.id, 1)
        self.update_status_label()

    def set_in_progress_status(self):
        self.client.tasks.change_task_status(self.task.id, 2)
        self.task.status = "В работе"
        self.update_status_label()

    def set_completed_status(self):
        self.client.tasks.change_task_status(self.task.id, 3)
        self.task.status = "Завершена"
        self.update_status_label()

    def update_status_label(self):
        self.status_label.setText(f"Статус: {self.task.status}")
