from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QWidget, QComboBox, QMessageBox

from app.api.client import api_client

from app.schemas.users import UserCreate


class UserCreateForm(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.client = api_client

        self.setWindowTitle("Добавить пользователя")
        self.setFixedSize(400, 250)

        # Основной контейнер
        main_layout = QVBoxLayout()

        # Создаем макет
        layout = QFormLayout()

        # Логин
        self.username = QLineEdit()
        layout.addRow("Логин:", self.username)

        # Пароль
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Пароль:", self.password)

        # Имя
        self.first_name = QLineEdit()
        layout.addRow("Имя:", self.first_name)

        # Фамилия
        self.last_name = QLineEdit()
        layout.addRow("Фамилия:", self.last_name)

        # Отчество
        self.patronymic = QLineEdit()
        layout.addRow("Отчество:", self.patronymic)

        # Должность
        self.position = QComboBox()
        layout.addRow("Должность:", self.position)

        # Сохранить кнопка
        self.save_button = QPushButton("Сохранить")

        # Привязываем событие кнопки со слотом
        self.save_button.clicked.connect(self.save_user)

        # Добавляем макет к окну
        main_layout.addLayout(layout)
        main_layout.addWidget(self.save_button)

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
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения должностей", f"Не удалось загрузить должности")
            return

    def save_user(self):
        try:
            username = self.username.text() or None
            password = self.password.text() or None
            first_name = self.first_name.text() or None
            last_name = self.last_name.text() or None
            patronymic = self.patronymic.text() or None
            position_id = self.position.currentData() or None
            if not (not username or not password or not first_name or not last_name):
                user = UserCreate(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    patronymic=patronymic,
                    position_id=position_id
                )
                self.client.managers.users.create_user(user)
                self.parent.parent.switch_page("management_users")
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка сохранения", "Не все поля заполнены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка создания нового пользователя",
                                 f"Попробуйте ещё раз или попробуйте поменять логин")
            return
