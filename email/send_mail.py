from __future__ import print_function
import smtplib
from email.mime.text import MIMEText
import configparser

cf = configparser.ConfigParser(allow_no_value=True)
cf.read('config.ini')
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 25

def send_method(user, pwd, to, subject, text):
  msg = MIMEText(text)
  msg['From'] = user
  msg['To'] = to
  msg['Subject'] = subject

  smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
  print('Connecting To Mail Server.')
  try:
    smtp_server.ehlo()
    print('Starting Encrypted Seccion.')

    smtp_server.starttls()
    smtp_server.ehlo()
    print('Logging Into Mail Server')
    smtp_server.login(user, pwd)
    print('Sending Mail.')
    smtp_server.sendmail(user, to, msg.as_string())
  except Exception as err:
    print('Sending Mail Failed: {0}'.format(err))
  finally:
    smtp_server.quit()

def send_mail():

  #读取扫描结果文件的内容，作为邮件正文
  f = open(cf.get('Basic','ResultFile'))
  content = f.read()
  f.close()

  #发送邮件
  send_method(cf.get('Mail', 'SendMailbox'), cf.get('Mail', 'Password'),
              cf.get('Mail', 'ReceiveMailbox'), 'Important', content)
