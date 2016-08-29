#	captcha has been removed from login process since 2016 sum	#

#	To order a course: 
#		input username and password as global variables
#		input courseid as variable in main function
#	To order courses of other types, change kcsx in query string params and coresponding position in request urlencoded
#		gongxuanke		4
#		ziyouxuanxiu	2

import urllib.request
import requests
import re
import os
import sys
import time

username = ''
password = ''

class USTC:
	def __init__(self):
		self.s = requests.Session()
		self.baseheaders = {
			'Accept'					:	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
			'Accept-Language'			:	'zh-CN,zh;q=0.8', 
			'Cache-Control'				:	'max-age=0', 
			'Connection'				:	'keep-alive', 
			'Content-Type'				:	'application/x-www-form-urlencoded', 
			'Origin'					:	'http://mis.teach.ustc.edu.cn', 
			'Referer'					:	'http://mis.teach.ustc.edu.cn/', 
			'Upgrade-Insecure-Requests'	:	'1', 
			'User-Agent'				:	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
		}
#-------init-------#
		
	def login(self):
		headers_ustc = self.baseheaders.copy()
		del headers_ustc['Content-Type']
		del headers_ustc['Origin']
		del headers_ustc['Referer']
		self.s.get('http://mis.teach.ustc.edu.cn/', headers = headers_ustc)
		headers_user = self.baseheaders.copy()
		data_user = {
			'userbz'					:	's'
		}
		self.s.post('http://mis.teach.ustc.edu.cn/userinit.do', data = data_user, headers = headers_user)
		while True:
			headers_login = self.baseheaders.copy()
			headers_login['Referer'] += 'userinit.do'
			data_login = {
				'userbz'					:	's', 
				'hidjym'					:	'', 
				'userCode'					:	username, 
				'passWord'					:	password
			}
			resp = self.s.post('http://mis.teach.ustc.edu.cn/login.do', data = data_login, headers = headers_login)
			if 'Expires' in resp.headers:
				break
			else:
				print('wrong captcha')
		headers_loginhtml = self.baseheaders.copy()
		del headers_loginhtml['Cache-Control']
		del headers_loginhtml['Content-Type']
		headers_loginhtml['Referer'] += 'login.do'
		self.s.get('http://mis.teach.ustc.edu.cn/bt_top.do', headers = headers_loginhtml)
		self.s.get('http://mis.teach.ustc.edu.cn/left.do', headers = headers_loginhtml)
#-------login-------#

	def logout(self): 
		headers_left = self.baseheaders.copy()
		del headers_left['Cache-Control']
		del headers_left['Content-Type']
		del headers_left['Origin']
		headers_left['Referer'] += 'login.do'
		self.s.get('http://mis.teach.ustc.edu.cn/quit.do', headers = headers_left)


	def checkscore(self, term):
		headers_left = self.baseheaders.copy()
		del headers_left['Cache-Control']
		del headers_left['Content-Type']
		headers_left['Referer'] += 'left.do'
		self.s.get('http://mis.teach.ustc.edu.cn/initquerycjxx.do', headers = headers_left)
		headers_check = self.baseheaders.copy()
		headers_check['Referer'] += 'initquerycjxx.do'
		data_check = {
			'xuenian'					:	term, 
			'chaxun'					:	'', 
			'px'						:	'1', 
			'zd'						:	'0'
		}
		check = self.s.post('http://mis.teach.ustc.edu.cn/querycjxx.do', data = data_check, headers = headers_check)
		# here is a time delay on the server
		check = check.text
		table = re.findall(r'<tr class=\"bg\">(.*?)</tr>', check, re.S)
		items = []
		for item in table:
			items.append(re.findall('align=\"center\" class=\"bg\">(.*?)</td>', item))
		items = items[1:]
		return items
#-------check-score-------#

	def searchbykw(self, keyword):
		headers_left = self.baseheaders.copy()
		del headers_left['Cache-Control']
		del headers_left['Content-Type']
		del headers_left['Origin']
		headers_left['Referer'] += 'init_st_xk_dx.do'
		geturl = headers_left['Referer'] + '?' + 'qr_queryType' + '=' + 'null' + 'xnxq' + '=' + '20161' + 'seldwdm' + '=' + 'null' + 'selkkdw' + '=' + '' + 'sjpdmlist' + '=' + '' + 'seyxn' + '=' + '2016' + 'seyxq' + '=' + '1' + 'queryType' + '=' + '4' + 'rkjs' + '=' + '' + 'kkdw' + '=' + '' + 'kcmc' + '=' + keyword
		params = {
			'qr_queryType'				:	'null', 
			'xnxq'						:	'20161', 
			'seldwdm'					:	'null', 
			'selkkdw'					:	'', 
			'sjpdmlist'					:	'', 
			'seyxn'						:	'2016', 
			'seyxq'						:	'1', 
			'queryType'					:	'4', 
			'rkjs'						:	'', 
			'kkdw'						:	'', 
			'kcmc'						:	keyword
		}
		rsp = self.s.get(geturl, params = params, headers = headers_left)
		rsp = rsp.text
		print(rsp)
		table = re.findall(r'<table id=\"dxkctable1\"(.*?)</div>\s*</form>\s*</body>\s*</html>', rsp, re.S)[0]
		tr = re.findall(r'<tr bgcolor=\"DEEDF8\">(.*?)</tr>', table, re.S)
		items = []
		for item in tr:
			items.append(re.findall(r'<td.*?>\s*(.*?)\s*</td>', item, re.S))
		items[0] = [re.findall(r'<b>(.*?)</b>', i, re.S)[0] for i in items[0]]
		for i in range(1, len(items)):
			items[i][2] = re.findall(r'<font color=blue>(.*?)</font>', items[i][2], re.S)[0]
			items[i][3] = re.findall(r'<font color=blue>(.*?)</font>', items[i][3], re.S)[0]
		print(items)
#-------search-------#

#-------type-4-only(gongxuan)-------#
	def orderbycourseid(self, courseid):
		headers_left = self.baseheaders.copy()
		del headers_left['Cache-Control']
		del headers_left['Content-Type']
		del headers_left['Origin']
		headers_left['Referer'] += 'init_st_xk_dx.do'
		params = {
			'xnxq'				:	'20161', 
			'kcbjbh'			:	courseid, 
			'kcid'				:	'17186', 
			'kclb'				:	'F',  
			'kcsx'				:	'4', 
			'cxck'				:	'0', 
			'zylx'				:	'01', 
			'gxkfl'				:	'null', 
			'xlh'				:	'1', 
			'sjpdm'				:	'44', 
			'kssjdm'			:	'null'
		}
		geturl = 'http://mis.teach.ustc.edu.cn/xkgcinsert.do?xnxq=20161&kcbjbh=' + courseid + '&kcid=17186&kclb=F%20&kcsx=4&cxck=0&zylx=01&gxkfl=null&xlh=1&sjpdm=44&kssjdm=null'
		rsp = self.s.get(geturl, params = params, headers = headers_left)
		if rsp.text[0] == 'D':
			return True
		elif rsp.text[0] == '9':
			return False
		else:
			print('unknown type in response')
			return True
#-------order-course-------#

if __name__ == '__main__':
	courseid = ''
	ustc = USTC()
	rs = False
	while True:
		ustc.login()
		print('Ordering course: ' + courseid + '...')
		for i in range(60): 
			rs = ustc.orderbycourseid(courseid)
			if rs == True: 
				print('Successfully ordered. ')
				break
			else:
				print(time.ctime())
				time.sleep(10)
		ustc.logout()
		if rs == True:
			break

	
