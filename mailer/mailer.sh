#! /bin/bash

if [[ $# -lt 2 ]]
then
  echo "Usage: $0 <smtp file> <recipient email> <template>"
  exit 1
fi

SMTP_FILE=$1
RECIPIENT_EMAIL=$2
TEMPLATE=$3

sed 's/\r$//' ${SMTP_FILE} > smtp_creds.txt
export $(cat smtp_creds.txt | xargs)

echo "python mailer.py notificationMailer --smtp_server $SMTP_SERVER --smtp_port $SMTP_PORT --smtp_user $SMTP_USER --smtp_password $SMTP_PASSWORD --to $RECIPIENT_EMAIL --template $TEMPLATE"
python mailer.py notificationMailer --smtp_server $SMTP_SERVER --smtp_port $SMTP_PORT --smtp_user $SMTP_USER --smtp_password $SMTP_PASSWORD --to $RECIPIENT_EMAIL --template $TEMPLATE
