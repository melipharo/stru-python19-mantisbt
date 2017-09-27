import pytest
from fixture import Application
import json
import os.path

target = None
webfixture = None

def load_config(file):
    global target
    if target is None:
        with open(file) as targetfile:
            target = json.load(targetfile)
    return target


@pytest.fixture
def app(request):
    global webfixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    user_config = load_config(request.config.getoption("--target"))["webadmin"]

    if webfixture is None or not webfixture.is_valid():
        webfixture = Application(browser=browser, base_url=web_config["baseUrl"])

    webfixture.session.ensure_login(
        username=user_config["username"],
        password=user_config["password"]
    )
    return webfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global webfixture

    def fin():
        if webfixture:
            webfixture.session.ensure_logout()
            webfixture.destroy()
    request.addfinalizer(fin)
    return webfixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption(
        "--target",
        action="store",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "target.json")
    )
