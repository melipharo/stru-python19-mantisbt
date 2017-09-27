import random
from model import Project
from model import utils

def test_del_project(app):
    if app.project.get_projects_count() == 0:
        app.project.add_project(
            Project(
                name=utils.random_string(),
                description=utils.random_string()
            )
        )

    old_list = app.project.get_projects_list()
    project = random.choice(old_list)
    app.project.remove_project(project)
    old_list.remove(project)

    assert len(old_list) == app.project.get_projects_count()
    new_list = app.project.get_projects_list()
    assert sorted(old_list) == sorted(new_list)
