import pytest
from fixture import Application
import json
import os.path
import ftputil

target = None
webfixture = None

def load_config(file):
    global target
    if target is None:
        with open(file) as targetfile:
            target = json.load(targetfile)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global webfixture
    browser = request.config.getoption("--browser")

    if webfixture is None or not webfixture.is_valid():
        webfixture = Application(browser=browser, config=config)

    webfixture.session.ensure_login(
        username=config["webadmin"]["username"],
        password=config["webadmin"]["password"]
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


@pytest.fixture(scope="session", autouse=True)
def configure_ftp_server(request, config):
    install_server_configuration(
        host=config["ftp"]["host"],
        username=config["ftp"]["username"],
        password=config["ftp"]["password"]
    )

    def fin():
        restore_server_configuration(
            host=config["ftp"]["host"],
            username=config["ftp"]["username"],
            password=config["ftp"]["password"]
        )
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc_ORIG_AUTOTEST.php"):
            remote.remove("config_inc_ORIG_AUTOTEST.php")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc_ORIG_AUTOTEST.php")
        disabled_captcha_config = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "resources/config_inc.php"
        )
        remote.upload(disabled_captcha_config, "config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc_ORIG_AUTOTEST.php"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc_ORIG_AUTOTEST.php", "config_inc.php")
