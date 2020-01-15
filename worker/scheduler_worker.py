#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author : Jelly
# @Date : 2019/12/12 11:46
import datetime
import os
import time

import pymysql
import schedule


def get_con(host, port, user, password, db, charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    return conn


def execute(conn, exe_sql):
    res = None
    cur = conn.cursor()
    try:
        status = cur.execute(exe_sql)
        conn.commit()
        res = status, cur.fetchall()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
    return res


def run_cmd(exe_cmd):
    """
    在系统终端执行命令
    :param exe_cmd: 需要执行的命令
    :return: 是否执行成功
    """
    result = os.system(exe_cmd)
    if result == 0:
        return True
    print('%s execute failed!! %s ' % (exe_cmd, result))
    return False


def remain_num():
    """
    查询剩余的任务数量
    ai_sql_data 数据库中 task_info 表 task_type=1 && task_status<8
    :return: 剩余任务数量
    """
    conn = get_con('localhost', 3306, 'ai_root', 'Linkdoc_ai123', 'ai_sql_data')
    rep = execute(conn, "SELECT COUNT(1) FROM task_info WHERE task_type=1 AND task_status<8;")
    print('remained task: %s \n' % rep[1][0][0])
    return rep[1][0][0]


def job1(job_name='job1'):
    """
    关闭吕大夫ai-worker服务，开启线上ai-worker服务
    :param job_name:  任务名称
    :return:
    """
    print('%s start %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_name))
    cmds = []
    start_prod_service = "docker exec -i " + prod_service + " sv start ai_worker"
    stop_lv_service = "docker exec -i " + other_service + " sv stop ai_worker"
    cmds.append(start_prod_service)
    cmds.append(stop_lv_service)
    if run_cmd(' && '.join(cmds)):
        print('%s end %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_name))
    else:
        print('%s failed!!! %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_name))


def job2(job_name='job2'):
    """
        关闭线上ai-worker服务，开启吕大夫ai-worker服务
        :param job_name:  任务名称
        :return:
        """
    print('%s start %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_name))
    cmds = []
    stop_prod_service = "docker exec -i " + prod_service + " sv stop ai_worker"
    start_lv_service = "docker exec -i " + other_service + " sv start ai_worker"
    cmds.append(stop_prod_service)
    cmds.append(start_lv_service)
    if run_cmd(' && '.join(cmds)):
        print('%s end %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_name))
    else:
        print('%s failed!!! %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), job_name))


def main():
    schedule.every().day.at('6:30').do(job1)
    schedule.every().day.at('8:30').do(job2)

    # schedule.every().monday.at('6:30').do(job1)
    # schedule.every().friday.at('20:30').do(job2)
    print('%s start schedule mission.\n%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), schedule.jobs))
    while True:
        schedule.run_pending()
        # 每2分钟检查一次是否完成
        if remain_num() > 0:
            time.sleep(120)
        else:
            job1('start prod service')
            schedule.clear()
            break
    print('all done.')


if __name__ == '__main__':
    prod_service = 'cfda_ai_policy_cfda_1'
    other_service = 'du_data_ai_policy_1'
    main()
