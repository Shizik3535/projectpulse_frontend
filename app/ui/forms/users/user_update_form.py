from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QWidget, QComboBox, QMessageBox

from app.api.client import api_client

from app.schemas.users import UserUpdate, UserResponse


class UserUpdateForm(QDialog):
    def __init__(self, user_data: UserResponse, parent=None):
        super().__init__()
        self.parent = parent
        self.client = api_client
        self.user_data = user_data

        self.setWindowTitle("Редактировать пользователя")
        self.setFixedSize(400, 250)

        # Основной контейнер
        main_layout = QVBoxLayout()

        # Создаем макет
        layout = QFormLayout()

        # Имя
        self.first_name = QLineEdit()
        self.first_name.setText(self.user_data.first_name)
        layout.addRow("Имя:", self.first_name)

        # Фамилия
        self.last_name = QLineEdit()
        self.last_name.setText(self.user_data.last_name)
        layout.addRow("Фамилия:", self.last_name)

        # Отчество
        self.patronymic = QLineEdit()
        self.patronymic.setText(self.user_data.patronymic or "")
        layout.addRow("Отчество:", self.patronymic)

        # Должность
        self.position = QComboBox()
        layout.addRow("Должность:", self.position)

        # Роль
        self.role = QComboBox()
        layout.addRow("Роль:", self.role)

        # Загрузка ролей
        self.get_roles()

        # Сохранить кнопка
        self.edit_button = QPushButton("Редактировать")

        # Привязываем событие кнопки со слотом
        self.edit_button.clicked.connect(self.edit_user)

        # Добавляем макет к окну
        main_layout.addLayout(layout)
        main_layout.addWidget(self.edit_button)

        # Устанавливаем макет для окна
        self.setLayout(main_layout)

        # Загрузка должностей
        self.get_positions()

    def get_positions(self):
        try:
            positions = self.client.references.get_positions()
            self.position.addItem("Ничего", None)
            for position in positions:
                self.position.addItem(position.name, position.id)

            # Установка текущей должности
            if self.user_data.position:
                index = self.position.findText(self.user_data.position, Qt.MatchFlag.MatchExactly)
                if index != -1:
                    self.position.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения должностей", f"Не удалось загрузить должности")
            return

    def get_roles(self):
        try:
            roles = self.client.references.get_roles()
            for role in roles:
                self.role.addItem(role.name, role.id)

            # Установка текущей роли
            if self.user_data.role:
                index = self.role.findText(self.user_data.role, Qt.MatchFlag.MatchExactly)
                if index != -1:
                    self.role.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения ролей", f"Не удалось загрузить роли")
            self.close()
            return

    def edit_user(self):
        try:
            first_name = self.first_name.text() or None
            last_name = self.last_name.text() or None
            patronymic = self.patronymic.text() or None
            position_id = self.position.currentData() or None
            role_id = self.role.currentData()
            if not (not first_name or not last_name):
                user = UserUpdate(
                    first_name=first_name,
                    last_name=last_name,
                    patronymic=patronymic,
                    position_id=position_id,
                    role_id=role_id
                )
                self.client.managers.users.update_user(user_id=self.user_data.id, user_data=user)
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка сохранения", "Не все поля заполнены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка создания нового пользователя",
                                 f"Попробуйте ещё раз, если не пытаетесь отредактировать самого себя")
            return
