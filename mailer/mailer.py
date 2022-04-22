import smtplib
from email.message import EmailMessage
import argparse
from jinja2 import  Environment, FileSystemLoader
import os

# initialize argument parsers
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

# to send notifications, used by jenkins
def sendNoticiationMails(args):
    mailserver = smtplib.SMTP(args.smtp_server,args.smtp_port)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(args.smtp_user, args.smtp_password)

    jenv = Environment(loader = FileSystemLoader(f"templates/{args.template}"))
    env = os.environ

    msg = EmailMessage()
    msg['Subject'] = jenv.get_template("subject.jinja").render(**env)
    msg['From'] = args.smtp_user
    msg['To'] = args.to
    msg.set_content(jenv.get_template("body.jinja").render(**env))


    mailserver.send_message(msg)
    mailserver.quit()

# add sendNotificationMails to subparser
# example call: python mailer.py notificationMailer <Arguments as shown below>
notificationMailer = subparser.add_parser('notificationMailer')

notificationMailer.add_argument("--smtp_server", required=True)
notificationMailer.add_argument("--smtp_port", required=True)
notificationMailer.add_argument("--smtp_user", required=True)
notificationMailer.add_argument("--smtp_password", required=True)
notificationMailer.add_argument("--to", required=True)
notificationMailer.add_argument("--template", required=True)

notificationMailer.set_defaults(func=sendNoticiationMails)


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    args.func(args)

