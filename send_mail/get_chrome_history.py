#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/22 21:05
# @Author  : Jelly
# @File    : get_chrome_history.py

import datetime
import getpass
import os
import platform
import sqlite3
import time


def _pc_info():
    username = getpass.getuser()
    node = platform.node()  # 获取计算机的网络名
    plat = platform.platform()  # 获取操作系统名称及版本号
    machine = platform.machine()  # 获取计算机类型
    processor = platform.processor()  # 获取计算机处理器信息
    # print('computerInfo：\n\tusername：' + str(username) + '\n\thostname：' + str(node) + '\n\tsystem：' + str(plat) +
    #       ' ' + str(machine) + '\n\tprocess：' + str(processor).replace(',', '-'))
    return username, node, plat, machine, processor


def _history_data():
    # 获取今天0点的日期
    now = datetime.datetime.now()
    now_000 = time.strftime('%Y-%m-%d', datetime.datetime.timetuple(now))

    # 获取昨天0点的日期
    today = datetime.datetime.strptime(now_000, '%Y-%m-%d')
    yestoday = today - datetime.timedelta(days=1)
    basedate = datetime.datetime(1601, 1, 1)

    # 获取以1601年为基准的时间戳
    # today_timestamp = (today - basedate).total_seconds()
    yestoday_timestamp = (yestoday - basedate).total_seconds()

    pc = _pc_info()
    if pc and ('Windows' in pc[2]):
        connstr = 'C:\\Users\\' + pc[0] + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History'
    else:
        connstr = '~/Library/Application\ Support/Google/Chrome/Default/History'

    # 校验Chrome文件是否存在
    if not os.path.exists(connstr):
        raise Exception('Chrome History File does not exists!')

    conn = sqlite3.connect(connstr)
    cur = conn.cursor()
    querystr = 'select url,last_visit_time from urls order by last_visit_time desc'

    try:
        cur.execute(querystr)
    except sqlite3.OperationalError:
        print('please close chrome browser at first!')

    data_all = cur.fetchall()
    expectdata = []
    for data in data_all:
        # 微秒转换为秒
        last_visit_time = data[1] / 1000 / 1000
        # 获取昨天时间之后的内容，否则退出循环（查询数据已经倒序排列）
        if last_visit_time > yestoday_timestamp:
            # 转换访问时间，UTC转换时区 + 8h
            visit_time = basedate + datetime.timedelta(seconds=last_visit_time, hours=8)
            # #UTC转换时区
            # visit_time = visit_time.astimezone(pytz.timezone('Asia/Shanghai'))
            visit_time = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.timetuple(visit_time))
            expectdata.append(visit_time + '   ' + data[0])
        else:
            # 如果无历史数据，抛出异常提示
            if not expectdata:
                raise Exception('there is no data.')
            break
    cur.close()
    conn.close()
    return '\n'.join(pc) + '\n\n' + '\n'.join(expectdata)


def _str2file(content, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(str(content))
        f.close()


def get_history(file_name='his.txt'):
    content = _history_data()
    _str2file(content=content, file_name=file_name)
    return file_name


if __name__ == '__main__':
    get_history()