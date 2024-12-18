from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.schemas.projects import ProjectResponse


class ProjectCard(QFrame):
    def __init__(self, project: ProjectResponse):
        super().__init__()
        self.project = project

        # Основной layout карточки
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Название проекта
        self.title_label = QLabel(f"Название: {self.project.title}")
        self.layout.addWidget(self.title_label)

        # Описание проекта
        self.description_label = QLabel(f"Описание: {self.project.description or "Описание отсутствует"}")
        self.description_label.setWordWrap(True)
        self.layout.addWidget(self.description_label)

        # Даты проекта
        self.dates_label = QLabel(self._format_dates())
        self.layout.addWidget(self.dates_label)

        # Статус проекта
        self.status_label = QLabel(f"Статус: {self.project.status}")
        self.layout.addWidget(self.status_label)

    def _format_dates(self):
        start_date = self.project.start_date.strftime("%d.%m.%Y") if self.project.start_date else "Не указана"
        due_date = self.project.due_date.strftime("%d.%m.%Y") if self.project.due_date else "Не указана"
        return f"Начало: {start_date} | Срок: {due_date}"
