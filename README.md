# RPi_email_script_runner
RPi_email_script_runner is a Python script which runs your scripts delivered by email.

# Introduction
RPi_email_script_runner is a Python script which runs your scripts delivered by email and sends answers by email. You need install only Python3 to run it. It was created for my RPI, but this script can be used by Unix based system.

# Status
Script's will be continued if it needs.

#Configuration
Next variables must be changed for script working:

**EMAIL_LOGIN**
    This is the user that will login to the IMAP and SMTP host to receive and send emails.

**EMAIL_PASSWORD**
    This password will be used when authenticating the email user with the IMAP and SMTP host.

**IMAP_HOST**
    Emails will be received using this IMAP host.

**IMAP_PORT**
    This port will be used for IMAP host communucating.

**SMTP_HOST**
    Emails will be sent using this SMTP host.

**SMTP_PORT**
    This port will be used for SMTP host communucating.

**TRIGGER_SUBJECT**
    If "TRIGGER_SUBJECT" appears in subject, then script runs. It should be in lowercase.

**ALLOWED_SENDERS**
    List of allowed senders. In some cases *.*@yandex.ru shows as *-*@ya.ru so it should be added both. It can take place in other mailbox.

**RESULT_EMAIL**
    You can recieve result on specified email after execution of scripts.

**ANSWER_SUBJECT**
    All emails with result will have that subject.
 
# Schedule crontab
RPi_email_script_runner can be executed by schedule. For example, you can use 2 minutes delay. RPi_email_script_runner will check unseen emails and will execute delivered commands each 2 minutes.

Open crontab with command:

crontab -e

and add new entry:

 */2 * * * * export DISPLAY=:0 && /usr/bin/python3 /home/pi/path_to_script/RPi_email_script_runner.py >> /home/pi/path_to_log/cron.log 2>&1

# Usage
Usage of RPi_email_script_runner is very simple. You just have to send e-mail with your BASH commands 
to specified e-mail address from your e-mail account, which shoud be in ALLOWED_SENDERS.
This email is checked every 2 minutes by RPi_email_script_runner and if any new emails with commands is found, 
RPi_email_script_runner will execute it.

#Licence
MIT License.

