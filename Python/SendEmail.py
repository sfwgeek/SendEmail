#! /usr/bin/env python2.7
# vim: et sw=4 ts=4:
"""
DESCRIPTION:
    A Command Line Interface (CLI) program to send email.
    If a program argument is a file path and the file exists, the file lines will be used with leading and trailing white space removed.
    When supplying multiple email addresses for an argument, a comma should be used to separate them.
    Arguments with spaces should be enclosed in double quotes (").
AUTHOR:
    sfw geek
NOTES:
    <PROG_NAME> = ProgramName
    <FILE_NAME> = <PROG_NAME>.py = ProgramName.py

    Static Analysis:
        pychecker.bat <FILE_NAME>
        pylint <FILE_NAME>
    Profile code:
        python -m cProfile -o <PROG_NAME>.prof <FILE_NAME>
    Vim:
        Remove redundant trailing white space: '\s\+$'.
    Python Style Guide:
        http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
    Docstring Conventions:
        http://www.python.org/dev/peps/pep-0257
"""


# TODO:
#   Implement BCC functionality (FUNC_BCC).


# FUTURE STATEMENTS (compiler directives).
# Enable Python 3 print() functionality.
from __future__ import print_function


# VERSION.
# http://en.wikipedia.org/wiki/Software_release_life_cycle
__version__ = '2014.03.15.01' # Year.Month.Day.Build (YYYY.MM.DD.BB).
__release_stage__ = 'General Availability (GA)' # Phase.


# MODULES.
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Imports_formatting
# Standard library imports.
import argparse
import datetime
import email.mime.multipart
import email.mime.text
import email.utils
import os
import smtplib
import sys


# CONSTANTS.
PROGRAM_NAME = sys.argv[0]

# Linux/Unix programs generally use 2 for command line syntax errors and 1 for all other kind of errors.
SYS_EXIT_CODE_SUCCESSFUL = 0
SYS_EXIT_CODE_GENERAL_ERROR = 1
SYS_EXIT_CODE_CMD_LINE_ERROR = 2

COMMA_SPACE = email.utils.COMMASPACE


# DEFINITIONS.
def usage():
    """Return string detailing how this program is used."""

    return '''
    A Command Line Interface (CLI) program to send email.
    If a program argument is a file path and the file exists, the file lines will be used with leading and trailing white space removed.
    When supplying multiple email addresses for an argument, a comma should be used to separate them.
    Arguments with spaces should be enclosed in double quotes (").'''

def getProgramArgumentParser():
    """Return argparse object containing program arguments."""

    argParser = argparse.ArgumentParser(description=usage())

    # Mandatory parameters (though not set as required=True or can not use -V on own).
    mandatoryGrp = argParser.add_argument_group('mandatory arguments', 'These arguments must be supplied.')
    mandatoryGrp.add_argument('-b', '--body', action='store', dest='body', type=str,
        help='Body of email.  All lines from file used if file path provided.')
    mandatoryGrp.add_argument('-f', '--from', action='store', dest='frm', type=str,
        help='Email sender (source/from).  Only first line of file used if file path provided.')
    mandatoryGrp.add_argument('-H', '--smtp_host', action='store', dest='smtphost', type=str,
        help='Name of SMTP host used to send email.  Only first line of file used if file path provided.')
    mandatoryGrp.add_argument('-s', '--subject', action='store', dest='subject', type=str,
        help='Subject of email.  Only first line of file used if file path provided.')
    mandatoryGrp.add_argument('-t', '--to', action='store', dest='to', type=str,
        help='Recipient(s) of email (destination).  One email address per line if file path provided.')

    # Optional parameters.
    optionalGrp = argParser.add_argument_group('extra optional arguments', 'These arguments are not mandatory.')
    optionalGrp.add_argument('-c', '--cc', action='store', dest='cc', type=str,
        help='Recipient(s) to be Carbon Copied (CC).  One email address per line if file path provided.')
    # TODO: FUNC_BCC
    #optionalGrp.add_argument('-B', '--bcc', action='store', dest='bcc', type=str,
    #    help='Who the email is to be Blind Carbon Copied (BCC) to.  One email address per line if file path provided.')
    optionalGrp.add_argument('-d', '--debug', action='store_true', dest='debug',
        help='Increase verbosity to help debugging.')
    optionalGrp.add_argument('-D', '--duration', action='store_true', dest='duration',
        help='Print to standard output the programs execution duration.')
    optionalGrp.add_argument('-V', '--version', action='store_true', dest='version',
        help='Print the version number to the standard output.  This version number should be included in all bug reports.')

    return argParser

