#encoding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sql_header = ['phone','passwd','status','class_type','class_num','sex']
sql_info = {
					'host' : 'localhost',
					'user' : 'root',
					'passwd' : 'python123',
					'db' : 'user'
					}
sql_info_text = {
					'host' : 'localhost',
					'user' : 'root',
					'passwd' : 'python123',
					'db' : 'text',
					'charset':'utf8'
					}

result = {
			0: '登录OK',
			1: '手机号或者密码为空',
			2: '手机号不存在，请注册',
			3: '密码错误',
			4: '用户未激活'
		}
reg_info = {
			'en_phone':18710700958,
			'en_passwd':'python',
			'class_type' : 'linux',
			'class_num' : 3,
			'sex' : '女'
			}
#message info
smsbao_api = 'http://api.smsbao.com/sms'
smsbao_user = 'kumikoda'
smsbao_passwd = '1b2853a309fb00d6934ff7bcfce8d281'


#邮箱配置文件
# app.config['MAIL_SERVER']='smtp.qq.com'
# app.config['MAIL_PORT']=587
# app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USERNAME']='418836702'
# app.config['MAIL_PASSWORD']='vvbaojrkvldubhdg'