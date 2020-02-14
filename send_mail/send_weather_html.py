#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from lxml import etree

from get_chrome_history import get_history


def _weather_info(q_city):
    url = "http://i.tianqi.com/index.php?c=code&a=getcode&id=19&h=93&w=345&py=" + q_city
    resp = requests.get(url)
    resp.encoding = 'utf8'
    selector = etree.HTML(resp.text)
    city = selector.xpath('//div[@class="wtname"]/a/text()')[0]
    day1 = selector.xpath('string(//div[@id="day_1"]/div[1]/span)')
    img1 = selector.xpath('//div[@id="day_1"]/div[2]/img/@src')[0]
    wea1 = selector.xpath('//div[@id="day_1"]/div[3]/text()')[0]
    tem1f = selector.xpath('//div[@id="day_1"]/div[4]/font[1]/text()')[0]
    tem1t = selector.xpath('//div[@id="day_1"]/div[4]/font[2]/text()')[0]

    day2 = selector.xpath('string(//div[@id="day_2"]/div[1]/span)')
    img2 = selector.xpath('//div[@id="day_2"]/div[2]/img/@src')[0]
    wea2 = selector.xpath('//div[@id="day_2"]/div[3]/text()')[0]
    tem2f = selector.xpath('//div[@id="day_2"]/div[4]/font[1]/text()')[0]
    tem2t = selector.xpath('//div[@id="day_2"]/div[4]/font[2]/text()')[0]

    day3 = selector.xpath('string(//div[@id="day_1"]/div[1]/span)')
    img3 = selector.xpath('//div[@id="day_3"]/div[2]/img/@src')[0]
    wea3 = selector.xpath('//div[@id="day_3"]/div[3]/text()')[0]
    tem3f = selector.xpath('//div[@id="day_3"]/div[4]/font[1]/text()')[0]
    tem3t = selector.xpath('//div[@id="day_3"]/div[4]/font[2]/text()')[0]
    print(r'天气信息查询完毕.')
    return city, day1, day2, day3, img1, img2, img3, wea1, wea2, wea3, tem1f, tem1t, tem2f, tem2t, tem3f, tem3t


def _html_content(city='linfen'):
    today = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    weather = _weather_info(q_city=city)
    mail_content = """<html><head></head><body>  
    <center><font color="#0099ff">如果没有你，明天不值得期待，昨天不值得回忆。</font></center><br/>
    <font color="#0099ff">Today is """ + today + """</font><br/>
    <font><b>""" + weather[0] + """</b></font> :
    <table border="0" cellspacing="0" style="font-family:Arial;font-size: 12px"> 
        <tr align="center">
            <th style="padding-left: 20px;padding-right: 20px"><font style="padding-right: 5px;color: #f00">今天</font>
            <font color='#390'>""" + weather[1] + """</font></th>
            <th style="padding-right: 20px"><font style="padding-right: 5px;color: #f00">明天</font>""" + weather[2] + """</font></th>
            <th style="padding-right: 20px"><font style="padding-right: 5px;color: #06c">后天</font>""" + weather[3] + """</font></th>
        </tr>
        <tr align="center"> 
            <th><img src='http:""" + weather[4] + """' style='width:46px;height:46px'/></th> 
            <th><img src='http:""" + weather[5] + """' style='width:46px;height:46px'/></th> 
            <th><img src='http:""" + weather[6] + """' style='width:46px;height:46px'/></th> 
        </tr> 
        <tr align="center">
            <th>""" + weather[7] + """</th>
            <th>""" + weather[8] + """</th>
            <th>""" + weather[9] + """</th>
        </tr>
        <tr align="center"> 
            <th><font style="color: #f00">""" + weather[10] + """</font>～<font style="color: #390">""" + weather[11] + """</font></th>
            <th><font style="color: #f00">""" + weather[12] + """</font>～<font style="color: #390">""" + weather[13] + """</font></th>
            <th><font style="color: #f00">""" + weather[14] + """</font>～<font style="color: #390">""" + weather[15] + """</font></th>
        </tr> 
    </table></body></html>"""
    return mail_content


def send_mail(to_list, sub, body, file_name):
    me = "Big Jelly" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    # 添加正文
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # 添加附件
    if file_name:
        part = MIMEApplication(open(file_name, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(mail_host)
        server.set_debuglevel(1)
        server.ehlo(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(str(e))
        return False


mailto_list = ['jelly_xx@163.com']  # 收件人(列表)
mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user = "jelly_xx"  # 用户名
mail_pass = "xxxx"  # 密码
mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com
mail_title = '今日关注'  # 邮件标题


def main():
    file_name = get_history()
    flag = True
    while flag:
        flag = os.system('ping www.baidu.com >> nul')
        if flag == 0:
            if send_mail(to_list=mailto_list, sub=mail_title, body=_html_content(city='linfen'), file_name=file_name):
                flag = False
                print("done.")
            else:
                print("failed!")
        else:
            time.sleep(300)


if __name__ == '__main__':
    main()
