import sys
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

from app.api.client import api_client
from app.core.settings import app_settings

from app.ui.windows.login_window import LoginWindow
from app.ui.windows.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Настройки приложения
    settings = app_settings

    # Получение названия темы и применение её к приложению
    theme = settings.value("theme")
    apply_stylesheet(app, f"{theme}.xml")

    client = api_client

    # Проверка на наличие токена в авторизации
    if settings.contains("token"):
        client.set_token(settings.value("token"))
        window = MainWindow()
    else:
        window = LoginWindow()

    # Запуск приложения
    window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
