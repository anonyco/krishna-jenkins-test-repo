#! /bin/bash

if [[ $# -lt 2 ]]
then
  echo "Usage: $0 <smtp file> <recipient email>"
  exit 1
fi

SMTP_FILE=$1
RECIPIENT_EMAIL=$2

sed 's/\r$//' ${SMTP_FILE} > smtp_creds.txt
export $(cat smtp_creds.txt | xargs)

echo "python mailer.py --smtp_server $SMTP_SERVER --smtp_port $SMTP_PORT --smtp_user $SMTP_USER --smtp_password $SMTP_PASSWORD --to $RECIPIENT_EMAIL --template accept_pr"
python mailer.py --smtp_server $SMTP_SERVER --smtp_port $SMTP_PORT --smtp_user $SMTP_USER --smtp_password $SMTP_PASSWORD --to $RECIPIENT_EMAIL --template accept_pr
