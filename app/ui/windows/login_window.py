from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

from app.ui.windows.main_window import MainWindow

from app.api.client import api_client
from app.core.settings import app_settings


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setFixedSize(300, 150)
        self.setup_ui()
        self.client = api_client

    def setup_ui(self):
        self.login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Зашифрованный ввод пароля
        self.login_button = QPushButton("Войти")

        self.login_button.clicked.connect(self.handle_button_login)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.login_label)
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def handle_button_login(self):
        username = self.login_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.critical(self, "Ошибка авторизации", "Введите логин и пароль")
            return
        try:
            token = self.client.auth.login(username, password)
            app_settings.setValue("token", token.access_token)
            self.window = MainWindow()
            self.window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка авторизации", str(e))
            return
