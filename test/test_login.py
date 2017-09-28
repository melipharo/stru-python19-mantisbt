def test_login_loogut(app, config):
    app.session.ensure_logout()
    app.session.login(config["webadmin"]["username"], config["webadmin"]["password"])
    assert app.session.is_logged_in_as("administrator")
    app.session.logout()
