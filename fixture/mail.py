import poplib
import email
import time


class MailHelper:
    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(10):
            pop = poplib.POP3(self.app.config["james"]["host"])
            pop.user(username)
            pop.pass_(password)
            mail_count = pop.stat()[0]
            if mail_count > 0:
                for n in range(mail_count):
                    msglines = pop.retr(n+1)[1]
                    msgtext = "\n".join(map(lambda x: x.decode('utf-8'), msglines))
                    message = email.message_from_string(msgtext)
                    if message.get("Subject") == subject:
                        pop.dele(n+1)
                        pop.quit()
                        return message.get_payload()
            pop.quit()
            time.sleep(3)
        return None
