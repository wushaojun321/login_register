#encoding:utf-8

import time
import re
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import db
import conf

def input_userdata(**reg_info):
	conn,cur = db.open_sql()
	print reg_info
	query = '''INSERT INTO USER (
				phone,
				passwd,
				class_type,
				class_num,
				sex
			)
			VALUES
				(
					{phone},
					'{passwd}',
					'{class_type}',
					{class_num},
					'{sex}'
				)
				'''.format(	phone = reg_info['en_phone'],
							passwd = md5(reg_info['en_passwd']),
							class_type = reg_info['class_type'],
							class_num = reg_info['class_num'],
							sex = reg_info['sex']
							)
	try:	
		cur.execute(query=query)
		conn.commit()
		cur.close();conn.close()
		return True
	except:
		return False
def get_userdata(phone):
	#以phone为索引拿出用户的所有数据
	data = None
	conn,cur = db.open_sql()
	query = "SELECT * FROM user WHERE phone LIKE {phone}".format(phone = phone)
	try:
		cur.execute(query = query)
		data = cur.fetchone()
	except:
		pass
	conn.commit()
	cur.close();conn.close()
	return data #(18710700957L, 'affaf271b3ebb2db157a04874259cdcb', 1L, 'python', 3L, '?')
def md5(passwd):
	#转换成MD5
	m = hashlib.md5()
	m.update(passwd)
	return m.hexdigest()

class User(object):
	def __init__(self, phone = None, passwd = None, **reg_info):
		self.phone = phone
		try:
			self.len_passwd = len(passwd)
			self.passwd = md5(passwd)
		except:
			pass
		
		self.reg_info = reg_info


	def check_login_complete(self):
		#判断登录时输入的数据是否完整
		if self.len_passwd == 0:
			return False
		else:
			return True

	def check_exist(self,phone):
		#判断用户名是否存在
		data = get_userdata(phone)
		if data == None:
			return False  #不存在
		else:
			return True	  #存在

	def check_login_passwd(self):
		#判断密码是否正确
		data = get_userdata(self.phone)[1]
		if data == self.passwd:
			return True
		else:
			return False
	def check_status(self):
		#判断是否激活
		data = get_userdata(self.phone)[2]
		if data == 1:
			return True
		else:
			return False
	def check_reg_complete(self):
		#判断注册条目是否齐全
		if conf.reg_info.keys() == self.reg_info.keys():
			return True
		else:
			return False
	def check_regcontent_complete(self):
		#判断注册内容是否为空
		if len(self.reg_info['en_passwd'])==0 or len(self.reg_info['class_type'])==0 or len(self.reg_info['sex'])==0:
			return False
		else:
			return True
	def phone_legal(self,phone = None):
		#判断手机号是否合法
		re_rule = r'1[3|4|5|7|8]\d{9}'
		if re.match(re_rule,str(self.reg_info['en_phone'])) == None:
			return False
		else:
			return True
	def passwd_legal(self):
		#判断密码是否合法
		if len(str(self.reg_info['en_passwd'])) >= 6 and str(self.reg_info['en_passwd']).isdigit() == False and str(self.reg_info['en_passwd']).isalpha() == False:
			return True
		else:
			return False

	def login(self):
		if  self.check_login_complete() == False:
			result = {
					'code':1,
					'message':conf.result.get(1,'手机号或者密码为空')
			}
		elif not self.check_exist(self.phone):
			result = {
					'code':2,
					'message':conf.result.get(2,'手机号不存在，请注册')
			}
		elif not self.check_login_passwd():
			result = {
					'code':3,
					'message':conf.result.get(3,'密码错误')
			}
		elif not self.check_status():
			result = {
					'code':4,
					'message':conf.result.get(4,'用户未激活')
			}
		else:
			result = {
					'code':0,
					'message':conf.result.get(0,'登录成功')
			}
		return result
	def reg(self):
		if not self.check_reg_complete():
			result = {
					'code':51,
					'message':conf.result.get(51,'接受到的注册信息不完整')			
			}
		elif not self.check_regcontent_complete():
			result = {
					'code':52,
					'message':conf.result.get(52,'注册信息不能为空')
			}
		elif not self.phone_legal():
			result = {
					'code':53,
					'message':conf.result.get(53,'手机号不合法')
			}
		elif self.check_exist(self.reg_info['en_phone']):
			result = {
					'code':54,
					'message':conf.result.get(54,'手机号已注册')
			}
		elif not self.passwd_legal():
			result = {
					'code':55,
					'message':conf.result.get(55,'密码不合法')
			}
		else:
			a = input_userdata(**self.reg_info)
			if a:
				result = {
						'code':50,
						'message':conf.result.get(50,'注册成功')
				}
			else:
				result = {
						'code': 56,
						'message': conf.result.get(56,'MySQLError,注册失败')
				}


		return result

	def activating(self):
		if not self.check_exist(self.phone):
			result = {
					'code':101,
					'message':conf.result.get(101,'激活用户不存在，请注册后再激活')
			}
		elif get_userdata(self.phone)[2] == 1:
			result = {
					'code':102,
					'message':conf.result.get(102,'用户已经激活，请直接登录')
			}
		else:
			conn,cur = db.open_sql()
			query = '''	UPDATE USER
						SET STATUS = 1
						WHERE
						phone = {phone}'''.format(phone = self.phone)
			try:	
				cur.execute(query=query)
				conn.commit()
				cur.close();conn.close()
				result = {
						'code':100,
						'message':conf.result.get(100,'激活成功')
				}
			except:
				result = {
						'code':103,
						'message':conf.result.get(103,'SQL原因，激活失败')
				}

		return result

if __name__ == '__main__':
	'''#测试check_exist()
	u = user(18710700957,'python123')
	print u.check_exist()
	'''

	'''测试check_login_passwd()
	u = user(18710700957,'python12')
	print u.check_login_passwd()
	'''

	'''测试login,功能正常
	u = user(18710700957,'python123')
	a = u.login()
	print a
	print a['message']
	'''

	'''测试注册
	reg_info = {
			'en_phone':18710700955,
			'en_passwd':'python123',
			'class_type' : 'linux',
			'class_num' : 3,
			'sex' : 'female'
			
			}
	u = user(**reg_info)
	a = u.reg()
	print a
	print a['message']  #就说他妈的注册两个号 调用了两次啊
	'''

	'''测试激活
	u = user(phone = 18710700955)
	a = u.activating()
	print a
	print a['message']
	'''
	u = User(18710700957)
	print u.check_exist(18710700957)