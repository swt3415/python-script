#!/usr/bin/env python
#coding:utf-8
#author:tazman
#version:1.0

import time
from optparse import OptionParser

def writeFile(options, parser):
	out_file = open(options.out_file, 'w')
	years = options.years.split('-')
	months = options.months.split('-')
	days = options.days.split('-')

	if len(years) != 2 or len(months) != 2 or len(days) != 2:
		parser.print_help()
		print '===you should input: 1990-2017, 1-12, 1-31 eg.==='
		print '===please reinput==='
		exit(-1)

	year0 = int(years[0])
	year1 = int(years[1])+1
	month0 = int(months[0])
	month1 = int(months[1])+1
	day0 = int(days[0])
	day1 = int(days[1])+1

	if year0 < 0 or year1 > 10000:
		parser.print_help()
		print '===you input [YEAR-BETWEEN] number in bad.==='
		print '===please reinput==='
	if month0 < 1 or month1 > 13:
		parser.print_help()
		print '===you input [MONTH-BETWEEN] number in bad.==='
		print '===please reinput==='
	if day0 < 1 or day1 > 32:
		parser.print_help()
		print '===you input [DAY-BETWEEN] number in bad.==='
		print '===please reinput==='

	for i in range(year0, year1):
			for j in range(month0, month1):
		            for k in range(day0, day1):
		                if j < 10:
		                    month = '0'+str(j)
		                else:
		                    month = str(j)
		                if k < 10:
		                    day = '0'+str(k)
		                else:
		                    day = str(k)

		                if j in [4,6,9,11]:
		                    if k == 31:
		                    	continue
		                elif j == 2:
		                    if i % 4 == 0:
		                    	if k > 29:
		                    		continue
		                    else:
		                    	if k > 28:
		                    		continue

		                out_file.write(str(i)+month+day+'\n')

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-o', '--output', dest='out_file', type='string', default='./'+str(time.time()).split('.')[0]+'.txt', help='will be output file')
	parser.add_option('-y', '--year-between', dest='years', type='string', default='1990-2017', help='please input:1990-2017 eg.')
	parser.add_option('-m', '--month-between', dest='months', type='string', default='1-12', help='please input:1-12 eg.')
	parser.add_option('-d', '--day-between', dest='days', type='string', default='1-31', help='please input:1-31 eg.')
	options, args = parser.parse_args()

	writeFile(options, parser)

