from app.api.management.projects import ProjectAPI
from app.api.management.tasks import TaskAPI
from app.api.management.users import UserAPI
from app.api.management.reports import ReportAPI


class ManagementAPI:
    def __init__(self, client):
        self.client = client

        self.tasks = TaskAPI(self.client)
        self.projects = ProjectAPI(self.client)
        self.users = UserAPI(self.client)
        self.reports = ReportAPI(self.client)
