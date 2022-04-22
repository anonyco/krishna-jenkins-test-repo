import smtplib
import imaplib
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
spSendNoticiationMails = subparser.add_parser('notificationMailer')
spSendNoticiationMails.add_argument("--smtp_server", required=True)
spSendNoticiationMails.add_argument("--smtp_port", required=True)
spSendNoticiationMails.add_argument("--smtp_user", required=True)
spSendNoticiationMails.add_argument("--smtp_password", required=True)
spSendNoticiationMails.add_argument("--to", required=True)
spSendNoticiationMails.add_argument("--template", required=True)
spSendNoticiationMails.set_defaults(func=sendNoticiationMails)

# patch formatter before sending email
def insertBranchInSubject(subject, branch):
    subject = subject.rstrip()
    subjectLines= subject.split(" ",2)
    commitMessage = subjectLines[2]
    return f"{' '.join(subjectLines[:2])} BranchName: {branch} ||| CommitMessage: {subjectLines[2]}\n"

def patchFormatter(args):
    path = args.path
    branch = args.branch
    files = os.listdir(path)
    for file in files:
        with open(f"{path}/{file}") as f:
            data = f.readlines()
            for line in data:
                if "Subject: [PATCH]" in line:
                    subjectLineIndex = data.index(line)
                    newSubjectLine = insertBranchInSubject(line, branch)
                    break
            data[subjectLineIndex] = newSubjectLine
        with open(f"{path}/{file}","w") as f:
            f.writelines(data)

spPatchFormatter = subparser.add_parser('patchFormatter')
spPatchFormatter.add_argument("--path", help = "path to patches", required=True)
spPatchFormatter.add_argument("--branch", help = "branch to insert", required=True)
spPatchFormatter.set_defaults(func=patchFormatter)

# patch branch identifier
def getBranchFromSubject(subject):
    return subject.split('|||')[0].strip().split("BranchName:")[-1].strip()

def patchBranchIdentifier(args):
    path = args.path
    with open(f"{path}") as f:
        data = f.readlines()
        for line in data:
            if "Subject: [PATCH]" in line:
                branch = getBranchFromSubject(line)
                break
    print(branch)

spPatchBranchIdentifier = subparser.add_parser('patchBranchIdentifier')
spPatchBranchIdentifier.add_argument("--path", help = "path to patches", required=True)
spPatchBranchIdentifier.set_defaults(func=patchBranchIdentifier)

# patch reformatter after recieving the mail
def removeBranchNameFromSubject(subject):
    commitMessage = subject.strip().split('|||')[-1].strip().split('CommitMessage:')[-1].strip()
    return f"{' '.join(subject.strip().split(' ',2)[:2])} {commitMessage}\n"

def patchReFormatter(args):
    path = args.path
    with open(f"{path}") as f:
        data = f.readlines()
        for line in data:
            if "Subject: [PATCH]" in line:
                subjectLineIndex = data.index(line)
                newSubjectLine = removeBranchNameFromSubject(line)
                break
        data[subjectLineIndex] = newSubjectLine
    with open(f"{path}","w") as f:
        f.writelines(data)

spPatchReFormatter = subparser.add_parser('patchReFormatter')
spPatchReFormatter.add_argument("--path", help = "path to patches", required=True)
spPatchReFormatter.set_defaults(func=patchReFormatter)


# download Mail from inbox
def downloadPatchMail(args):
    path = args.path
    messsageNumber = args.messageNumber
    imapServer = args.imap_server
    imapPort = args.imap_port
    imapUser = args.imap_user
    imapPassword = args.imap_password
    imapInbox =  args.imap_inbox
    imap = imaplib.IMAP4_SSL(imapServer)
    imap.login(imapUser, imapPassword)
    imap.select(imapInbox)
    tmp, data = imap.fetch(messsageNumber, '(RFC822)')
    f = open(path, "w")
    f.write(data[0][1].decode('utf-8'))
    f.close()
    imap.close()


spDownloadPatchMail = subparser.add_parser('downloadPatchMail')
spDownloadPatchMail.add_argument("--path", help = "path to patches", required=True)
spDownloadPatchMail.add_argument("--messageNumber", help = "Message Number from Jenkins", required=True)
spDownloadPatchMail.add_argument("--imap_server", required=True)
spDownloadPatchMail.add_argument("--imap_port", required=True)
spDownloadPatchMail.add_argument("--imap_user", required=True)
spDownloadPatchMail.add_argument("--imap_password", required=True)
spDownloadPatchMail.add_argument("--imap_inbox", required=True)

spDownloadPatchMail.set_defaults(func=downloadPatchMail)

# download and reformat patch

def downloadReFormat(args):
    downloadPatchMail(args)
    patchReFormatter(args)
    pass

spDownloadReFormat = subparser.add_parser('downloadReFormat')
spDownloadReFormat.add_argument("--path", help = "path to patches", required=True)
spDownloadReFormat.add_argument("--messageNumber", help = "Message Number from Jenkins", required=True)
spDownloadReFormat.add_argument("--imap_server", required=True)
spDownloadReFormat.add_argument("--imap_port", required=True)
spDownloadReFormat.add_argument("--imap_user", required=True)
spDownloadReFormat.add_argument("--imap_password", required=True)
spDownloadReFormat.add_argument("--imap_inbox", required=True)

spDownloadReFormat.set_defaults(func=downloadReFormat)


# download and reformat patch

def downloadAndGetBranch(args):
    downloadPatchMail(args)
    patchBranchIdentifier(args)
    pass

spDownloadAndGetBranch = subparser.add_parser('downloadAndGetBranch')
spDownloadAndGetBranch.add_argument("--path", help = "path to patches", required=True)
spDownloadAndGetBranch.add_argument("--messageNumber", help = "Message Number from Jenkins", required=True)
spDownloadAndGetBranch.add_argument("--imap_server", required=True)
spDownloadAndGetBranch.add_argument("--imap_port", required=True)
spDownloadAndGetBranch.add_argument("--imap_user", required=True)
spDownloadAndGetBranch.add_argument("--imap_password", required=True)
spDownloadAndGetBranch.add_argument("--imap_inbox", required=True)

spDownloadAndGetBranch.set_defaults(func=downloadAndGetBranch)


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)

