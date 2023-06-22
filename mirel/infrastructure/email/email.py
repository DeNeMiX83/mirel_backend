import smtplib
from email.mime.text import MIMEText
from mirel.config.settings import Settings
from mirel.core.dto import ForwardingFeedbackData
from mirel.core.protocols import EmailSender


class EmailSenderImpl(EmailSender):
    def __init__(self, settings: Settings):
        email_sender_settings = settings.email_sender_settings
        self.email_username = email_sender_settings.email_username
        self.email_password = email_sender_settings.email_password
        self.email_from = email_sender_settings.email_from
        self.email_to_default = email_sender_settings.email_to_default
        self.server = email_sender_settings.server
        self.server_port = email_sender_settings.server_port
        self.jinja_templates = settings.jinja_templates

    async def forwarding_feedback(self, data: ForwardingFeedbackData):
        template = self.jinja_templates.get_template("feedback_tmp.html")
        rendered_message = template.render(
            name=data.name,
            email=data.email,
            telephone=data.telephone,
            message=data.msg,
        )
        email_message = MIMEText(rendered_message)
        email_message["Subject"] = "Новое обращение"
        email_message["From"] = self.email_from
        email_recepient = self.email_to_default
        if data.email_recipient is not None:
            email_recepient = data.email_recipient
        email_message["To"] = email_recepient

        server = smtplib.SMTP_SSL(self.server, self.server_port)
        server.ehlo()
        server.login(self.email_from, self.email_password)
        server.send_message(email_message)
