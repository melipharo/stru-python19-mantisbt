from suds.client import Client
from suds import WebFault
from model.project import Project


class SOAPHelper:
    def __init__(self, app):
        self.app = app
        self.config = app.config["soap"]
        self.config.update(app.config["webadmin"])

        self.client = Client(self.config["baseUrl"])

    def can_login(self, username, password):
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self):
        try:
            projects = self.client.service.mc_projects_get_user_accessible(
                self.config["username"],
                self.config["password"]
            )
            return [Project(id=project.id, name=project.name) for project in projects]
        except WebFault:
            return None

    def get_project_id(self, project):
        try:
            return self.client.service.mc_project_get_id_from_name(
                self.config["username"],
                self.config["password"],
                project.name
            )
        except WebFault:
            return None
