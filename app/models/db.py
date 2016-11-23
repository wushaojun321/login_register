#encoding:utf-8

import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import conf

def open_sql():
	#连接数据库
	db = MySQLdb.connect(**conf.sql_info)
	cur = db.cursor()
	return db,cur
if __name__ == '__main__':
	#连接数据库测试程序
	db,cur = open_sql()
	cur.execute("SELECT * FROM user WHERE phone LIKE 18710700957")

	print cur.fetchall()
	db.commit()
	cur.close();db.close()

