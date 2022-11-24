import os
import re

import DataBase
import api
import yaml



# 群聊管理员判断
def su_auth(GID, QID, Address, Port):
    if api.get_group_member_info(GID, QID, Address, Port) == 'admin' or api.get_group_member_info(GID, QID, Address,
                                                                                                  Port) == 'owner':
        return 0
    else :
        return 1
#私聊
def private_chat( QID, Address, Port, message):

    if message == '#帮助':
        api.send_message_private(QID, Address, Port, '管理员——(群聊)：')
        api.send_message_private(QID, Address, Port, '1.#创建数据库，获取群内所有成员QID并建立数据库')
        api.send_message_private(QID, Address, Port, '2.#导入群成员QID，向数据库内导入群成员QID')
        api.send_message_private(QID, Address, Port, '3.#导出，获取导出收集文件帮助')
        api.send_message_private(QID, Address, Port, '4.#日期(#YYYY-MM-DD)，接收打包文件,文件以私聊形式发送')
        api.send_message_private(QID, Address, Port, '5.#未上传，获取今日未上传截图人员名单')
        api.send_message_private(QID, Address, Port, '6.at未上传，以@形式通知未上传人员')
        api.send_message_private(QID, Address, Port, '7.#班级****，建立Q群与班级联系，每个群均需输入一次')

        #群聊
def group_chat(GID, QID, Address, Port, message):
        conf = yaml.safe_load(open(r"Config" + os.sep + "config.yml"))
        # 用户格式
 #权限者命令
        if message == '#创建数据库' and su_auth(GID, QID, Address, Port) == 0:
            DataBase.create_table(GID)
            api.send_message_group(GID, Address, Port, '数据库创建完成')
        elif message == '#导入群成员QID' and su_auth(GID, QID, Address, Port) == 0:
            data = api.get_group_member_list(GID, Address, Port)
            for user_info in data['data']:
                QID = user_info['user_id']
                DataBase.insert_into(QID,GID)
            DataBase.delete_Bot_QID(conf['Bot_QID'],GID)
            api.send_message_group(GID, Address, Port, '群成员信息已导入')

        elif message == '#导出':
            path = os.listdir('Images')
            out = []
            for i in path:
                out.append(i[:10])
            api.send_message_group(GID,Address,Port,out)
            api.send_message_group(GID, Address, Port, '请回复\n#日期（YYYY-MM-DD）\n以选择')
        elif message == '#未上传':
            api.get_infolderpic_ID(GID,Address,Port)
        elif message == 'at未上传':
            api.notice(GID,Address,Port)
        elif re.match(r"#\d{4}-\d{2}-\d{2}", message) != None:
            api.upload_zip(message[1:], Address, Port, QID, GID)
        elif re.match(r"#班级.*",message) != None:
            DataBase.insert_into_table_group_and_class(GID,message[3:])
            api.send_message_group(GID,Address,Port,'群班级信息已录入')




 #成员命令
        elif re.match(r"\d{8}#(.*)#(.*)", message) != None:
            stu_id = re.search(r"(.*)#", message, flags=0).group()
            class_ = re.search(r"#(.*)#", message, flags=0).group()
            name = re.search(r"#(.*)", message, flags=0).group()
            stu_id = stu_id.replace(class_, "")
            name = name.replace(class_, "")
            int(stu_id)
            class_ = class_.lstrip('#')
            class_ = class_.rstrip('#')
            DataBase.update_major_data(GID,QID,stu_id,name,class_)
            api.send_message_group(GID, Address, Port, '信息已录入')
        elif message == '#帮助':
            api.send_message_group(GID, Address, Port, '[CQ:image,file=Help.png]')
        elif '[CQ:image,file='in message:
            url=message.split('url=')
            url=url[1]
            str(url)
            pic_url=url.rstrip("]")#后接下载模块
            api.pic_download(pic_url,QID,GID)
            api.send_message_group(GID, Address, Port, '截图已保存')