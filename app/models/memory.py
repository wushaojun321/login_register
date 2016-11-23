#encoding:utf8
import sys,psutil
reload(sys)
sys.setdefaultencoding('utf8')

class Memory():
	def virtual_memory(self):
		virtual = psutil.virtual_memory()
		return virtual
	def disk_memory(self):
		c = psutil.disk_usage('c:/')
		d = psutil.disk_usage('d:/')
		e = psutil.disk_usage('e:/')
		f = psutil.disk_usage('f:/')
		total = c.total +d.total +e.total +f.total
		used = c.used +d.used +e.used +f.used
		percent = used * 0.1 / total * 1000
		disk = {
				'total':total,
				'used':used,
				'percent':percent
		}
		return disk

# print psutil.virtual_memory()
# print psutil.disk_partitions()
# a = psutil.disk_usage('c:/')
# sdiskusage(total=85900390400L, used=61173452800L, free=24726937600L, percent=71.2)
if __name__ == '__main__':
	a = Memory()
	print type(a.disk_memory())
	print a.virtual_memory()
	# svmem(total=4239687680L, available=1404325888L, percent=66.9, used=2835361792L, free=1404325888L)