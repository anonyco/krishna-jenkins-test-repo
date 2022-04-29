#! /bin/bash

if [[ $# -lt 2 ]]
then
  echo "Usage: $0 <SMTP Configfile> <Function Type> <Other Options>"
  exit 1
fi

PYTHON_BIN=$(which python)

SMTP_FILE=$1
shift
FUNCTION_TYPE=$1
shift

sed 's/\r$//' ${SMTP_FILE} > smtp_creds.txt
export $(cat smtp_creds.txt | xargs)

notificationMailer () {
    if [[ $# -lt 2 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <Recepient> <Template>"
        exit 1
    fi
    RECIPIENT_EMAIL=$1
    TEMPLATE=$2
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --smtpServer $SMTP_SERVER --smtpPort $SMTP_PORT --smtpUser $SMTP_USER --smtpPassword $SMTP_PASSWORD --to $RECIPIENT_EMAIL --template $TEMPLATE
}

patchFormatter () {
    if [[ $# -lt 2 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <PATH to files> <Branch>"
        exit 1
    fi
    PATH=$1
    BRANCH=$2
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --path $PATH --branch $BRANCH
}

patchReFormatter () {
    if [[ $# -lt 1 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <path>"
        exit 1
    fi
    PATH=$1 
    echo "$PYTHON_BIN mailer.py $FUNCTION_TYPE --path $PATH"
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --path $PATH

}

downloadPatchMail () {
    if [[ $# -lt 3 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <path to download> <messageNumber> <imapInbox>"
        exit 1
    fi
    PATH=$1
    MESSAGE_NUMBER=$3
    IMAP_INBOX=$2
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --imapServer $IMAP_SERVER --imapPort $IMAP_PORT --imapUser $IMAP_USER --imapPassword $IMAP_PASSWORD --path $PATH --messageNumber $MESSAGE_NUMBER --imapInbox $IMAP_INBOX

}

downloadReFormat () {
    if [[ $# -lt 3 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <path to download> <messageNumber> <imapInbox>"
        exit 1
    fi
    PATH=$1
    MESSAGE_NUMBER=$2
    IMAP_INBOX=$3
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --imapServer $IMAP_SERVER --imapPort $IMAP_PORT --imapUser $IMAP_USER --imapPassword $IMAP_PASSWORD --path $PATH --messageNumber $MESSAGE_NUMBER --imapInbox $IMAP_INBOX
}

checkMailForBranch () {
    if [[ $# -lt 2 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <mail inbox> <message number>"
        exit 1
    fi
    IMAP_INBOX=$1
    MESSAGE_NUMBER=$2
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --imapServer $IMAP_SERVER --imapPort $IMAP_PORT --imapUser $IMAP_USER --imapPassword $IMAP_PASSWORD --messageNumber $MESSAGE_NUMBER --imapInbox $IMAP_INBOX
}

checkMailForJobTrigger () {
    if [[ $# -lt 2 ]]
    then
        echo "Usage: $0 $SMTP_FILE $FUNCTION_TYPE <mail inbox> <message number>"
        exit 1
    fi
    IMAP_INBOX=$1
    MESSAGE_NUMBER=$2
    $PYTHON_BIN mailer.py $FUNCTION_TYPE --imapServer $IMAP_SERVER --imapPort $IMAP_PORT --imapUser $IMAP_USER --imapPassword $IMAP_PASSWORD --messageNumber $MESSAGE_NUMBER --imapInbox $IMAP_INBOX
}

if [[ $(type -t $FUNCTION_TYPE) != function ]]; then
    echo "$FUNCTION_TYPE doesn't exists"
fi

$FUNCTION_TYPE $@
