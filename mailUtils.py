import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import os

#邮件参数，由host&user&pass组成
mail_env = os.environ['MAIL_ENV']
mail_value = mail_env.split('&')

mail_host = mail_value[0]
mail_user = mail_value[1]
mail_pass = mail_value[2]

receivers = [mail_user]

date = str(datetime.now().date()).replace('-', '')

def sendText(title, msg):

	message = MIMEText(msg, 'plain', 'utf-8')
	#设置显示邮件里的发件人
	message['From'] = Header('东哥发', 'utf-8')
	#设置显示邮件里的收件人
	message['To'] = Header('东哥收', 'utf-8')

	subject = date + title
	#设置主题和格式
	message['Subject'] = Header(subject, 'utf-8')

	try:
		smtpObj = smtplib.SMTP_SSL( mail_host, 465)
		smtpObj.login(mail_user, mail_pass)
		smtpObj.sendmail(mail_user, receivers, message.as_string())
		print("发送success")
	except smtplib.SMTPException as e:
		print("发送文本邮件失败")
		print(e)
		
		
def sendFile(title, path):
	message = MIMEText('', 'plain', 'utf-8')
	#设置显示邮件里的发件人
	message['From'] = Header('东哥发', 'utf-8')
	#设置显示邮件里的收件人
	message['To'] = Header('东哥收', 'utf-8')

	subject = date + title
	#设置主题和格式
	message['Subject'] = Header(subject, 'utf-8')

	try:
		smtpObj = smtplib.SMTP_SSL( mail_host, 465)
		smtpObj.login(mail_user, mail_pass)
		smtpObj.sendmail(mail_user, receivers, message.as_string())
		print("发送success")
	except smtplib.SMTPException as e:
		print("发送文件邮件失败")
		print(e)
	
