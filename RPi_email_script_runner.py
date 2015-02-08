#!/usr/bin/env python3

import imaplib
import smtplib
import email
import email.header
import email.mime.text
import re
import subprocess


EMAIL_LOGIN = "user that will login to the IMAP and SMTP host to receive and send emails"
EMAIL_PASSWORD = "this password will be used when authenticating the email user with the IMAP and SMTP host"

IMAP_HOST = "imap.yandex.ru"
IMAP_PORT = 993
SMTP_HOST = "smtp.yandex.ru"
SMTP_PORT = 465

TRIGGER_SUBJECT = "run script"
ALLOWED_SENDERS = ("List of allowed senders", )
RESULT_EMAIL = "you can recieve result on specified email after execution of scripts"
ANSWER_SUBJECT = "Script output"


class Mailer(object):
    def __init__(self, login, password, imap_host, smtp_host, imap_port=993, smtp_port=465):
        self.login = login
        self.password = password
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def read_emails_with_scripts(self, trigger_subject, allowed_senders):
        """Searching of unseen emails with scripts from allowed senders.
        Keyword arguments:
        trigger_subject -- trigger subject for filter
        allowed_senders -- list of senders which allowed execute scripts
        Returns:
        A list with commands.
        """
        server = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
        server.login(self.login, self.password)
        server.select()

        res, data = server.search(None, "(UNSEEN)")
        if res != 'OK':
            #No messages found
            return None

        commands = []
        compiled_pattern = re.compile(r'[A-Za-z]+')
        for num in data[0].split():
            res, raw_email = server.fetch(num, '(RFC822)')
            if res != 'OK':
                #error getting message
                return None

            msg = email.message_from_bytes(raw_email[0][1])
            sender_name, sender_email = email.utils.parseaddr(msg['From'])
            email_header, charset = email.header.decode_header(msg['Subject'])[0]
            if charset:
                subject = email_header.decode(charset)
            else:
                subject = email_header

            if sender_email in allowed_senders and subject.lower() == trigger_subject:
                lines = []
                if msg.is_multipart():
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            charset = part.get_content_charset()
                            lines += part.get_payload(decode=True).decode(charset).split('\n')
                else:
                    charset = msg.get_content_charset()
                    lines = msg.get_payload(decode=True).decode(charset).split('\n')

                for line in lines:
                    if line and compiled_pattern.search(line):
                        commands.append(line.rstrip())

        return commands

    def send_email(self, to_email, subject, text):
        msg = email.mime.text.MIMEText(text, 'plain')
        msg['From'] = self.login
        msg['To'] = to_email
        msg['Subject'] = subject

        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        server.login(self.login, self.password)
        server.sendmail(self.login, to_email, msg.as_string())


if __name__ == '__main__':

    mailer = Mailer(login=EMAIL_LOGIN, password=EMAIL_PASSWORD, imap_host=IMAP_HOST, smtp_host=SMTP_HOST,
                    imap_port=IMAP_PORT, smtp_port=SMTP_PORT)

    commands = mailer.read_emails_with_scripts(trigger_subject=TRIGGER_SUBJECT, allowed_senders=ALLOWED_SENDERS)

    answer = []
    for command in commands:
        answer.append("\n" + command + ":\n")
        try:
            res = subprocess.check_output(command, shell=True)
            answer.append(res.decode('utf-8'))
        except Exception as e:
            answer.append(str(e))

            
    if answer and RESULT_EMAIL:
        mailer.send_email(to_email=RESULT_EMAIL, subject=ANSWER_SUBJECT, text="\n".join(answer))
