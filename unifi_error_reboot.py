#!/usr/bin/python3
# -*- coding: utf-8 -*-

#################################################################################################

import subprocess 

import smtplib
from email.mime.text import MIMEText
from email.header    import Header


AP_LIST = ['192.168.100.100','192.168.100.200','192.168.100.200']
AP_SSH_PASS = 'my_unifi_app_ssh_pass'
MAIL_FROM = 'myaddress@mydomain.eus'
MAIL_TO = ['myaddress@mydomain.eus']
MAIL_REBOT_MESSAGE = 'This AP has been rebooted'
MAIL_BODY = "This AP has been rebooted: AP_IP "
SMTP_SERVER = 'mail.mydomain.eus'
SMTP_USER = 'smtp-account@mydomain.eus'
SMTP_PASS = 'my_smtp_user_pass'

def send_mail(AP):
    sender = MAIL_FROM
    receivers = MAIL_TO
    body = MAIL_BODY

    body = body.replace("AP_IP", AP)

    msg = MIMEText(body,'plain','utf-8')
    msg['Subject'] = Header(MAIL_REBOT_MESSAGE + AP, 'utf-8')
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO

    try:
       smtpObj = smtplib.SMTP(SMTP_SERVER)
       smtpObj.login(SMTP_USER, SMTP_PASS)
       smtpObj.sendmail(sender, receivers, msg.as_string())
       print ("Successfully sent email")
    except Exception as e:
       print ("Error: unable to send email")
       print (e)
    finally:
       smtpObj.quit()


for ap in AP_LIST:
    COMMAND = ['sshpass', '-p', AP_SSH_PASS , 'ssh', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no', 'admin@'+ap, "/bin/cat /var/log/messages | grep 'reset-handler' | grep 'exited after' | grep 'with status 0' | grep 'Scheduling for restart'"]

    p1 = subprocess.Popen(COMMAND, stdout=subprocess.PIPE)
    b = str(p1.communicate()[0])
    print(b)
    c = b.split('\\n')

    count_lines = len(c)

    if count_lines > 1:
        print("Error")
        send_mail(ap)
        COMMAND = ['sshpass', '-p', AP_SSH_PASS, 'ssh', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no', 'admin@'+ap, "/sbin/reboot"]
        p1 = subprocess.Popen(COMMAND, stdout=subprocess.PIPE)
    else:
        print("OK")

