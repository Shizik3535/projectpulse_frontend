from app.schemas.users import UserResponse
from app.schemas.tasks import TaskResponseWithProject
from app.schemas.base import MessageResponse


class TaskAPI:
    def __init__(self, client):
        self.client = client

    def get_user_tasks(self) -> list[TaskResponseWithProject]:
        """Получение списка задач текущего пользователя"""
        response = self.client.request(
            method="GET",
            endpoint='/tasks/',
        )

        if "error" in response:
            raise Exception("Ошибка получения задач")

        return [TaskResponseWithProject(**task) for task in response["data"]]

    def get_task(self, task_id: int) -> TaskResponseWithProject:
        """Получение информации о конкретной задаче"""
        response = self.client.request(
            method="GET",
            endpoint=f'/tasks/{task_id}',
        )

        if "error" in response:
            raise Exception("Ошибка получения задачи")

        return TaskResponseWithProject(**response["data"])

    def get_task_assignments(self, task_id: int) -> list[UserResponse]:
        """Получение списка назначений на текущую задачу"""
        response = self.client.request(
            method="GET",
            endpoint=f'/tasks/{task_id}/assignments',
        )

        if "error" in response:
            raise Exception("Ошибка получения назначенных сотрудников")

        return [UserResponse(**assignment) for assignment in response["data"]]

    def change_task_status(self, task_id: int, status_id: int) -> MessageResponse:
        """Изменение статуса текущей задачи"""
        response = self.client.request(
            method="PUT",
            endpoint=f'/tasks/{task_id}/status',
            params={"status_id": status_id}
        )

        if "error" in response:
            raise Exception("Ошибка смены статуса задачи")

        return MessageResponse(**response["data"])
