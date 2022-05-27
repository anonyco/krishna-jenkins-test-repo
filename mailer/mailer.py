from email.message import EmailMessage
import email
import argparse
import os
import re
import sys
from os import path
import base64
from utils.commons import *

# initialize argument parsers
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

# to send notifications, used by jenkins
def notificationMailer(args):
    env = os.environ
    msg = prepareMailFromJinja(env, args.template)
    msg['From'] = args.smtpUser
    msg['To'] = args.to
    sendEmail(args, msg)


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
    imap = getImap(args, args.imapInbox)
    mail = getEmail(args, args.imapInbox, messageNumber)
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
            mail = getEmail(args, args.imapInbox, messageNumber)
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
    mail = getEmail(args, args.imapInbox, args.messageNumber)
    branchName = getBranchFromSubject(mail['subject'])
    print(branchName)

createSubparser(subparser, checkMailForBranch, ["messageNumber","imapServer","imapPort","imapUser","imapPassword","imapInbox"])

# Check if Mail should trigger a Job

def checkMailForJobTrigger(args):
    mail = getEmail(args, args.imapInbox, args.messageNumber)
    if 'In-Reply-To' in mail:
        sys.exit(1)
    else:
        sys.exit()
    
createSubparser(subparser, checkMailForJobTrigger, ["messageNumber","imapServer","imapPort","imapUser","imapPassword","imapInbox"])

# to Failed Patch 
def failedPatchMail(args):
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
    sendEmail(args, msg)

createSubparser(subparser, failedPatchMail, ["smtpServer", "smtpPort", "smtpUser", "smtpPassword","badPatchPath"])

def getMailParameter(args):
    mail = getEmail(args, args.imapInbox, args.messageNumber)
    print(mail[args.mailParameter])

createSubparser(subparser, getMailParameter, ["imapServer","imapPort","imapUser","imapPassword","messageNumber","mailParameter", "imapInbox"])


def patchRejectionForBranch(args):
    mail = getEmail(args, args.imapInbox, args.messageNumber)
    env = os.environ
    subject = mail['Subject']
    env["PATCH_SUBJECT"] = subject
    env["TARGET_BRANCH"] = getBranchFromSubject(subject)
    msg = prepareMailFromJinja(env, "patchRejectionForBranch")
    msg['From'] = args.smtpUser
    msg['To'] = mail['Return-Path']
    msg['In-Reply-To'] = mail['Message-Id']
    msg['References'] = mail['Message-Id']
    sendEmail(args, msg)

createSubparser(subparser, patchRejectionForBranch, ["imapServer","imapPort","imapUser","imapPassword","messageNumber", "imapInbox", "smtpServer", "smtpPort", "smtpUser", "smtpPassword"])


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
