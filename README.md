Based on my experience with UNIFI APs, sometimes some APs appear as disconnected, but they are able to respond to PINGs. In these cases, for the controller, the AP is down. We monitor our APs with nagios/iciga, but since they have no problems responding to ping requests, we do not receive any notification.

When this happens, if we open an ssh session to the AP, we can find messages in the /var/log/messages file with this text "failed to contact mcad".

I suspect that the problem is related to the schedule we apply to the APs. In the evenings we disable the wifi networks (WiFi Scheduler) and in the mornings we re-enable them. Whenever this problem appears, it is always first thing in the morning.

To solve the problem we have created the following script, which is in charge of monitoring this error in our APs, and when it finds the string 'failed to contact mcad' in the /var/log/messages file, it restarts the AP autonomously through ssh.

These are the parameters to customize:

- AP_LIST: In this list, you have to enter the IPs of your APs.
- AP_SSH_PASS: The ssh password that we have defined for our APs in the controller.

- MAIL_FROM: Address from which the notifications will be sent.
- MAIL_TO: Address to which the notifications will be sent.
- MAIL_REBOT_MESSAGE: Subject of the notification message.
- MAIL_BODY: Body of the notification message.
- SMTP_SERVER: Mail sending server
- SMTP_USER: User to be authenticated in the SMTP_SERVER server to send the mail.
- SMTP_PASS: Password of the SMTP_USER user.

This script uses sshpass, so it must be installed beforehand:  apt-get install sshpass
