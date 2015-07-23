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
	def asyncSet():
		setVal = random.randint(0,99)
		print 'real set - %s' % setVal
		client.set('/nodes/abc', setVal)
		print 'set ok - %s' % setVal

	for i in range(5):
		print 'now set...'
		Greenlet.spawn(asyncSet).join()
	print('Finished!!!!!!!')

def task2():
	def asyncGet():
		val = client.read('/nodes/abc')
		print 'get ok - %s' % val

	for i in range(5):
		print 'now get....'
		Greenlet.spawn(asyncGet).join()
	print('Finished!!!!!!! Task2')



gevent.sleep(1)

gevent.joinall([
	gevent.spawn(watchTask),
	gevent.spawn(task1),
	gevent.spawn(task2)

	
])