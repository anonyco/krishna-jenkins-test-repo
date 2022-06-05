from utils.commons import *
import argparse
import time
from email.message import EmailMessage

def deleteDraft(imap, number):
    imap.store(number, "+Flags","\\Deleted")
    imap.expunge()

# initialize argument parsers
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

def create(args):
    imap = getImap(args)
    sourceMail = getEmail(args, args.reportForMailInBox, args.reportForMailNumber)
    mail = EmailMessage()
    mail['Subject'] = f"Draft Report for {sourceMail['Message-Id']}"
    imap.append("Drafts","",imaplib.Time2Internaldate(time.time()), str(mail).encode('utf-8'))

createSubparser(subparser, create, ["imapServer", "imapPort", "imapUser", "imapPassword", "reportForMailInBox", "reportForMailNumber"])

def update(args):
    if not (args.updateWithText or args.updateWithBase64File):
        raise Exception("Parameter Missing, either --updateWithText or --updateWithBase64File should be passed")
    imap = getImap(args, "Drafts")
    sourceMail = getEmail(args, args.reportForMailInBox, args.reportForMailNumber)
    draftSubject = f"Draft Report for {sourceMail['Message-Id']}"
    uid = imap.uid('search',None, f"HEADER Subject \"{draftSubject}\"")[1][0]
    id, rawMessage = imap.uid('Fetch', uid, '(RFC822)')[1][0]
    id = id.decode('utf-8').split()[0]
    mail = email.message_from_bytes(rawMessage)
    if args.updateWithText:
        mail.set_payload(f"{mail.get_payload()}\r\n{args.updateWithText}")
    elif args.updateWithBase64File:
        with open(args.updateWithBase64File) as f:
            data = f.readlines()
        mail.set_payload(f"{mail.get_payload()}\r\n{data}")
    imap.append("Drafts","",imaplib.Time2Internaldate(time.time()), str(mail).encode('utf-8'))
    deleteDraft(imap, id)

createSubparser(subparser, update, ["imapServer", "imapPort", "imapUser", "imapPassword", "reportForMailInBox", "reportForMailNumber"], ["updateWithText","updateWithBase64File"])

def send(args):
    imap = getImap(args, "Drafts")
    sourceMail = getEmail(args, args.reportForMailInBox, args.reportForMailNumber)
    draftSubject = f"Draft Report for {sourceMail['Message-Id']}"
    uid = imap.uid('search',None, f"HEADER Subject \"{draftSubject}\"")[1][0]
    id, rawMessage = imap.uid('Fetch', uid, '(RFC822)')[1][0]
    id = id.decode('utf-8').split()[0]
    mail = email.message_from_bytes(rawMessage)
    mail.add_header("In-Reply-To", sourceMail['Message-Id'])
    mail.add_header("To", sourceMail['From'])
    mail.add_header('From', args.smtpUser)
    mail['Subject']=f"Report for Patch Request {sourceMail['Subject']}"
    sendEmail(args, mail)
    deleteDraft(imap, id)


createSubparser(subparser, send, ["imapServer", "imapPort", "imapUser", "imapPassword", "reportForMailInBox", "reportForMailNumber", "smtpServer", "smtpPort", "smtpUser", "smtpPassword"])

if __name__ == '__main__':
    args = parser.parse_args()
    if len(vars(args).keys()) == 0:
        parser.print_help()
    else:
        args.func(args)