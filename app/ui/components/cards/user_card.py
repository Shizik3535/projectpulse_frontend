from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.schemas.users import UserResponse


class UserCard(QFrame):
    def __init__(self, user: UserResponse):
        super().__init__()
        self.user = user

        # Основной layout карточки
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Полное имя пользователя
        self.first_name_label = QLabel(f"Имя: {self.user.first_name}")
        self.layout.addWidget(self.first_name_label)
        self.last_name_label = QLabel(f"Фамилия: {self.user.last_name}")
        self.layout.addWidget(self.last_name_label)
        self.patronymic_label = QLabel(f"Отчество: {self.user.patronymic or "Нет"}")
        self.layout.addWidget(self.patronymic_label)

        # Должность пользователя
        self.position_label = QLabel(f"Должность: {self.user.position or "Отсутствует"}")
        self.layout.addWidget(self.position_label)
