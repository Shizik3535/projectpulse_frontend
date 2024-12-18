from app.schemas.base import MessageResponse
from app.schemas.tasks import TaskResponseWithProject, TaskCreate, TaskUpdate
from app.schemas.users import UserResponse


class TaskAPI:
    def __init__(self, client):
        self.client = client

    def get_tasks(self) -> list[TaskResponseWithProject]:
        """Получение списка всех задач"""
        response = self.client.request(
            method="GET",
            endpoint="/manager/tasks"
        )

        if "error" in response:
            raise Exception("Ошибка получения задач")

        return [TaskResponseWithProject(**task) for task in response['data']]

    def get_task(self, task_id: int) -> TaskResponseWithProject:
        """Получение информации о конкретной задаче"""
        response = self.client.request(
            method="GET",
            endpoint=f"/manager/tasks/{task_id}"
        )

        if "error" in response:
            raise Exception("Ошибка получения задачи")

        return TaskResponseWithProject(**response['data'])

    def create_task(self, task_data: TaskCreate) -> MessageResponse:
        """Создание новой задачи"""
        response = self.client.request(
            method="POST",
            endpoint="/manager/tasks",
            json=task_data.dict(),
        )

        if "error" in response:
            raise Exception(response['error'])

        return MessageResponse(**response['data'])

    def delete_task(self, task_id: int) -> MessageResponse:
        """Удаление задачи"""
        response = self.client.request(
            method="DELETE",
            endpoint=f"/manager/tasks/{task_id}"
        )

        if "error" in response:
            raise Exception("Ошибка удаления задачи")

        return MessageResponse(**response['data'])

    def update_task(self, task_id: int, task_data: TaskUpdate) -> MessageResponse:
        """Изменение информации о задаче"""
        response = self.client.request(
            method="PUT",
            endpoint=f"/manager/tasks/{task_id}",
            json=task_data.dict(),
        )

        if "error" in response:
            raise Exception("Ошибка обновления задачи")

        return MessageResponse(**response['data'])

    def get_task_assignments(self, task_id: int) -> list[UserResponse]:
        """Получение списка назначенных сотрудников на текущую задачу"""
        response = self.client.request(
            method="GET",
            endpoint=f"/manager/tasks/{task_id}/assignments"
        )

        if "error" in response:
            raise Exception("Ошибка получения назначенных сотрудников")

        return [UserResponse(**user) for user in response['data']]

    def add_task_assignments(self, task_id: int, user_id: int):
        """Добавление сотрудника на текущую задачу"""
        response = self.client.request(
            method="POST",
            endpoint=f"/manager/tasks/{task_id}/assignments/",
            params={"user_id": user_id}
        )

        if "error" in response:
            raise Exception("Ошибка назначения сотрудника")

        return MessageResponse(**response['data'])

    def remove_task_assignment(self, task_id: int, user_id: int):
        """Удаление сотрудника из текущей задачи"""
        response = self.client.request(
            method="DELETE",
            endpoint=f"/manager/tasks/{task_id}/assignments/{user_id}"
        )

        if "error" in response:
            raise Exception("Ошибка удаления назначения")

        return MessageResponse(**response['data'])
