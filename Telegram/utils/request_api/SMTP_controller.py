from email.mime.text import MIMEText
import logging as logger
from smtplib import SMTP

from colorama import Fore
from Data import SMTP_SERVER, SMTP_PORT, SMTP_FROM_LOGIN, SMTP_FROM_PASSWORD, SMTP_TO


class SMTPController:

    def __init__(self, fully_name, group, date, first_time, second_time, phone, state_number, email):
        self.message = None
        self.fully_name = fully_name
        self.group = group
        self.email = email
        self.date = date
        self.first_time = first_time
        self.second_time = second_time
        self.phone = phone
        self.state_number = state_number

    def build_message(self):
        html = f"""\
            <html>
              <head></head>
              <body>
                <p><strong>{self.fully_name}</strong>, <strong>{self.group}</strong><br>
                   открыл шлагбаум за ({self.date}) - период: {self.first_time} - {self.second_time} более 2 раз! <br>
                   Его номер телефона: <a>{self.phone}</a>. Гос. номер: <a>{self.state_number}</a>.<br>
                   Сообщение сформировано автоматически:<br>
                    <a href="https://t.me/Alf_Kai_Bot">Telegram Bot</a>.
                </p>
              </body>
            </html> 
        """

        message = MIMEText(html, 'html')
        message['Subject'] = "Parking Abuse"
        message['From'] = SMTP_FROM_LOGIN
        message['Reply-To'] = self.email
        message['To'] = SMTP_TO
        self.message = message

    def send_message(self):
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            try:
                server.login(SMTP_FROM_LOGIN, SMTP_FROM_PASSWORD)
                server.send_message(self.message)
            except Exception as _ex:
                logger.error(f"{Fore.LIGHTRED_EX}Error with send message func {Fore.LIGHTYELLOW_EX}{_ex}{Fore.RESET}")

