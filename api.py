import datetime
import os
import ssl
import urllib.request
import zipfile
import requests
import DataBase



def get_group_member_list(GID, Address, Port):  # 获取群成员信息列表
    url = 'http://%s:%s/get_group_member_list' % (Address, Port)
    params = {
        "group_id": '%s' % (GID)
    }
    data = requests.get(url, params=params).json()
    return data


def get_group_member_info(GID, QID, Address, Port):  # 获取群用户身份
    url = 'http://%s:%s/get_group_member_info' % (Address, Port)
    params = {
        "group_id": '%s' % (GID),
        "user_id": '%s' % (QID)
    }
    data = requests.get(url, params=params).json()
    role = data['data']['role']
    return role


def send_message_group(GID, Address, Port, message):
    url = 'http://%s:%s/send_group_msg' % (Address, Port)
    params = {
        "group_id": '%s' % (GID),
        "message": '%s' % (message)
    }
    requests.get(url, params=params)


def send_message_private(QID, Address, Port, message):
    url = 'http://%s:%s/send_private_msg' % (Address, Port)
    params = {
        "user_id": '%s' % (QID),
        "message": '%s' % (message)
    }
    requests.get(url, params=params)

def pic_download(img_url,QID,GID):
    #保存图片到磁盘
    Date = datetime.date.today().strftime('%Y-%m-%d')
    file_path = 'Images'+os.sep+Date
    file_name = DataBase.select_Stu_id(QID,GID)+'-'+DataBase.select_Name(QID,GID)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        #获得图片后缀
    file_suffix = '.jpg'
        #拼接图片名（包含路径）
    filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
       #下载图片，并保存到文件夹中
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(img_url,filename=filename)

def upload_zip(Date,Address,Port,QID):
    #压缩
    Date=Date.lstrip("#")
    source_path =os.getcwd()+os.sep+ 'Images' + os.sep + Date

    name=Date+'.zip'
    destnation = 'E_Send' + os.sep +name
    if os.path.exists(source_path):
        send_message_private(QID,Address,Port,'压缩中，请耐心等待')
        # 压缩后的名字
        zip = zipfile.ZipFile(destnation, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, file_names in os.walk(source_path):
            # 去掉目标跟路径，只对目标文件夹下面的文件及文件夹进行压缩
            fpath = dir_path.replace(source_path, '')
            for filename in file_names:
                zip.write(os.path.join(dir_path, filename), os.path.join(fpath, filename))
        zip.close()

    #zip私聊发送
    path= os.getcwd()+os.sep+destnation
    url = 'http://%s:%s/upload_private_file' % (Address, Port)
    params = {
        "user_id": '%s' % (QID),
        "file":'%s' %(path),
        "name":'%s'%(name)
    }
    requests.get(url, params=params)

    #获取文件夹内所有文件名称
def get_infolderpic_ID(GID,Address,Port):
    path = 'Images' + os.sep + datetime.date.today().strftime('%Y-%m-%d')
    datanames = os.listdir(path)
    list = []
    for i in datanames:
        list.append(i[:8])
    for id in list:
        DataBase.update_check_point(GID, id, 1)
    name = DataBase.selest_unsendpic_name(GID)
    send_message_group(GID,Address,Port,(r'未交截图名单: %s'%name))

