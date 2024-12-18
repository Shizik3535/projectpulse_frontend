from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QFrame
from app.schemas.tasks import TaskResponse


class TaskTable(QFrame):
    def __init__(self, tasks: list[TaskResponse], row_double_click_callback=None, parent=None):
        super().__init__(parent)

        self.row_double_click_callback = row_double_click_callback
        self.tasks = tasks

        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        if not self.tasks:
            self._create_empty_label()
        else:
            self._create_table()

    def _create_empty_label(self):
        """Создает метку, если список задач пуст."""
        no_tasks_label = QLabel("Нет задач.", self)
        self.layout.addWidget(no_tasks_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _create_table(self):
        """Создает и настраивает таблицу."""
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Название", "Описание", "Дата начала", "Крайний срок", "Статус", "Приоритет"])

        self._fill_table()

        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self._handle_double_click)

        self.layout.addWidget(self.table)

    def _fill_table(self):
        """Заполняет таблицу данными задач."""
        self.table.setRowCount(len(self.tasks))
        for row, task in enumerate(self.tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task.title))
            self.table.setItem(row, 1, QTableWidgetItem(task.description or "Нет описания"))
            self.table.setItem(row, 2, QTableWidgetItem(self._format_date(task.start_date)))
            self.table.setItem(row, 3, QTableWidgetItem(self._format_date(task.due_date)))
            self.table.setItem(row, 4, QTableWidgetItem(task.status))
            self.table.setItem(row, 5, QTableWidgetItem(task.priority))

    @staticmethod
    def _format_date(date):
        """Форматирует дату в строку."""
        return date.strftime("%d-%m-%Y") if date else "Не указана"

    def _handle_double_click(self, index):
        """Обрабатывает двойное нажатие на строку таблицы."""
        if self.row_double_click_callback:
            task_id = self._get_task_id(index.row())
            if task_id:
                self.row_double_click_callback(task_id)

    def _get_task_id(self, row):
        """Возвращает ID задачи для строки."""
        if 0 <= row < len(self.tasks):
            return self.tasks[row].id
        return None
