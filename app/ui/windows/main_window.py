from PyQt6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import Qt
import sys

from app.api.client import api_client
from app.core.settings import app_settings

from app.ui.components.sidebar import SideBar
from app.ui.components.statusbar import StatusBar

from app.ui.pages.home_page import HomePage
from app.ui.pages.settings_page import SettingsPage
from app.ui.pages.tasks.tasks_page import TasksPage
from app.ui.pages.tasks.task_page import TaskPage
from app.ui.pages.projects.projects_page import ProjectsPage
from app.ui.pages.projects.project_page import ProjectPage

from app.ui.pages.management.management_page import ManagementPage
from app.ui.pages.management.users.management_users_page import UsersManagementPage
from app.ui.pages.management.users.management_user_page import UserManagementPage
from app.ui.pages.management.tasks.management_tasks_page import TasksManagementPage
from app.ui.pages.management.tasks.management_task_page import TaskManagementPage
from app.ui.pages.management.projects.management_projects_page import ProjectsManagementPage
from app.ui.pages.management.projects.management_project_page import ProjectManagementPage



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ProjectPulse")
        self.setMinimumSize(1280, 720)
        self.current_page = None

        # Объект клиента
        self.client = api_client

        # Получение данных пользователя
        try:
            self.user_data = self.client.auth.get_user_info()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", f"{str(e)}")
            app_settings.remove("token")
            sys.exit(1)

        self.setup_ui()

    def setup_ui(self):
        # Главный контент
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Главный контейнер
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_widget.setLayout(self.main_layout)

        # Боковое меню
        self.sidebar = SideBar(self.user_data.role, self)

        # Основной контент
        self.content_widget = QWidget()

        # Конетейнер для основгого контента
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_widget.setLayout(self.content_layout)

        # Строка состояния
        self.statusbar = StatusBar()

        # Основная страница
        self.page_stack = QStackedWidget(self.content_widget)

        # Добавление компонентов в основной контент
        self.content_layout.addWidget(self.statusbar)
        self.content_layout.addWidget(self.page_stack)

        # Добавление компонентов в основной контейнер
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_widget)

        self.page_registry = {
            "home": HomePage,
            "settings": SettingsPage,
            "tasks": TasksPage,
            "task": TaskPage,
            "projects": ProjectsPage,
            "project": ProjectPage,
            "management": ManagementPage,
            "management_users": UsersManagementPage,
            "management_user": UserManagementPage,
            "management_tasks": TasksManagementPage,
            "management_task": TaskManagementPage,
            "management_projects": ProjectsManagementPage,
            "management_project": ProjectManagementPage,
        }

        self.switch_page("home")

    def switch_page(self, page_name, params=None):
        try:
            # Получаем или создаем новую страницу
            page_class = self.page_registry.get(page_name)
            if not page_class:
                raise ValueError(f"Неизвестная страница: {page_name}")

            # Создаем новую страницу
            page = page_class(params=params, parent=self)

            # Удаляем старую страницу, если она есть
            if self.page_stack.count() > 0:
                old_page = self.page_stack.widget(0)
                self.page_stack.removeWidget(old_page)
                old_page.deleteLater()  # Освобождаем память

            # Переключаемся на новую страницу
            self.page_stack.addWidget(page)
            self.page_stack.setCurrentWidget(page)

            # Обновляем текущую страницу
            self.current_page = page
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"При переключении страницы: {str(e)}")
