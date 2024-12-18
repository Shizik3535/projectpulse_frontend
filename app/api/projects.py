from app.schemas.users import UserResponse
from app.schemas.projects import ProjectResponse
from app.schemas.tasks import TaskResponse


class ProjectAPI:
    def __init__(self, client):
        self.client = client

    def get_user_projects(self) -> list[ProjectResponse]:
        """Получение списка проектов текущего пользователя"""
        response = self.client.request(
            method="GET",
            endpoint='/projects/',
        )

        if "error" in response:
            raise Exception("Ошибка получения проектов")

        return [ProjectResponse(**project) for project in response["data"]]

    def get_project(self, project_id: int):
        """Получение проекта по его идентификатору"""
        response = self.client.request(
            method="GET",
            endpoint=f'/projects/{project_id}',
        )

        if "error" in response:
            raise Exception("Ошибка получения проекта")

        return ProjectResponse(**response["data"])

    def get_project_tasks(self, project_id: int) -> list[TaskResponse]:
        """Получение списка задач проекта"""
        response = self.client.request(
            method="GET",
            endpoint=f'/projects/{project_id}/tasks',
        )

        if "error" in response:
            raise Exception("Ошибка получения задач проекта")

        return [TaskResponse(**task) for task in response["data"]]

    def get_project_members(self, project_id: int) -> list[UserResponse]:
        """Получение списка участников проекта"""
        response = self.client.request(
            method="GET",
            endpoint=f'/projects/{project_id}/members',
        )

        if "error" in response:
            raise Exception("Ошибка получения участников проекта")

        return [UserResponse(**user) for user in response["data"]]
