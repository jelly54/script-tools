#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
import json
import platform 
import getpass
import os
import re
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def get_PCinfo():
	usname = getpass.getuser()
	node = platform.node()			# 获取计算机的网络名
	plat = platform.platform() 		# 获取操作系统名称及版本号
	machine = platform.machine()		# 获取计算机类型
	processor = platform.processor() 		# 获取计算机处理器信息
	return 'computerInfo：\n\tuserName：'+str(usname)+'\n\thostName：'+str(node)+'\n\toperSystem：'+str(plat)+'\n\tsystemYype：'+ str(machine)+'\n\tpocessInfo：'+str(processor).replace(',','-')


def get_weather():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Referer": "http://www.weather.com.cn/weather40d/101050101105.shtml",
    }
    resp = requests.get('http://forecast.weather.com.cn/town/weather1dn/101050101105.shtml#input', headers=headers)
    resp.encoding = 'utf8'
    selector = etree.HTML(resp.text)
    # 当前天气
    now_time = selector.xpath('//div[@class="time"]/span/text()')[0]
    now_wea = selector.xpath('//div[@class="weather dis"]/text()')[0]
    now_temp = selector.xpath('//div[@class="tempDiv"]/span/text()')[0] + ' ℃'
    temp_min = selector.xpath('//div[@id="minTempDiv"]/span/text()')[0]
    temp_max = selector.xpath('//div[@id="maxTempDiv"]/span/text()')[0]
    wind_lv = selector.xpath('//div[@class="todayLeft"]/p/span/text()')[0]
    sd_lv = selector.xpath('//div[@class="todayLeft"]/p/span/text()')[1]
    str = '%s：\n    香坊区:  %s  %s\n    全天气温：%s - %s\n    %s\n    %s' % (now_time, now_wea, now_temp, temp_min, temp_max, wind_lv, sd_lv)
    # print str
    # 当天天气
    hours_weather = '今天天气：\n|  时间 | 天气 | 温度 | 风力\n'
    hours_weather_part = json.loads(re.findall('forecast_1h =(.*?);', resp.text)[0])
    for hour in hours_weather_part:
        h_time = hour['time']
        h_wea = hour['weather']
        h_temp = hour['temp']
        h_wind = hour['windD'] + ' ' + hour['windL']
        hours_weather += '| %s:00 |%-5s| %2d℃ | %s\n' % (h_time, h_wea, h_temp, h_wind)
    # print hours_weather
    # 未来七天天气
    day_resp = requests.get('http://forecast.weather.com.cn/town/weathern/101050101105.shtml', headers=headers)
    day_resp.encoding = 'utf8'
    day_selector = etree.HTML(day_resp.text)
    days_weather = '未来七天天气：\n'
    for i in range(2, 9):
        date = day_selector.xpath('//ul[@class="date-container"]/li[{}]/p/text()'.format(i))[0]
        day = day_selector.xpath('//ul[@class="date-container"]/li[{}]/p/text()'.format(i))[1]
        weather = day_selector.xpath('//ul[@class="blue-container backccc"]/li[{}]/p/text()'.format(i))[0].strip()
        wind1 = day_selector.xpath('//ul[@class="blue-container backccc"]/li[{}]/div/i/@title'.format(i))[0]
        wind2 = day_selector.xpath('//ul[@class="blue-container backccc"]/li[{}]/div/i/@title'.format(i))[0]
        wind_lv = day_selector.xpath('//ul[@class="blue-container backccc"]/li[{}]/p/text()'.format(i))[1].strip()
        days_weather += '%s(%-4s) |%-8s|%+7s转%s %s\n' % (date, day, weather, wind1, wind2, wind_lv)
    return str , hours_weather, days_weather


def send_mail(to_list,sub,content):
	me="Big Jelly"+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(content,'plain','utf-8')
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)                            #连接服务器
		server.login(mail_user,mail_pass)               #登录操作
		server.sendmail(me, to_list, msg.as_string())
		server.close()
		return True
	except Exception, e:
		print str(e)
		return False

mailto_list=['xxxx@163.com','xxxx@163.com']           #收件人(列表),'
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user="yourname"                           #用户名
mail_pass="yourpass"                             #密码
mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com

if __name__ == '__main__':
	ffff = True
	while ffff:
		flag = os.system('ping www.baidu.com >> nul')# 测试网络是否连接，未连接就sleep五分钟
		if flag==0:
			for i in range(1):                             #发送1封，上面的列表是几个人，这个就填几
				mesg = get_PCinfo()+'\n\n'+get_weather()[0]+'\n\n'+get_weather()[1]+'\n\n'+get_weather()[2]
				if send_mail(mailto_list,"今日你关注的消息",mesg):  #邮件主题和邮件内容
					#这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
					# print "done!"
					ffff = False
				else:
					print "failed!"
		else:
			time.sleep(300)