from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QHeaderView, QMessageBox

from app.api.client import api_client

from app.schemas.users import UserResponse


class ProjectMemberManagementForm(QDialog):
    def __init__(self, project_id: int, parent=None):
        super().__init__()
        self.setWindowTitle("Управление участниками проекта")
        self.resize(1200, 500)
        self.project_id = project_id
        self.parent = parent
        self.client = api_client

        # Получаем данные пользователей и участников
        self.all_users = self.get_all_users()
        self.used_ids = {user.id for user in self.get_participants()}

        # Основной layout
        main_layout = QHBoxLayout(self)

        # Левая таблица: Участники проекта
        self.participants_table = QTableWidget()
        self.participants_table.setColumnCount(5)
        self.participants_table.verticalHeader().setVisible(False)
        self.participants_table.resizeColumnsToContents()
        self.participants_table.resizeRowsToContents()
        self.participants_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.participants_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.participants_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.participants_table.setHorizontalHeaderLabels([
            "Имя", "Фамилия", "Отчество", "Должность", "Удалить"
        ])
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(QLabel("Участники проекта"))
        self.left_layout.addWidget(self.participants_table)

        # Правая таблица: Доступные пользователи
        self.all_users_table = QTableWidget()
        self.all_users_table.setColumnCount(5)
        self.all_users_table.verticalHeader().setVisible(False)
        self.all_users_table.resizeColumnsToContents()
        self.all_users_table.resizeRowsToContents()
        self.all_users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.all_users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.all_users_table.setHorizontalHeaderLabels([
            "Имя", "Фамилия", "Отчество", "Должность", "Добавить"
        ])
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(QLabel("Доступные пользователи"))
        self.right_layout.addWidget(self.all_users_table)

        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)

        # Первоначальное заполнение таблиц
        self.refresh_tables()

    def populate_table(self, table: QTableWidget, users: list[UserResponse], is_participant: bool):
        """Заполняет таблицу данными и добавляет кнопки"""
        table.setRowCount(0)
        for row, user in enumerate(users):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(user.first_name))
            table.setItem(row, 1, QTableWidgetItem(user.last_name))
            table.setItem(row, 2, QTableWidgetItem(user.patronymic if user.patronymic else "Не указано"))
            table.setItem(row, 3, QTableWidgetItem(user.position if user.position else "Не указана"))
            # Кнопка добавить/удалить
            button = QPushButton("Удалить" if is_participant else "Добавить")
            button.clicked.connect(
                lambda _, u=user, p=is_participant: self.handle_button_click(u, p)
            )
            table.setCellWidget(row, 4, button)  # Последняя колонка - кнопка

    def refresh_tables(self):
        """Обновляет обе таблицы с использованием локального множества used_ids"""
        participants = [user for user in self.all_users if user.id in self.used_ids]
        available_users = [user for user in self.all_users if user.id not in self.used_ids]

        self.populate_table(self.participants_table, participants, is_participant=True)
        self.populate_table(self.all_users_table, available_users, is_participant=False)

    def get_all_users(self) -> list[UserResponse]:
        """Получает список всех пользователей"""
        try:
            return self.client.managers.users.get_users()
        except Exception as e:
            return []

    def get_participants(self) -> list[UserResponse]:
        """Получает список участников проекта"""
        try:
            return self.client.managers.projects.get_project_members(self.project_id)
        except Exception as e:
            return []

    def get_available_users(self) -> list[UserResponse]:
        """Возвращает список пользователей, которые ещё не участвуют в проекте"""
        return [user for user in self.all_users if user.id not in self.used_ids]

    def handle_button_click(self, user: UserResponse, is_participant: bool):
        """Обрабатывает нажатие кнопок 'Добавить' и 'Удалить'"""
        if is_participant:
            try:
                self.used_ids.remove(user.id)
                self.client.managers.projects.remove_project_member(project_id=self.project_id, user_id=user.id)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка удаления", f"Попробуйте снова или повторите позже: {str(e)}")
        else:
            try:
                self.used_ids.add(user.id)
                self.client.managers.projects.add_project_member(project_id=self.project_id, user_id=user.id)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка добавления", f"Попробуйте снова или повторите позже: {str(e)}")

        # Обновляем таблицы
        self.refresh_tables()
