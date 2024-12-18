from app.schemas.users import UserResponse, UserCreate, UserUpdate
from app.schemas.projects import ProjectResponse
from app.schemas.tasks import TaskResponseWithProject
from app.schemas.base import MessageResponse


class UserAPI:
    def __init__(self, client):
        self.client = client

    def get_users(self) -> list[UserResponse]:
        """Получение списка всех пользователей"""
        response = self.client.request(
            method='GET',
            endpoint='/manager/users'
        )

        if "error" in response:
            raise Exception("Ошибка получения пользователей")

        return [UserResponse(**user) for user in response["data"]]

    def get_user(self, user_id: int) -> UserResponse:
        """Получение информации о конкретном пользователе"""
        response = self.client.request(
            method='GET',
            endpoint=f'/manager/users/{user_id}'
        )

        if "error" in response:
            raise Exception("Ошибка получения пользователя")

        return UserResponse(**response["data"])

    def create_user(self, user_data: UserCreate) -> MessageResponse:
        """Создание нового пользователя"""
        response = self.client.request(
            method='POST',
            endpoint='/manager/users',
            json=user_data.dict()
        )

        if "error" in response:
            raise Exception("Ошибка создания пользователя")

        return MessageResponse(**response["data"])

    def update_user(self, user_id: int, user_data: UserUpdate) -> MessageResponse:
        """Изменение информации о пользователе"""
        response = self.client.request(
            method='PUT',
            endpoint=f'/manager/users/{user_id}',
            json=user_data.dict()
        )

        if "error" in response:
            raise Exception("Ошибка обновления пользователя")

        return MessageResponse(**response["data"])

    def delete_user(self, user_id: int) -> MessageResponse:
        """Удаление пользователя"""
        response = self.client.request(
            method='DELETE',
            endpoint=f'/manager/users/{user_id}'
        )

        if "error" in response:
            raise Exception("Ошибка удаления пользователей")

        return MessageResponse(**response["data"])

    def get_user_tasks(self, user_id: int) -> list[TaskResponseWithProject]:
        """Получение списка задач конкретного пользователя"""
        response = self.client.request(
            method='GET',
            endpoint=f'/manager/users/{user_id}/tasks'
        )

        if "error" in response:
            raise Exception("Ошибка получения задач пользователя")

        return [TaskResponseWithProject(**task) for task in response["data"]]

    def get_user_projects(self, user_id: int) -> list[ProjectResponse]:
        """Получение списка проектов конкретного пользователя"""
        response = self.client.request(
            method='GET',
            endpoint=f'/manager/users/{user_id}/projects'
        )

        if "error" in response:
            raise Exception("Ошибка получения проектов пользователя")

        return [ProjectResponse(**project) for project in response["data"]]
