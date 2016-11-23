#encoding:utf8

from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/message',methods = ['GET','POST'])
def message():
	if request.method == 'POST'
	return render_template('message.html')

if __name__ == '__main__':
	app.run(debug = True)


