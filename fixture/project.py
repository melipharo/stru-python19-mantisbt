import re
from model import Project
from model.utils import trim_spaces

class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def open_manage_projects_page(self):
        wd = self.app.wd
        on_projects_page = wd.current_url.endswith("manage_proj_page.php")
        if not on_projects_page:
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def get_projects_count(self):
        self.open_manage_projects_page()
        return len(self.app.wd.find_elements_by_xpath("//table[@class='width100']/tbody/tr")) - 3

    def get_projects_list(self):
        self.open_manage_projects_page()

        projects = []
        rows = self.app.wd.find_elements_by_xpath("//table[@class='width100']/tbody/tr")[3:]
        for row in rows:
            cells = row.find_elements_by_xpath("td")
            project_href = cells[0].find_element_by_xpath("a")
            name = project_href.text
            id = re.match(r'.*=(\d)+$', project_href.get_attribute("href")).groups()[0]
            descr = cells[4].text
            projects.append(Project(
                id=id,
                name=name,
                description=descr
            ))

        return projects

    def add_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_data(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def fill_project_data(self, project):
        wd = self.app.wd
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)

    def open_project_edit_page(self, project):
        self.app.wd.find_element_by_link_text(trim_spaces(project.name)).click()

    def remove_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.open_project_edit_page(project)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # validate that we are on the right page
        wd.find_element_by_name("_confirmed")
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
