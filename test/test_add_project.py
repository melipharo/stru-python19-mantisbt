from model import Project


def test_add_project(app):
    old_list = app.soap.get_projects_list()
    project = Project.random()
    while app.soap.get_project_id(project) is None:
        project = Project.random()
    app.project.add_project(project)
    old_list.append(project)

    new_list = app.soap.get_projects_list()
    assert sorted(old_list) == sorted(new_list)
