import gevent
from gevent import monkey
monkey.patch_all()

from gevent import Greenlet
import etcd
import random
import threading

client = etcd.Client()

def watchTask():
	print 'now watch...'
	def do():
		rVal = client.read('/nodes/abc', wait=True)
		print "!!!!!!!!!!!!!!!!!!!!!ChangeVal %s" % rVal

	t = threading.Thread(target=do)
	t.start()
	
	print 'now watch2...'

	print 'watch finished...'

def task1():

	for i in range(10):
		print 'now set...'
		setVal = random.randint(0,99)
		print 'real set - %s' % setVal
		client.set('/nodes/abc', setVal)
		print 'set ok - %s' % setVal
	print('Finished!!!!!!!')

def task2():
	def asyncGet():
		val = client.read('/nodes/abc')
		print 'get ok - %s' % val

	for i in range(10):
		print 'now get....'
		gevent.spawn(asyncGet).join()
	print('Finished!!!!!!! Task2')


gevent.joinall([
	gevent.spawn(watchTask),
	gevent.spawn(task1),
	gevent.spawn(task2)

	
])