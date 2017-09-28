from model import random_username


def test_signup_new_account(app):
    app.session.ensure_logout()

    username = random_username("user_")
    email = "{}@localhost".format(username)
    password = "test"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, password, email)
    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.logout()
