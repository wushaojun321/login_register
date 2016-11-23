#encoding:utf8
import sys
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
reload(sys)
sys.setdefaultencoding('utf8')

'''
1,验证是否为空
2，验证是否符合邮箱格式
'''

def send(to_mailaddr,title,text):
	result = {}
	app = Flask(__name__)
	app.config['MAIL_SERVER']='smtp.qq.com'
	app.config['MAIL_PORT']=587
	app.config['MAIL_USE_TLS']=True
	app.config['MAIL_USERNAME']='418836702'
	app.config['MAIL_PASSWORD']='vvbaojrkvldubhdg'
	# app.config['ADMINS'] = '418836702@qq.com'
	# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
	# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <418836702@qq.com>'
	mail = Mail(app)

	msg = Message(title,sender = '418836702@qq.com', 
					recipients=[to_mailaddr])
	msg.body = 'text body'
	msg.html = text
	try:
		with app.app_context():
			mail.send(msg)
		result['code'] = 100
		result['message']='邮件发送成功'
	except:
		result['code'] = 101
		result['message']='邮件发送失败'
	return result
if __name__ == '__main__':
	# try:
	# 	send('1@qq.com','好好学习','天天向上！')
	# except Error as e:
	# 	print e
	a = send('1@qq.com','好好学习','天天向上！')
	print a




