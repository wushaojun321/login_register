#encoding:utf8

import sys,requests,conf
reload(sys)
sys.setdefaultencoding('utf8')

class Message(object):
	def __init__(self,phone,content):
		self.phone = phone
		self.content = content
		self.smsbao_api = conf.smsbao_api
		self.smsbao_user = conf.smsbao_user
		self.smsbao_passwd = conf.smsbao_passwd
		self.err = {
            0: '发送成功',
            30: '密码错误',
            40: '账号不存在',
            41: '余额不足',
            42: '帐号过期',
            43: 'IP地址限制',
            50: '内容含有敏感词',
            51: '手机号码不正确'
        			}

	def send(self):
		params = {
				'u':self.smsbao_user,
				'p':self.smsbao_passwd,
				'm':self.phone,
				'c':self.content
				}
		try:
			result = {}
			r = requests.get(url = self.smsbao_api,
							params = params,
							timeout = 10)
			text = r.text
			if text.isdigit():
				a = int(text)
				if a in self.err:
					result['code'] = a
					result['message'] = self.err[a]
				else:
					result['code'] = 9999
					result['message'] = '接口未知错误！'
			result['phone'] = self.phone
			return result
		except Exception,e:
			result['code'] = 200
			result['message'] = str(e)
			return result 
if __name__ == '__main__':
	s = Message('1871','这个应该可以发吧？也是醉了！')
	print(s.send())

