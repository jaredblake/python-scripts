#!/usr/bin/python
# Author: Andrea Veri <av@gnome.org>
# Target host: chooser.gnome.org
# Description: script to automatize new Prosody user creation at jabber.gnome.org. Usage as
# follows: 'python prosody.py username email'. Example: 'python prosody.py av av@gnome.org'.
# TODO: Add some exception handling in the case the prosody daemon isn't running or accepting
# new user's creation.

import random
import string
import pexpect
from email.mime.text import MIMEText
import smtplib
import sys

def create_prosody_account():

    username = sys.argv[1]
    email = sys.argv[2]

    s = string.lowercase+string.digits 
    random_password = ''.join(random.sample(s, 10))

    child = pexpect.spawn ('prosodyctl adduser %s@jabber.gnome.org' % (username))
    child.expect ('Enter new password: ')
    child.sendline ('%s' % random_password)
    child.expect ('Retype new password: ')
    child.sendline ('%s' % random_password)

    message = """
Hi,

as requested, your Jabber account at GNOME.org has  been created, the details:

User: %s@jabber.gnome.org
Password: %s

Please update the password as soon as you can by using the Gajim
client. Unfortunately this feature is not yet available on Empathy. See
https://bugzilla.gnome.org/show_bug.cgi?id=576999 for more details. """ % (username, random_password)

    try:
        msg = MIMEText(message)
        msg['Subject'] = "Your Jabber account at GNOME.org"
        msg['From']    = "accounts@gnome.org"
        msg['To']      = "%s" % (email)
        server = smtplib.SMTP("localhost")
        server.sendmail (msg['From'], msg['To'], msg.as_string())
        server.quit ()
        print "Successfully sent email to %s" % (email)
    except smtplib.SMTPException:
        print "ERROR: I wasn't able to send the email correctly, please check /var/log/maillog!"


create_prosody_account()