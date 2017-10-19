#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
    Date:    Thu Oct 19 19:56:58 CST 2017
    Author:  苏伟涛
    Version: 1.0
    Email:   13667831357aa@gmail.com
'''

import os
from Queue import Queue

'''
    @function 目标路径下的所有cpp文件放进队列里面
    @param queues 队列
    @param now_path 目标路径
'''
def listDir(queues, now_path):
    now_files =  os.listdir(now_path)
    for i in now_files:
        now_file = "%s/%s"%(now_path, i)
        if os.path.isdir(now_file):
            listDir(queues, now_file)
        elif now_file.rsplit('/', 1)[1].rsplit('.', 1)[1] == 'cpp' :
            queues.put(now_file)

'''
    @function 将队列中的所有文件的编码转为utf8
    @param queues 存有文件路径的队列
'''
def iconvFile(queues):
    while not queues.empty():
        ori_file =  queues.get()
        try:
            os.system('iconv -f GBK -t UTF-8 %s -o %s'%(ori_file, ori_file))
        except Exception as e:
            print str(e)

if __name__ == "__main__":
    queues = Queue(100)

    listDir(queues, '/root/Desktop/源代码/')
    iconvFile(queues)