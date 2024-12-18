from app.schemas.base import MessageResponse
from app.schemas.projects import ProjectResponse, ProjectCreate, ProjectUpdate
from app.schemas.users import UserResponse
from app.schemas.tasks import TaskResponse


class ProjectAPI:
    def __init__(self, client):
        self.client = client

    def get_projects(self) -> list[ProjectResponse]:
        """Получение списка проектов"""
        response = self.client.request(
            method="GET",
            endpoint="/manager/projects"
        )

        if "error" in response:
            raise Exception("Ошибка получения проектов")

        return [ProjectResponse(**project) for project in response['data']]

    def get_project(self, project_id) -> ProjectResponse:
        """Получение проекта по ID"""
        response = self.client.request(
            method="GET",
            endpoint=f"/manager/projects/{project_id}"
        )

        if "error" in response:
            raise Exception("Ошибка получения проекта")

        return ProjectResponse(**response['data'])

    def create_project(self, project_data: ProjectCreate) -> MessageResponse:
        """Создание нового проекта"""
        response = self.client.request(
            method="POST",
            endpoint=f"/manager/projects",
            json=project_data.dict(),
        )

        if "error" in response:
            raise Exception("Ошибка создания проекта")

        return MessageResponse(**response['data'])

    def delete_project(self, project_id: int):
        """Удаление проекта"""
        response = self.client.request(
            method="DELETE",
            endpoint=f"/manager/projects/{project_id}"
        )

        if "error" in response:
            raise Exception("Ошибка удаления проекта")

        return MessageResponse(**response['data'])

    def update_project(self, project_id, project_data: ProjectUpdate) -> MessageResponse:
        """Обновление проекта"""
        response = self.client.request(
            method="PUT",
            endpoint=f"/manager/projects/{project_id}",
            json=project_data.dict(),
        )

        if "error" in response:
            raise Exception("Ошибка обновления проекта")

        return MessageResponse(**response['data'])

    def get_project_members(self, project_id: int) -> list[UserResponse]:
        """Получение списка сотрудников на проекте"""
        response = self.client.request(
            method="GET",
            endpoint=f"/manager/projects/{project_id}/members"
        )

        if "error" in response:
            raise Exception("Ошибка получения участников проекта")

        return [UserResponse(**user) for user in response['data']]

    def add_project_member(self, project_id: int, user_id: int) -> MessageResponse:
        """Назначение сотрудника на проект"""
        response = self.client.request(
            method="POST",
            endpoint=f"/manager/projects/{project_id}/members",
            params={"user_id": user_id}
        )

        if "error" in response:
            raise Exception("Ошибка добавления участника проекта")

        return MessageResponse(**response['data'])

    def remove_project_member(self, project_id: int, user_id: int) -> MessageResponse:
        """Удаление сотрудника с проекта"""
        response = self.client.request(
            method="DELETE",
            endpoint=f"/manager/projects/{project_id}/members/{user_id}",
        )

        if "error" in response:
            raise Exception("Ошибка удаления участника проекта")

        return MessageResponse(**response['data'])

    def get_project_tasks(self, project_id: int) -> list[TaskResponse]:
        """Получение списка задач на проекте"""
        response = self.client.request(
            method="GET",
            endpoint=f"/manager/projects/{project_id}/tasks",
        )

        if "error" in response:
            raise Exception("Ошибка получения задач проекта")

        return [TaskResponse(**task) for task in response['data']]
