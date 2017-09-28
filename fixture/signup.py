import re

class SignupHelper:
    def __init__(self, app):
        self.app = app

    def new_user(self, username, password, email):
        wd = self.app.wd
        wd.get("{}/signup_page.php".format(self.app.base_url))
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").click()
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector('input[type="submit"]').click()

        mail = self.app.mail.get_mail(
            username,
            password,
            "[MantisBT] Account registration"
        )
        if mail:
            url = self.extract_confirmation_url(mail)
            wd.get(url)

            wd.find_element_by_name("password").click()
            wd.find_element_by_name("password").clear()
            wd.find_element_by_name("password").send_keys(password)
            wd.find_element_by_name("password_confirm").click()
            wd.find_element_by_name("password_confirm").clear()
            wd.find_element_by_name("password_confirm").send_keys(password)
            wd.find_element_by_css_selector('input[value="Update User"]').click()
        else:
            assert False, "check your email server: seems like it doesn't works well"

    def extract_confirmation_url(self, text):
        return re.search("http://.*$", text, re.MULTILINE).group(0)
