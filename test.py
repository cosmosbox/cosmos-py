import gevent
from gevent import thread
from gevent import monkey
#monkey.patch_thread()

from gevent import Greenlet
import etcd
import random

client = etcd.Client()

def watchTask():
	print 'now watch...'

	rVal = client.read('/nodes/abc', wait=True)
	print "!!!!!!!!!!!!!!!!!!!!!ChangeVal %s" % rVal

	print 'now watch2...'

	print 'watch finished...'

def task1():
	def asyncSet():
		setVal = random.randint(0,99)
		client.set('/nodes/abc', setVal)
		print 'set ok - %s' % setVal

	for i in range(5):
		print 'now set...'
		Greenlet.spawn(asyncSet).start()
	print('Finished!!!!!!!')

def task2():
	def asyncGet():
		val = client.read('/nodes/abc')
		print 'get ok - %s' % val

	for i in range(5):
		print 'now get....'
		Greenlet.spawn(asyncGet).start()
	print('Finished!!!!!!! Task2')


thread.start_new_thread(watchTask)

gevent.joinall([
	

	gevent.spawn(task1),
	gevent.spawn(task2)
	
])