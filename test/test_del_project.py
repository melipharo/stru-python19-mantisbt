import random
from model import Project


def test_del_project(app):
    if len(app.soap.get_projects_list()) == 0:
        project = Project.random()
        while app.soap.get_project_id(project) is None:
            project = Project.random()

    old_list = app.soap.get_projects_list()
    project = random.choice(old_list)
    app.project.remove_project(project)
    old_list.remove(project)

    new_list = app.soap.get_projects_list()
    assert sorted(old_list) == sorted(new_list)
