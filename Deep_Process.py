import requests
import datetime
import os
import urllib
import ssl
import zipfile
import re
import DataBase_About


# redis配置信息



class ToCqhttp:
    # 向群组发送消息（群聊）
    def send_message_group(GID, Address, Port, message):
        url = 'http://%s:%s/send_group_msg' % (Address, Port)
        params = {
            "group_id": '%s' % (GID),
            "message": '%s' % (message)
        }
        requests.get(url, params=params)

    # 向个人发送消息（私聊）
    def send_message_private(QID, Address, Port, message):
        url = 'http://%s:%s/send_private_msg' % (Address, Port)
        params = {
            "user_id": '%s' % (QID),
            "message": '%s' % (message)
        }
        requests.get(url, params=params)

    # 获取群成员信息列表
    def get_group_member_list(GID, Address, Port):
        url = 'http://%s:%s/get_group_member_list' % (Address, Port)
        params = {
            "group_id": '%s' % (GID)
        }
        data = requests.get(url, params=params).json()
        QID = []
        for user_info in data['data']:
            QID.append(user_info['user_id'])
        return QID #返回List，所有人QID

    #获取群列表
    def get_group_list(Address, Port):
        url = 'http://%s:%s/get_group_list' % (Address, Port)
        data = requests.get(url).json()['data']
        for m in data :
            DataBase_About.RedisDB.create_set_gid(m['group_id'])

class LocalProcess:
    # 下载图片
    def pic_download(img_url, QID, GID):
        # 保存图片到磁盘
        Date = datetime.date.today().strftime('%Y-%m-%d')
        file_path = 'Images' + os.sep + Date + '&' + str(GID)
        stuid = DataBase_About.Redis_db.select_kv(QID)
        file_name = stuid + '-' + DataBase_About.Redis_db.select_kv(stuid) + '-' + str(QID)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            # 获得图片后缀
        file_suffix = '.jpg'
        # 拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        # 下载图片，并保存到文件夹中
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(img_url, filename=filename)
    # 文件压缩
    def mk_send_zip(Date, Address, Port, QID, GID):
        # 压缩
        source_path = os.getcwd() + os.sep + 'Images' + os.sep + Date + '&' + str(GID)

        name = Date + '&' + DataBase_About.Redis_db.select_kv(GID) + '.zip'
        destnation = 'E_Send' + os.sep + name
        if os.path.exists(source_path):
            ToCqhttp.send_message_group(GID,Address,Port,'正在压缩，请等候')
            # 压缩后的名字
            zip = zipfile.ZipFile(destnation, 'w', zipfile.ZIP_DEFLATED)
            for dir_path, dir_names, file_names in os.walk(source_path):
                # 去掉目标跟路径，只对目标文件夹下面的文件及文件夹进行压缩
                fpath = dir_path.replace(source_path, '')
                for filename in file_names:
                    zip.write(os.path.join(dir_path, filename), os.path.join(fpath, filename))
            zip.close()

        # zip私聊发送
        path = os.getcwd() + os.sep + destnation
        url = 'http://%s:%s/upload_private_file' % (Address, Port)
        params = {
            "user_id": '%s' % (QID),
            "file": '%s' % (path),
            "name": '%s' % (name)
        }
        requests.get(url, params=params)
        ToCqhttp.send_message_group(GID, Address, Port, '文件已通过私信发送')

    # 数据统计
    def get_infolderpic_ID(GID, Address, Port):
        # 获取文件夹内所有文件名称
        DataBase_About.Redis_db.delete_set(0)
        path = 'Images' + os.sep + datetime.date.today().strftime('%Y-%m-%d') + '&' + str(GID)
        data_names = os.listdir(path)
        for i in data_names:
            DataBase_About.Redis_db.create_set_fact_upload_stuid( re.match('\d*', i).group()) # 实交集合
        class_ = DataBase_About.Redis_db.select_kv(GID)#获取班级名称
        for j in DataBase_About.Redis_db.select_set(class_) :
            stuid = DataBase_About.Redis_db.select_kv(j)
            DataBase_About.Redis_db.create_set_should_upload_stuid(stuid) # 应交集合
        result = DataBase_About.Redis_db.unupload_stuid(0)
        list = '未上传人员名单：\n'
        ToCqhttp.send_message_group(GID, Address, Port, '未交人数：' + str(result[1]))
        if result[1] == 0:
            ToCqhttp.send_message_group(GID, Address, Port, '今日已全部上传')
        elif result[1]>=1:
            name = '?'
            for k in result[0]:
                tmpname = DataBase_About.Redis_db.select_kv(k)
                name = name + '，' + tmpname
            name = name.lstrip('?，')
            ToCqhttp.send_message_group(GID, Address, Port, list + name)

 # at未上交人员
    def at_process(GID, Address, Port):
        # 获取文件夹内所有文件名称
        DataBase_About.Redis_db.delete_set(0)
        path = 'Images' + os.sep + datetime.date.today().strftime('%Y-%m-%d') + '&' + str(GID)
        data_names = os.listdir(path)
        for i in data_names:
            DataBase_About.Redis_db.create_set_fact_upload_stuid( re.match('\d*', i).group()) # 实交集合
            DataBase_About.Rdb2.create_kv_stuid_qid(re.match('\d*', i).group(), re.match('\d*',i[::-1][4:]).group()[::-1])
        class_ = DataBase_About.Redis_db.select_kv(GID)#获取班级名称
        for j in DataBase_About.Redis_db.select_set(class_) :
            stuid = DataBase_About.Redis_db.select_kv(j)
            DataBase_About.Redis_db.create_set_should_upload_stuid(stuid) # 应交集合
        result = DataBase_About.Redis_db.unupload_stuid(0)
        msg = "\n" + "今日：" + datetime.date.today().strftime('%Y-%m-%d') + " 截图未上传，请尽快上传"
        ToCqhttp.send_message_group(GID, Address, Port, '未交人数：' + str(result[1]))
        if result[1] == 0:
            ToCqhttp.send_message_group(GID, Address, Port, '今日已全部上传')
        elif result[1]>=1:
            for k in result[0]:
                qid = DataBase_About.Rdb2.select_kv(k)
                notice = "[CQ:at,qq=%s]" % (str(qid)) + msg
                ToCqhttp.send_message_group(GID,Address,Port,notice)