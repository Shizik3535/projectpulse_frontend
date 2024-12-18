from app.schemas.reference import ReferenceResponse


class ReferenceAPI:
    def __init__(self, client):
        self.client = client

    def get_positions(self):
        """Получение списка всех должностей"""
        response = self.client.request(
            method='GET',
            endpoint="/references/positions"
        )

        if "error" in response:
            raise Exception("Ошибка получения должностей в компании")

        return [ReferenceResponse(**position) for position in response["data"]]

    def get_roles(self):
        """Получение списка всех ролей"""
        response = self.client.request(
            method='GET',
            endpoint="/references/roles"
        )

        if "error" in response:
            raise Exception("Ошибка получения ролей в системе")

        return [ReferenceResponse(**role) for role in response["data"]]

    def get_task_statuses(self):
        """Получение списка статусов задач"""
        response = self.client.request(
            method='GET',
            endpoint="/references/task-statuses"
        )

        if "error" in response:
            raise Exception("Ошибка получения статусов задач")

        return [ReferenceResponse(**status) for status in response["data"]]

    def get_task_priorities(self):
        """Получение списка приоритетов задач"""
        response = self.client.request(
            method='GET',
            endpoint="/references/task-priorities"
        )

        if "error" in response:
            raise Exception("Ошибка получения приоритетов задач")

        return [ReferenceResponse(**priority) for priority in response["data"]]

    def get_project_statuses(self):
        """Получение списка статусов проектов"""
        response = self.client.request(
            method='GET',
            endpoint="/references/project-statuses"
        )

        if "error" in response:
            raise Exception("Ошибка получения статусов проектов")

        return [ReferenceResponse(**status) for status in response["data"]]
