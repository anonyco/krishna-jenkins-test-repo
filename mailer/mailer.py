import smtplib
import imaplib
from email.message import EmailMessage
import email
import argparse
from jinja2 import  Environment, FileSystemLoader
import os
import re
import sys
from os import path
import shutil
import base64
import ssl

SUBJECT_REGEXES = ["^[PATCH [0-9]+/[0-9]+]", "^\[PATCH\]"]

def regexListMatch(regexList, string):
    for pattern in regexList:
        x = re.search(pattern, string)
        if x:
            return x
    return False

def createSubparser(subparser, func, argList):
    parser = subparser.add_parser(func.__name__)
    for arg in argList:
        parser.add_argument(f"--{arg}", required=True)
    parser.set_defaults(func=func)

def getTLSContext():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    return context

def getImap(args):
    context = getTLSContext()
    try:
        imap = imaplib.IMAP4_SSL(args.imapServer, args.imapPort, ssl_context=context)
    except ssl.SSLCertVerificationError as e:
        print("SSL Certificate is not Verified, Try this SO Post: https://stackoverflow.com/a/58394602", file=sys.stderr)
        raise e
    imap.login(args.imapUser, args.imapPassword)
    imap.select(args.imapInbox)
    return imap

def getEmail(messageNumber, args):
    imap = getImap(args)
    _, data = imap.fetch(messageNumber,'(RFC822)')
    mail = email.message_from_bytes(data[0][1])
    imap.close()
    return mail

def writeMessageToFile(path, mail):
    fileName = getFileName(mail['subject'])
    with open(f"{path}/{fileName}","w") as f:
        f.write(mail.as_string())

def getFileName(subject):
    patchNumber = str(getPatchNumber(subject))
    commitMessage = getCommitMessage(subject)
    return f"{patchNumber.zfill(5)}-{commitMessage}.patch"

def getPatchNumber(subject):
    PatchSection = regexListMatch(SUBJECT_REGEXES, subject).group()
    patchRe = re.search("\[PATCH (.+?)/[0-9]+\]",PatchSection)
    currentPatchCount = int(patchRe.group(1)) if patchRe else 1
    return currentPatchCount

def ensureFolder(folderPath):
    if path.exists(folderPath) and path.isdir(folderPath) and len(os.listdir(folderPath)) == 0:
        pass
    elif path.exists(folderPath) and ((path.isdir(folderPath) and len(os.listdir(folderPath)) > 0) or (not path.isdir(folderPath))):
        shutil.rmtree(folderPath)
        os.mkdir(folderPath)
    else:
        os.mkdir(folderPath)

def getBranchFromSubject(subject):
    return subject.split('|||')[0].strip().split("BranchName:")[-1].strip()

def insertBranchInSubject(subject, branch):
    subject = subject.rstrip()
    regexMatch = regexListMatch(SUBJECT_REGEXES, subject)
    return f"{subject[:regexMatch.end()].strip()} BranchName: {branch} ||| CommitMessage: {subject[regexMatch.end():].strip()}\n"

def getCommitMessage(subject):
    return subject.strip().split('|||')[-1].strip().split('CommitMessage:')[-1].strip()

def removeBranchNameFromSubject(subject):
    subject = subject.split('Subject:',1)[-1].strip()
    commitMessage = getCommitMessage(subject)
    patchRegex = regexListMatch(SUBJECT_REGEXES, subject)
    patchString = patchRegex.group()
    return f"Subject: {patchString} {commitMessage}\n"

def prepareMailFromJinja(env, template):
    jenv = Environment(loader = FileSystemLoader(f"templates/{template}"))
    msg = EmailMessage()
    msg['Subject'] = jenv.get_template("subject.jinja").render(**env)
    msg.set_content(jenv.get_template("body.jinja").render(**env))
    return msg

def getSMTPCon(args):
    context = getTLSContext()
    try:
        mailserver = smtplib.SMTP(args.smtpServer,args.smtpPort)
        mailserver.ehlo()
        mailserver.starttls(context=context)
        mailserver.login(args.smtpUser, args.smtpPassword)
    except ssl.SSLCertVerificationError as e:
        print("SSL Certificate is not Verified, Try this SO Post: https://stackoverflow.com/a/58394602", file=sys.stderr)
        raise e
    return mailserver

# initialize argument parsers
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

# to send notifications, used by jenkins
def notificationMailer(args):
    mailserver = getSMTPCon(args)
    env = os.environ
    msg = prepareMailFromJinja(env, args.template)
    msg['From'] = args.smtpUser
    msg['To'] = args.to
    mailserver.send_message(msg)
    mailserver.quit()


# add sendNotificationMails to subparser
# example call: python mailer.py notificationMailer <Arguments as shown below>
createSubparser(subparser, notificationMailer, ["smtpServer", "smtpPort", "smtpUser", "smtpPassword","to","template"])

