#Send Email

Python Command Line Interface (CLI) program to send email.


###Examples:

```
# Basic 
python SendEmail.py --smtp_host SMTP_HOST_MACHINE_NAME --to to@email.com --subject "Email Subject" --body "Email body main message" --from from@email.com
python SendEmail.py -H SMTP_HOST_MACHINE_NAME -t to@email.com -s "Email Subject" -b "Email body main message" -f from@email.com

# Basic with CC.
python SendEmail.py --smtp_host SMTP_HOST_MACHINE_NAME --to to@email.com --cc carbon.copy@email.com --subject "Email Subject" --body "Email body main message" --from from@email.com
python SendEmail.py -H SMTP_HOST_MACHINE_NAME -t to@email.com -c carbon.copy@email.com -s "Email Subject" -b "Email body main message" -f from@email.com

# Use files for arguments.  Commonly for email lists and large body message but all arguments accept a file path.
python SendEmail.py --smtp_host SMTP_HOST_MACHINE_NAME --to /home/sfwgeek/to.txt --subject "Email Subject" --body /home/sfwgeek/body.txt --from from@email.com
python SendEmail.py -H SMTP_HOST_MACHINE_NAME -t C:\home\to.txt -s "Email Subject" -b C:\home\body.txt -f from@email.com
python SendEmail.py --smtp_host SMTP_HOST_MACHINE_NAME --to /home/sfwgeek/to.txt --cc /home/sfwgeek/cc.txt --subject "Email Subject" --body /home/sfwgeek/body.txt --from from@email.com
python SendEmail.py --smtp_host /home/sfwgeek/smtp_host.txt --to /home/sfwgeek/to.txt --subject /home/sfwgeek/subject.txt --body /home/sfwgeek/body.txt --from /home/sfwgeek/from.txt
```

###py2exe:



###TODO:
1. Add BCC functionality.
2. Add HTML body functionality.
3. Add py2exe code and instructions.
