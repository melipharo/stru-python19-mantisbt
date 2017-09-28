from telnetlib import Telnet


class JamesHelper:
    def __init__(self, app):
        self.app = app
        self.config = self.app.config["james"]

    def ensure_user_exists(self, username, password):
        session = JamesHelper.Session(
            self.config["host"],
            self.config["port"],
            self.config["username"],
            self.config["password"]
        )
        if session.is_user_registered(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

    class Session:
        def _read_until(self, text):
            self.telnet.read_until(text.encode('ascii'), timeout=5)

        def _write(self, text):
            self.telnet.write(text.encode('ascii'))

        def __init__(self, host, port, username, password):
            self.telnet = Telnet(host=host, port=port, timeout=5)
            self._read_until("Login id:")
            self._write("{}\n".format(username))
            self._read_until("Password:")
            self._write("{}\n".format(password))
            self._read_until("Welcome {}. HELP for a list of commands".format(username))

        def is_user_registered(self, username):
            self._write("verify {}\n".format(username))
            res = self.telnet.expect([b"exists", b"does not exist"])
            return res[0] == 0

        def create_user(self, username, password):
            self._write("adduser {} {}\n".format(username, password))
            self._read_until("User {} added".format(username))

        def reset_password(self, username, password):
            self._write("setpassword {} {}\n".format(username, password))
            self._read_until("Password for {} reset".format(username))

        def quit(self):
            self._write("quit\n")
