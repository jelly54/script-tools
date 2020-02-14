#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/10 8:50
# @Author  : Jelly
# @File    : checkin_tool.py
import json
import time
from configparser import ConfigParser

import requests
import urllib3


class Note163:

    def __init__(self):
        self.cfg = ConfigParser()
        self.session = requests.Session()

    def checkin(self):
        self.cfg.read('config.ini')
        url = 'https://note.youdao.com/yws/mapi/user?method=checkin'
        cookies = {
            'YNOTE_LOGIN': 'true',
            'YNOTE_SESS': self.cfg.get('note163', 'note_sess')
        }

        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        resp = self.session.post(url=url, cookies=cookies)
        info = json.loads(resp.text)
        if resp.status_code == 200:
            total = info['total'] / 1048576
            space = info['space'] / 1048576
            msg = "".join([str(date), ' 签到成功,本次获取', str(space), 'M,总共获取', str(total), 'M'])
            print(msg)
            return True
        else:
            print("".join([str(date), ' 签到失败 ', info['message']]))
            return False

    def login_update_cfg(self):
        self.cfg.read('config.ini')
        login_url = 'https://note.youdao.com/login/acc/urs/verify/check?' \
                    'product=YNOTE&app=client&ClientVer=61000000001&GUID=PCa8d40a1219d9c618e&client_ver=61000000001&' \
                    'device_id=PCa8d40a1219d9c618e&device_name=BIGJELLY&device_type=PC&keyfrom=pc&os=Windows&' \
                    'os_ver=Windows%2010&vendor=website&vendornew=website&show=true&tp=urstoken&cf=6'
        param = {
            'username': self.cfg.get('note163', 'username'),
            'password': self.cfg.get('note163', 'password')
        }
        urllib3.disable_warnings()
        resp = self.session.post(url=login_url, data=param, verify=False)
        x = [i.value for i in self.session.cookies if i.name == 'YNOTE_SESS']
        if x.__len__() == 0:
            print("登录失败")
            print(resp.history)
            print(resp.cookies)
            return
        print('登陆成功，更新 note_sess')
        self.cfg.set('note163', 'note_sess', x[0])
        self.cfg.write(open("config.ini", "w"))

    def auto_checkin(self):
        if not self.checkin():
            self.login_update_cfg()
            self.checkin()

    def timestamp(self):
        return str(int(time.time() * 1000))


if __name__ == '__main__':
    Note163().auto_checkin()
