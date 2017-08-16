#!/usr/bin/env python
#coding=utf-8
#author=tazman
#function: gets proxy and test available

from bs4 import BeautifulSoup as BS
import requests
from optparse import OptionParser
import time
import os
import threading
from Queue import Queue
import re
from sys import stdout

def judgeAvail(parser, out_file, thread_count, page_count):
	out_path = os.path.realpath(out_file).rsplit('/', 1)[0]
	proxy_right_types = ['http', 'https', 'socks']

	if not os.path.isdir(out_path):
		print '[FAIL] out_file\'path is not exits'
		exit(-1)

	if thread_count < 1 or thread_count > 100:
		print '[FAIL] the thread_count is too small or too huge!(0 < thread_count < 100)'
		exit(-1)

	if page_count < 1 or page_count > 1000:
		print '[FAIL] page_count is too small or too huge!(0 < page_count < 1000)'
		exit(-1)

def toResQueue(res_queue, page_count):
	for i in range(1,page_count+1):
		URL = 'http://www.kuaidaili.com/free/inha/'+str(i)
		time.sleep(1)
		res_queue.put(requests.get(URL, headers={'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0'}))
		stdout.write('\r[SECCESS] read page: %d !!!'%res_queue.qsize())
		stdout.flush()

def proxySpider(res_queue, proxy_queue):
	while not res_queue.empty():
		soup = BS(res_queue.get().content, 'lxml')
		ips = soup.find_all(name='td', attrs={'data-title':'IP'})
		ports = soup.find_all(name='td', attrs={'data-title':'PORT'})
		for i in range(len(ips)):
			proxy_queue.put(ips[i].string+':'+ports[i].string)

def testProxy(proxy_queue, out_file):
	while not proxy_queue.empty():
		proxy = proxy_queue.get()
		if requests.get('https://www.baidu.com', proxies={'http' : proxy,}, timeout=6).status_code < 400:
			out_file.write(proxy+'\n')

def showTime(res_queue, proxy_queue):
	while not res_queue.empty() or not proxy_queue.empty():
		time.sleep(1)
		stdout.write('\r[STATUS] page:%5d == proxy:%5d'%(res_queue.qsize(), proxy_queue.qsize()))
		stdout.flush()

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-o', '--out_file', dest='out_file', type='string', default='./'+str(time.time()).split('.')[0]+'.txt', help='result will input the file example: /root/hello.txt')
	parser.add_option('-t', '--thread_count', dest='thread_count', type='int', default=10, help='set thread number to run example: 10, 20, 30')
	parser.add_option('-c', '--page_count', dest='page_count', type='int', default=300, help='spider page number example: 10, 100, 1000')
	options, args = parser.parse_args()

	out_file = options.out_file
	thread_count = options.thread_count
	page_count = options.page_count
	res_queue = Queue()
	proxy_queue = Queue()
	res_threads = []
	proxy_threads = []

	judgeAvail(parser, out_file, thread_count, page_count)
	out_file = open(out_file, 'w')

	toResQueue(res_queue, page_count)

	for i in range(thread_count):
		res_threads.append(threading.Thread(target=proxySpider, args=(res_queue, proxy_queue)))

	show_time_thread = threading.Thread(target=showTime, args=(res_queue, proxy_queue))
	show_time_thread.start()

	for i in range(thread_count):
		res_threads[i].start()

	for i in range(thread_count):
		res_threads[i].join()

	for i in range(thread_count):
		proxy_threads.append(threading.Thread(target=testProxy, args=(proxy_queue, out_file)))

	for i in range(thread_count):
		proxy_threads[i].start()

	for i in range(thread_count):
		proxy_threads[i].join()

	show_time_thread.join()
	out_file.close()
	print '\n[END] this is great!'
	