from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QFrame
from app.schemas.users import UserResponse


class UserTable(QFrame):
    def __init__(self, users: list[UserResponse], row_double_click_callback=None, parent=None):
        super().__init__(parent)
        self.row_double_click_callback = row_double_click_callback
        self.users = users

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        if not users:
            self._display_no_users_message()
            return

        self.table = QTableWidget(self)
        self._setup_table()
        self.fill_table(users)

        self.layout.addWidget(self.table)

    def _display_no_users_message(self):
        """Отображает сообщение, если пользователей нет."""
        label = QLabel("Нет пользователей.", self)
        self.layout.addWidget(label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_table(self):
        """Настроить таблицу."""
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Отчество", "Должность"])
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QTableWidget.
                                        SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.table.doubleClicked.connect(self.handle_double_click)

    def fill_table(self, users):
        """Заполняет таблицу данными пользователей."""
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            self._set_item(row, 0, user.first_name)
            self._set_item(row, 1, user.last_name)
            self._set_item(row, 2, user.patronymic or "Не указано")
            self._set_item(row, 3, user.position or "Не указана")

    def _set_item(self, row, col, text):
        """Устанавливает значение в ячейку таблицы."""
        self.table.setItem(row, col, QTableWidgetItem(text))

    def handle_double_click(self, index):
        """Обработчик двойного нажатия на строку таблицы."""
        if self.row_double_click_callback:
            row = index.row()
            user_id = self.get_user_id(row)
            if user_id and self.row_double_click_callback:
                self.row_double_click_callback(user_id)

    def get_user_id(self, row):
        """Возвращает ID пользователя для строки."""
        if 0 <= row < len(self.users):
            return self.users[row].id
        return None
