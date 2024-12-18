from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QFrame
from app.schemas.projects import ProjectResponse


class ProjectTable(QFrame):
    def __init__(self, projects: list[ProjectResponse], row_double_click_callback=None, parent=None):
        super().__init__(parent)

        self.row_double_click_callback = row_double_click_callback
        self.projects = projects

        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        if not self.projects:
            self._create_empty_label()
        else:
            self._create_table()

    def _create_empty_label(self):
        """Создает метку, если список проектов пуст."""
        no_projects_label = QLabel("Нет проектов.", self)
        self.layout.addWidget(no_projects_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _create_table(self):
        """Создает и настраивает таблицу."""
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Название", "Описание", "Дата начала", "Крайний срок", "Статус"])

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
        """Заполняет таблицу данными проектов."""
        self.table.setRowCount(len(self.projects))
        for row, project in enumerate(self.projects):
            self.table.setItem(row, 0, QTableWidgetItem(project.title))
            self.table.setItem(row, 1, QTableWidgetItem(project.description or "Нет описания"))
            self.table.setItem(row, 2, QTableWidgetItem(self._format_date(project.start_date)))
            self.table.setItem(row, 3, QTableWidgetItem(self._format_date(project.due_date)))
            self.table.setItem(row, 4, QTableWidgetItem(project.status))

    @staticmethod
    def _format_date(date):
        """Форматирует дату в строку."""
        return date.strftime("%d-%m-%Y") if date else "Не указана"

    def _handle_double_click(self, index):
        """Обрабатывает двойное нажатие на строку таблицы."""
        if self.row_double_click_callback:
            project_id = self._get_project_id(index.row())
            if project_id:
                self.row_double_click_callback(project_id)

    def _get_project_id(self, row):
        """Возвращает ID проекта для строки."""
        if 0 <= row < len(self.projects):
            return self.projects[row].id
        return None
