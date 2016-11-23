#encoding:utf8

import sys,re,time,datetime,random
from flask import Flask,render_template,request,session,url_for,redirect,flash

reload(sys)
sys.setdefaultencoding('utf8')

from models import message,mail,memory,user,db_text

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
	if session:
		return render_template('index.html')
	else:
		return redirect(url_for('login'))

@app.route('/message',methods = ['GET','POST'])
def send_message():
	result = {}
	if request.method == 'POST':	
		args = request.form.to_dict()
		if len(args['to_phonenumber']) == 0 or len(args['message_content']) == 0:
			result['code'] = 60
			result['message'] = '内容为空'
		else:
			m = message.Message(args['to_phonenumber'],args['message_content'])
			result = m.send()
		result = result['message']
	return render_template('message.html',result = result)

@app.route('/mail',methods = ['POST','GET'])
def send_mail():
	result = {}
	re_rule = r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z_]{0,10}.com'
	if request.method == 'POST':	
		args = request.form.to_dict()
		if len(args['to_mailaddr']) == 0 or len(args['mail_content']) == 0 or len(args['mail_title']) == 0:
			result['code'] = 102
			result['message'] = '内容为空'
		elif not re.match(re_rule,args['to_mailaddr']):
			result['code'] = 103
			result['message'] = '邮箱格式不正确'
		else:
			result = mail.send(args['to_mailaddr'],args['mail_title'],args['mail_content'])
			
		result = result['message']
	return render_template('mail.html',result = result)

@app.route('/memory',methods = ['POST','GET'])
def memory_monitor():
	while True:
		time.sleep(5)
		m = memory.Memory()
		virtual_memory = m.virtual_memory()#后面加.可以获得数据
		disk_memory = m.disk_memory()#dict{'total': 999964729344L, 'percent': 24.735764478639823, 'used': 247348920320L}
		# return str(disk_memory)
		# return render_template('memory.html',virtual_memory_total = virtual_memory.total,
		# 									virtual_memory_free = virtual_memory.free,
		# 									virtual_memory_percent = virtual_memory.percent,
		# 									disk_memory_total = disk_memory['total'],
		# 									disk_memory_free = disk_memory['used'],
		# 									disk_memory_percent = disk_memory['percent'])
		percent = '%0.2f' % (100-disk_memory['percent'])
		return render_template('memory.html',
								disk_free_percent = virtual_memory.percent)

@app.route('/login',methods=['POST','GET'])
def login():
	result = {}
	if request.method == 'POST':
		args = request.form.to_dict()
		u = user.User(args['phone'],args['passwd'])
		result = u.login()
		if result['code'] == 0:
			session['phone'] = args['phone']
			return redirect(url_for('index'))

		result = u.login()['message']
	return render_template('login.html',result =result)

@app.route('/loginout')
def loginout():
	if session:
		del session['phone']
	return redirect(url_for('login'))

@app.route('/reg',methods=['POST','GET'])
def reg():
	
	result = {}
	if request.method == 'POST':
		args = request.form.to_dict()
		if request.form.get('reg',None) == '发送验证码':
			verification = random.randint(100000,999999)
			d = {}
			d['en_phone'] = args['phone']  #这里必须字典传参，改User里的话太麻烦
			u = user.User(**d)
			if not u.phone_legal():
				result = {
						'code':61,
						'message':'手机号不合法！'
				}
			elif u.check_exist(args['phone']):
				result = {
						'code':59,
						'message':'手机号已经存在，请直接登录！'
				}
			else:
				m = message.Message(args['phone'],verification)
				send_result = m.send()
				if send_result['code'] == 0:
					result = {
						'code':60,
						'message':'验证码已经发送！'
					}
					session['verification'] = verification
					session['reg_phone'] = args['phone']
				else:
					result = {
						'code':62,
						'message':'验证码发送失败！'
					}
			return render_template('reg.html',result = result,verification=verification)
		elif request.form.get('reg',None) == '注册':
			if (len(args['phone']) == 0 or len(args['passwd']) == 0 or 
				len(args['confirm_passwd']) == 0 or len(args['class_type']) == 0 or 
				len(args['class_num']) == 0 or len(args['sex']) == 0 or 
				len(args['verification']) == 0):
				result = {
					'code': 51,
					'message':'接受到的注册信息不完整！'
				}
			elif not session:
				result = {
					'code':63,
					'message':'请进行手机验证！'
				}
			elif session['reg_phone'] != args['phone']:
				result = {
					'code':59,
					'message':'请用接收到验证码的手机注册！'
				}
			elif args['confirm_passwd'] != args['passwd']:
				result['code'] = 57
				result['message'] = '密码不一致'
			elif int(args['verification']) != int(session['verification']): #需要注意session的类型和args的类型
				result = {
					'code':58,
					'message':'验证码错误！'
				}
			else:
				reg_info = {'en_phone':args['phone'],
							'en_passwd':args['passwd'],
							'class_type':args['class_type'],
							'class_num':args['class_num'],
							'sex':args['sex']}
				r = user.User(**reg_info)
				result = r.reg()
			return render_template('reg.html',result = result)
		else:
			return '<h1>这是什么请求，你作弊！</h1>'
	else:
		return render_template('reg.html',result=result)

@app.route('/text')
def text_list():
	L = db_text.get_text()
	return render_template('text_list.html',L = L)

@app.route('/text/<text_id>')
def text_content(text_id):
	L = db_text.get_text()
	text = None
	n = 0
	for i in L:	
		if int(i[0]) == int(text_id):
			text = L[n]
		n += 1
	return render_template('text_content.html',text = text)

@app.route('/write_text',methods=['POST','GET'])
def write_text():
	result = None
	if request.method == 'POST':
		args = request.form.to_dict()
		args['date'] = str(datetime.datetime.now())[0:19]
		if len(args['content']) == 0 or len(args['title']) == 0:
			result = {
						'code': 302,
						'message':'不能为空'
			}	
		elif db_text.write_text(**args):
			return redirect(url_for('text_list'))
		else:
			result['code'] = 301
			result['message'] = '文章保存失败！'
	return render_template('write_text.html',result = result)

if __name__ == '__main__':
	app.secret_key = 'hehe'
	app.run(debug=True)