# patch formatter before sending email
def patchFormatter(args):
    path = args.path
    branch = args.branch
    files = os.listdir(path)
    for file in files:
        with open(f"{path}/{file}") as f:
            data = f.readlines()
            for line in data:
                if re.search("^Subject: \[PATCH",line):
                    subjectLineIndex = data.index(line)
                    newSubjectLine = f"Subject: {insertBranchInSubject(line.split('Subject: ',1)[-1], branch)}"
                    break
            data[subjectLineIndex] = newSubjectLine
        with open(f"{path}/{file}","w") as f:
            f.writelines(data)

createSubparser(subparser, patchFormatter, ["path","branch"])

# patch reformatter after recieving the mail
def patchReFormatter(args):
    path = args.path
    files = os.listdir(path)
    for file in files:
        with open(f"{path}/{file}") as f:
            data = f.readlines()
            for line in data:
                if "Subject: [PATCH" in line:
                    subjectLineIndex = data.index(line)
                    newSubjectLine = removeBranchNameFromSubject(line)
                    break
            data[subjectLineIndex] = newSubjectLine
        with open(f"{path}/{file}","w") as f:
            f.writelines(data)

createSubparser(subparser, patchReFormatter, ["path"])

# download Mail from inbox
def downloadPatchMail(args):
    path = args.path
    ensureFolder(path)
    messageNumber = args.messageNumber
    imap = getImap(args)
    mail = getEmail(messageNumber, args)
    PatchSection = regexListMatch(SUBJECT_REGEXES, mail['subject']).group()
    patchRe = re.search("\[PATCH [0-9]+/(.+?)\]",PatchSection)
    totalPatchCount = int(patchRe.group(1)) if patchRe else 1
    print(totalPatchCount)
    messageId = mail['Message-Id']
    if totalPatchCount == 1:
        writeMessageToFile(path, mail)
    else:
        writeMessageToFile(path, mail)
        messageNumbers = imap.search(None,'HEADER', 'In-Reply-To', messageId)
        messageNumbers = messageNumbers[1][0].decode('utf-8').split()
        for messageNumber in messageNumbers:
            mail = getEmail(messageNumber, args)
            writeMessageToFile(path,mail)



createSubparser(subparser, downloadPatchMail, ["path","messageNumber","imapServer","imapPort","imapUser","imapPassword","imapInbox"])

# download and reformat patch

def downloadReFormat(args):
    downloadPatchMail(args)
    patchReFormatter(args)
    pass

createSubparser(subparser, downloadReFormat, ["path","messageNumber","imapServer","imapPort","imapUser","imapPassword","imapInbox"])

# get the branch name for a given message number
def checkMailForBranch(args):
    mail = getEmail(args.messageNumber, args)
    branchName = getBranchFromSubject(mail['subject'])
    print(branchName)

createSubparser(subparser, checkMailForBranch, ["messageNumber","imapServer","imapPort","imapUser","imapPassword","imapInbox"])

# Check if Mail should trigger a Job

def checkMailForJobTrigger(args):
    mail = getEmail(args.messageNumber, args)
    if 'In-Reply-To' in mail:
        sys.exit(1)
    else:
        sys.exit()
    
createSubparser(subparser, checkMailForJobTrigger, ["messageNumber","imapServer","imapPort","imapUser","imapPassword","imapInbox"])

# to Failed Patch 
def failedPatchMail(args):
    mailserver = getSMTPCon(args)
    f = open(args.badPatchPath)
    mail = email.message_from_file(f)
    f.close()

    msg = EmailMessage()
    msg['Subject'] = f"PATCH FAILURE: {mail['Subject']}"
    msg['From'] = args.smtpUser
    msg['To'] = mail['Return-Path']
    msg['In-Reply-To'] = mail['Message-Id']
    msg['References'] = mail['Message-Id']
    message = "A Patch Failed, Please fix and send all the Patches in the Chain again\n" + "-"*25 + "\n" + base64.b64decode(mail.__dict__['_payload'].replace('\n','')).decode('UTF-8')

    msg.set_content(message)
    mailserver.send_message(msg)
    mailserver.quit()

createSubparser(subparser, failedPatchMail, ["smtpServer", "smtpPort", "smtpUser", "smtpPassword","badPatchPath"])

def getMailParameter(args):
    mail = getEmail(args.messageNumber, args)
    print(mail[args.mailParameter])

createSubparser(subparser, getMailParameter, ["imapServer","imapPort","imapUser","imapPassword","messageNumber","mailParameter", "imapInbox"])


def patchRejectionForBranch(args):
    mail = getEmail(args.messageNumber, args)
    mailserver = getSMTPCon(args)
    env = os.environ
    subject = mail['Subject']
    env["PATCH_SUBJECT"] = subject
    env["TARGET_BRANCH"] = getBranchFromSubject(subject)
    msg = prepareMailFromJinja(env, "patchRejectionForBranch")
    msg['From'] = args.smtpUser
    msg['To'] = mail['Return-Path']
    msg['In-Reply-To'] = mail['Message-Id']
    msg['References'] = mail['Message-Id']
    mailserver.send_message(msg)
    mailserver.quit()

createSubparser(subparser, patchRejectionForBranch, ["imapServer","imapPort","imapUser","imapPassword","messageNumber", "imapInbox", "smtpServer", "smtpPort", "smtpUser", "smtpPassword"])


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