def printVersionDetailsAndExit():
    """Print to standard output programs version details and terminate program."""

    msg = '''
NAME:
    {0}
VERSION:
    {1}
    {2}'''.format(PROGRAM_NAME, __version__, __release_stage__)
    print(msg)
    sys.exit(SYS_EXIT_CODE_SUCCESSFUL)

def getDaySuffix(day):
    """Return st, nd, rd, or th for supplied day."""

    if 4 <= day <= 20 or 24 <= day <= 30:
        return 'th'
    return ['st', 'nd', 'rd'][day % 10 - 1]

def printProgramStatus(started, stream=sys.stdout):
    """Print program duration information."""

    NEW_LINE = '\n'
    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f (%a %d{0} %b %Y)'
    finished = datetime.datetime.now()
    delta = finished - started
    dateTimeStr = started.strftime(DATE_TIME_FORMAT.format(getDaySuffix(started.day)))
    msg = '{1}Started:  {0}{1}'.format(dateTimeStr, NEW_LINE)
    dateTimeStr = finished.strftime(DATE_TIME_FORMAT.format(getDaySuffix(finished.day)))
    msg += 'Finished: {0}{1}'.format(dateTimeStr, NEW_LINE)
    msg += 'Duration: {0} (days hh:mm:ss:ms)'.format(delta)
    print(msg, file=stream)

def getEmailPart(valueOrFilePath, oneLineEmailPart=False):
    """Return list of file lines if valueOrFilePath parameter is file path,
    otherwise return parameter value.
    Leading and trailing white space is removed from file lines or parameter value.
    If oneLineEmailPart is true, only the first line of the file is returned if valueOrFilePath is a file."""

    if os.path.isfile(valueOrFilePath):
        # File path has been supplied, get list of trimmed lines from file.
        data = []
        with open(valueOrFilePath) as srcFO:
            for srcLine in srcFO:
                data.append(srcLine.strip())
        if oneLineEmailPart:
            # Only return first line.
            return data[0]
        return data
    if valueOrFilePath:
        return str(valueOrFilePath).strip()
    return ''

def main():
    """Program entry point."""

    # Store when program started.
    started = datetime.datetime.now()

    # Get parameters supplied to application.
    argParser = getProgramArgumentParser()
    args = argParser.parse_args()

    # Logic for displaying version details or program help.
    if args.version:
        printVersionDetailsAndExit()
    if not (args.smtphost and args.to and args.frm and args.subject and args.body):
        if args.version:
            printVersionDetailsAndExit()
        argParser.print_help()
        sys.exit(SYS_EXIT_CODE_CMD_LINE_ERROR)

    # Process program arguments to get email parts.
    # From can only have one value regardless if stored in file or not (first line in file used).
    fromVal = getEmailPart(args.frm, oneLineEmailPart=True)
    toData = getEmailPart(args.to)
    subjectVal = getEmailPart(args.subject, oneLineEmailPart=True)
    bodyData = getEmailPart(args.body)
    smtpHostVal = getEmailPart(args.smtphost, oneLineEmailPart=True)

    # Build multipart MIME message (email).
    multipartMimeMsg = email.mime.multipart.MIMEMultipart()
    multipartMimeMsg['Date'] = email.utils.formatdate(localtime=True)
    multipartMimeMsg['From'] = fromVal
    multipartMimeMsg['To'] = COMMA_SPACE.join(toData)
    multipartMimeMsg['Subject'] = subjectVal
    multipartMimeMsg.attach(email.mime.text.MIMEText(email.utils.CRLF.join(bodyData)))

    # Process optional arguments.
    if args.cc:
        ccData = getEmailPart(args.cc)
        multipartMimeMsg['Cc'] = COMMA_SPACE.join(ccData)
        toData.extend(ccData) # TODO: check?
    # TODO: FUNC_BCC
    #if args.bcc:
    #    bccData = getEmailPart(args.bcc)
    #    multipartMimeMsg['Bcc'] = COMMA_SPACE.join(bccData)
    #    toData.extend(bccData) # TODO: similar to CC but is blindness enforced?

    # Python 3.3 supports with statement (context manager) for smtplib.SMTP().
    # http://docs.python.org/dev/library/smtplib.html
    # with smtplib.SMTP(smtpHostVal) as smtpSvr:
    smtpSvr = None
    try:
        smtpSvr = smtplib.SMTP(smtpHostVal)
        if args.debug:
            # Increase display verbosity.
            smtpSvr.set_debuglevel(1)
        smtpSvr.sendmail(fromVal, toData, multipartMimeMsg.as_string())
    finally:
        smtpSvr.quit()

    if args.duration:
        printProgramStatus(started)


# Program entry point.
if __name__ == '__main__':
    main()
