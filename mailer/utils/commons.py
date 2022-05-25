import smtplib
import imaplib
from email.message import EmailMessage
import email
from jinja2 import  Environment, FileSystemLoader
import os
import re
import sys
from os import path
import shutil
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
        mailserver = smtplib.SMTP_SSL(host=args.smtpServer,port=args.smtpPort,context=context)
        mailserver.ehlo()
        mailserver.login(args.smtpUser, args.smtpPassword)
    except ssl.SSLCertVerificationError as e:
        print("SSL Certificate is not Verified, Try this SO Post: https://stackoverflow.com/a/58394602", file=sys.stderr)
        raise e
    return mailserver