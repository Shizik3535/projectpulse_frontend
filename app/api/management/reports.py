class ReportAPI:
    def __init__(self, client):
        self.client = client

    def create_report_by_task(self, task_id: int):
        """Создание отчета по задаче"""
        response = self.client.file_request(
            endpoint=f"/manager/reports/tasks/{task_id}",
        )

        if "error" in response:
            raise Exception("Ошибка создания отчета по задаче")

        return response["data"]

    def create_report_by_user(self, user_id: int):
        """Создание отчета по пользователю"""
        response = self.client.file_request(
            endpoint=f"/manager/reports/users/{user_id}",
        )

        if "error" in response:
            raise Exception("Ошибка создания отчета по пользователю")

        return response["data"]

    def create_report_by_project(self, project_id: int):
        """Создание отчета по проекту"""
        response = self.client.file_request(
            endpoint=f"/manager/reports/projects/{project_id}",
        )

        if "error" in response:
            raise Exception("Ошибка создания отчета по проекту")

        return response["data"]
