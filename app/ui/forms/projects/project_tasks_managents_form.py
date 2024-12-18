from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QHeaderView, QMessageBox

from app.api.client import api_client
from app.schemas.tasks import TaskResponse, TaskUpdate


class ProjectTaskManagementForm(QDialog):
    def __init__(self, project_id: int, parent=None):
        super().__init__()
        self.setWindowTitle("Управление задачами проекта")
        self.resize(1200, 500)
        self.project_id = project_id
        self.parent = parent
        self.client = api_client

        # Получаем данные задач и задач в проекте
        self.all_tasks = self.get_all_tasks()
        self.used_ids = {task.id for task in self.get_project_tasks()}

        # Получаем статусы и приоритеты
        self.statuses = self.get_task_statuses()
        self.priorities = self.get_task_priorities()

        # Основной layout
        main_layout = QHBoxLayout(self)

        # Левая таблица: Задачи проекта
        self.project_tasks_table = QTableWidget()
        self.project_tasks_table.setColumnCount(4)
        self.project_tasks_table.verticalHeader().setVisible(False)
        self.project_tasks_table.resizeColumnsToContents()
        self.project_tasks_table.resizeRowsToContents()
        self.project_tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.project_tasks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.project_tasks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.project_tasks_table.setHorizontalHeaderLabels([
            "Заголовок", "Описание", "Статус", "Удалить"
        ])
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(QLabel("Задачи проекта"))
        self.left_layout.addWidget(self.project_tasks_table)

        # Правая таблица: Доступные задачи
        self.available_tasks_table = QTableWidget()
        self.available_tasks_table.setColumnCount(4)
        self.available_tasks_table.verticalHeader().setVisible(False)
        self.available_tasks_table.resizeColumnsToContents()
        self.available_tasks_table.resizeRowsToContents()
        self.available_tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.available_tasks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.available_tasks_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.available_tasks_table.setHorizontalHeaderLabels([
            "Заголовок", "Описание", "Статус", "Добавить"
        ])
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(QLabel("Доступные задачи"))
        self.right_layout.addWidget(self.available_tasks_table)

        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_layout)

        # Первоначальное заполнение таблиц
        self.refresh_tables()

    def get_task_statuses(self):
        """Получает список статусов задач"""
        try:
            return {status.name: status.id for status in self.client.references.get_task_statuses()}
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения статусов", f"Не удалось загрузить статусы задач: {str(e)}")
            return {}

    def get_task_priorities(self):
        """Получает список приоритетов задач"""
        try:
            return {priority.name: priority.id for priority in self.client.references.get_task_priorities()}
        except Exception as e:
            QMessageBox.critical(self, "Ошибка получения приоритетов",
                                 f"Не удалось загрузить приоритеты задач: {str(e)}")
            return {}

    def populate_table(self, table: QTableWidget, tasks: list[TaskResponse], is_participant: bool):
        """Заполняет таблицу данными и добавляет кнопки"""
        table.setRowCount(0)
        for row, task in enumerate(tasks):
            table.insertRow(row)
            title_item = QTableWidgetItem(task.title)
            description_item = QTableWidgetItem(task.description if task.description else "Не указано")

            # Добавляем подсказку для названия
            title_item.setToolTip(task.title)

            # Добавляем подсказку для описания
            description_item.setToolTip(task.description if task.description else "Нет описания")

            table.setItem(row, 0, title_item)
            table.setItem(row, 1, description_item)
            table.setItem(row, 2, QTableWidgetItem(task.status))

            # Кнопка добавить/удалить
            button = QPushButton("Удалить" if is_participant else "Добавить")
            button.clicked.connect(
                lambda _, t=task, p=is_participant: self.handle_button_click(t, p)
            )
            table.setCellWidget(row, 3, button)  # Последняя колонка - кнопка

    def refresh_tables(self):
        """Обновляет обе таблицы с использованием локального множества used_ids"""
        project_tasks = [task for task in self.all_tasks if task.id in self.used_ids]
        available_tasks = [task for task in self.all_tasks if task.id not in self.used_ids]

        self.populate_table(self.project_tasks_table, project_tasks, is_participant=True)
        self.populate_table(self.available_tasks_table, available_tasks, is_participant=False)

    def handle_button_click(self, task: TaskResponse, is_participant: bool):
        """Обрабатывает нажатие кнопок 'Добавить' и 'Удалить'"""
        if is_participant:
            try:
                self.used_ids.remove(task.id)
                status_id = self.statuses.get(task.status, 1)  # Получаем status_id по названию
                priority_id = self.priorities.get(task.priority, 1)  # Получаем priority_id по названию
                self.client.managers.tasks.update_task(task_id=task.id, task_data=TaskUpdate(
                    title=task.title,
                    description=task.description,
                    start_date=str(task.start_date) if task.start_date else None,
                    due_date=str(task.due_date) if task.due_date else None,
                    status_id=status_id,
                    priority_id=priority_id,
                    project_id=None
                ))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка удаления", f"Попробуйте снова или повторите позже: {str(e)}")
        else:
            try:
                self.used_ids.add(task.id)
                status_id = self.statuses.get(task.status, 1)  # Получаем status_id по названию
                priority_id = self.priorities.get(task.priority, 1)  # Получаем priority_id по названию
                self.client.managers.tasks.update_task(task_id=task.id, task_data=TaskUpdate(
                    title=task.title,
                    description=task.description,
                    start_date=str(task.start_date) if task.start_date else None,
                    due_date=str(task.due_date) if task.due_date else None,
                    status_id=status_id,
                    priority_id=priority_id,
                    project_id=self.project_id
                ))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка добавления", f"Попробуйте снова или повторите позже: {str(e)}")

        # Обновляем таблицы
        self.refresh_tables()

    def get_all_tasks(self) -> list[TaskResponse]:
        """Получает список всех задач"""
        try:
            return self.client.managers.tasks.get_tasks()
        except Exception as e:
            return []

    def get_project_tasks(self) -> list[TaskResponse]:
        """Получает список задач проекта"""
        try:
            return self.client.managers.projects.get_project_tasks(self.project_id)
        except Exception as e:
            return []
