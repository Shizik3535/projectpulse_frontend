from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QFrame
from app.schemas.tasks import TaskResponseWithProject


class TaskTableWithProject(QFrame):
    def __init__(
            self,
            tasks: list[TaskResponseWithProject],
            row_double_click_callback=None,
            project_double_click_callback=None,
            parent=None
    ):
        super().__init__(parent)

        self.row_double_click_callback = row_double_click_callback
        self.project_double_click_callback = project_double_click_callback
        self.tasks = tasks

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._initialize_ui()

    def _initialize_ui(self):
        """Инициализация пользовательского интерфейса."""
        if not self.tasks:
            self._create_empty_label()
        else:
            self._create_table()

    def _create_empty_label(self):
        """Создает метку, если нет задач."""
        self.no_projects_label = QLabel("Нет задач.", self)
        self.layout.addWidget(self.no_projects_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _create_table(self):
        """Создает и настраивает таблицу."""
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Название", "Описание", "Дата начала", "Крайний срок", "Статус", "Приоритет", "Проект"])

        self._fill_table()

        self._configure_table()

        self.layout.addWidget(self.table)

    def _configure_table(self):
        """Настройка таблицы."""
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self._handle_double_click)

    def _fill_table(self):
        """Заполняет таблицу данными задач с проектами."""
        self.table.setRowCount(len(self.tasks))
        for row, task in enumerate(self.tasks):
            self._add_task_row(row, task)

    def _add_task_row(self, row, task):
        """Добавляет строку с задачей в таблицу."""
        self.table.setItem(row, 0, QTableWidgetItem(task.title))
        self.table.setItem(row, 1, QTableWidgetItem(self._get_description(task)))
        self.table.setItem(row, 2, QTableWidgetItem(self._format_date(task.start_date)))
        self.table.setItem(row, 3, QTableWidgetItem(self._format_date(task.due_date)))
        self.table.setItem(row, 4, QTableWidgetItem(task.status))
        self.table.setItem(row, 5, QTableWidgetItem(task.priority))
        self.table.setItem(row, 6, QTableWidgetItem(self._get_project_title(task)))

    @staticmethod
    def _get_description(task):
        """Возвращает описание задачи или сообщение о его отсутствии."""
        return task.description if task.description else "Нет описания"

    @staticmethod
    def _format_date(date):
        """Форматирует дату в строку."""
        return date.strftime("%d-%m-%Y") if date else "Не указана"

    @staticmethod
    def _get_project_title(task):
        """Возвращает название проекта задачи или сообщение о его отсутствии."""
        return task.project.title if task.project else "Нет проекта"

    def _handle_double_click(self, index):
        """Обработчик двойного нажатия на строку таблицы."""
        if self.row_double_click_callback:
            row = index.row()
            column = index.column()

            if column == 6 and self.project_double_click_callback:
                self._handle_project_double_click(row)
            elif self.row_double_click_callback:
                self._handle_task_double_click(row)

    def _handle_project_double_click(self, row):
        """Обрабатывает двойной клик по проекту."""
        project_id = self.get_project_id(row)
        if project_id:
            self.project_double_click_callback(project_id)

    def _handle_task_double_click(self, row):
        """Обрабатывает двойной клик по задаче."""
        task_id = self.get_task_id(row)
        if task_id:
            self.row_double_click_callback(task_id)

    def get_task_id(self, row):
        """Возвращает ID задачи для строки."""
        if 0 <= row < len(self.tasks):
            return self.tasks[row].id
        return None

    def get_project_id(self, row):
        """Возвращает ID проекта для строки задачи."""
        if 0 <= row < len(self.tasks) and self.tasks[row].project:
            return self.tasks[row].project.id
        return None
