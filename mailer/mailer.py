import smtplib
from email.message import EmailMessage
import argparse
from jinja2 import  Environment, FileSystemLoader
import os

parser = argparse.ArgumentParser()
parser.add_argument("--smtp_server", required=True)
parser.add_argument("--smtp_port", required=True)
parser.add_argument("--smtp_user", required=True)
parser.add_argument("--smtp_password", required=True)
parser.add_argument("--to", required=True)
parser.add_argument("--template", required=True)

args = parser.parse_args()

print(args)

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
