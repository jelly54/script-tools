# coding:utf-8
import itchat


def get_friends_info(file_name='res/friends_info.txt', download_header=False, save_path='headerImg/'):
    fh = open(file_name, 'a', encoding='utf8')
    itchat.login()
    friends = itchat.get_friends(update=False)[0:]
    # 设置需要爬取的信息字段
    info_k = ['NickName', 'RemarkName', 'Sex', 'Province', 'City', 'ContactFlag', 'SnsFlag', 'Signature']
    info_v = ['微信昵称', '备注', '性别', '省份', '城市', '联系标识', '渠道标识', '个性签名']

    for v in info_v:
        fh.write(v + ",")
    for index, friend in enumerate(friends):
        print('get ', index)
        for k in info_k:
            fh.write(str(friend.get(k)).strip().replace('\n', '').replace('\r', '') + ",")
        fh.write('\n')

        if download_header:
            head = itchat.get_head_img(userName=friend["UserName"])
            img_file = open(save_path + str(index) + '.jpg', 'wb')
            img_file.write(head)
            img_file.close()

    print("done")


def splice_imgs(save_path='res/', file_path='headerImg/'):
    """
    该函数功能为拼接图片
    :param save_path: 拼接完成的图片存储路径
    :param file_path: 源图片存储路径
    """

    # 将所有头像的路径提取出来
    path_list = []
    import os
    for item in os.listdir(file_path):
        img_path = os.path.join(file_path, item)
        path_list.append(img_path)

    # 为拼凑成一个正方形图片，每行头像个数为总数的开平方取整
    from math import sqrt
    line = int(sqrt(len(path_list)))

    # 新建待拼凑图片
    from PIL import Image
    new_image = Image.new('RGB', (128 * line, 128 * line))

    x, y = 0, 0

    # 进行拼图
    for item in path_list:
        try:
            img = Image.open(item)
            img = img.resize((128, 128), Image.ANTIALIAS)
            new_image.paste(img, (x * 128, y * 128))
            x += 1
        except IOError:
            print("第%d行,%d列文件读取失败！IOError:%s" % (y, x, item))
            x -= 1
        if x == line:
            x = 0
            y += 1
        if (x + line * y) == line * line:
            break

    # 将拼好的图片存储起来
    new_image.save(save_path + "splice.jpg")


if __name__ == '__main__':
    # get_friends_info(download_header=True)
    splice_imgs()
