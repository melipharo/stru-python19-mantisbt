from model import Project
from model import utils


def test_add_project(app):
    old_list = app.project.get_projects_list()
    project = Project(
        name=utils.random_string(),
        description=utils.random_string()
    )
    app.project.add_project(project)
    old_list.append(project)

    assert len(old_list) == app.project.get_projects_count()
    new_list = app.project.get_projects_list()
    assert sorted(old_list) == sorted(new_list)
