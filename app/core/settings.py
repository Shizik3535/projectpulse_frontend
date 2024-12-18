from PyQt6.QtCore import QSettings


# Создание или чтение настроек приложения
app_settings = QSettings("Damir", "ProjectPulse")

# Проверка на наличие темы в настройках
if not app_settings.contains("theme"):
    app_settings.setValue("theme", "light_blue")
