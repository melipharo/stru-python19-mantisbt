from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper

class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(
                firefox_binary="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
            )
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unknown browser {}".format(browser))

        self.base_url = base_url

        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)

    def open_home_page(self):
        self.wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False
