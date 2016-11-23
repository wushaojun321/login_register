#encoding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb

import db,conf

def open_sql_text():
	db = MySQLdb.connect(**conf.sql_info_text)
	cur = db.cursor()
	return db,cur

def get_text():
	conn,cur = open_sql_text()
	query = 'SELECT * FROM text'
	try:
		cur.execute(query = query)
		data = cur.fetchall()
		conn.commit()
		cur.close();conn.close()
		return data
	except:
		return False
def write_text(**args):
	conn,cur = open_sql_text()
	query = '''INSERT INTO text (title, date, content)
			VALUES
				(
					'{title}',
					'{date}',
					'{content}'
				)'''.format(title = args['title'],
							date = args['date'],
							content = args['content'])
	try:
		cur.execute(query = query)
		conn.commit()
		cur.close();conn.close()
		return True
	except:
		return False

if __name__ == '__main__':
	'''测试读取
	conn,cur = open_sql_text()
	query = 'SELECT * FROM text'
	cur.execute(query = query)
	data = cur.fetchall()
	conn.commit()
	cur.close();conn.close()
	print data
	'''
	'''测试写入	
	conn,cur = open_sql_text()
	query = "INSERT INTO text (title,date,content) VALUES ('测试','2016-10-25 20:25:33','正文测试')"
	cur.execute(query = query)
	conn.commit()
	cur.close();conn.close()
	'''
	'''测试get_text
	text = get_text()
	for i in text[0]:
		print i
	'''
	'''测试write
	args = {
			'title':'再测试一下',
			'date':'2016-10-25 20:43:16',
			'content':'好了吧？'
	}
	print write_text(**args)
	'''


