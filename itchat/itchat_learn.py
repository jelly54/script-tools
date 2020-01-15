# -*- coding: utf-8 -*-
import itchat


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    if not msg['FromUserName'] == myUserName:
        # 群名 发消息人 信息
        message = "Group:{}\tSender:{}\nContent:{}\n".format(msg['User']['NickName'], msg['ActualNickName'],
                                                             msg['Content'])

        if (msg['User']['NickName'] == '小金淘宝免单15群') and ('免单' in msg['Content']):
            print(message)
            itchat.send_msg(msg['Content'], get_user_by_nickname('杨静'))
            itchat.send_msg(msg['Content'], get_user_by_nickname('路人张'))


def get_user_by_nickname(nickname):
    users = itchat.search_friends(nickname)
    return users[0]['UserName']


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=-1)

    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
