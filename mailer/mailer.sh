#! /bin/bash

if [[ $# -lt 1 ]]
then
  echo "Usage: $0 <smtp file>"
fi

SMTP_FILE=$1

export $(cat ${SMTP_FILE} | xargs)

python mailer.py --smtp_server $SMTP_SERVER --smtp_port $SMTP_PORT --smtp_user $SMTP_USER --smtp_password $SMTP_PASSWORD --to $SMTP_USER --template accept_pr
