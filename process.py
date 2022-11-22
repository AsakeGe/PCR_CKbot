import api
import DataBase
import re
import os


# 群聊管理员判断
def su_auth(GID, QID, Address, Port):
    if api.get_group_member_info(GID, QID, Address, Port) == 'admin' or api.get_group_member_info(GID, QID, Address,
                                                                                                  Port) == 'owner':
        return 0
    else :
        return 1
#私聊
def private_chat( QID, Address, Port, message):
    if "['"+ message +"']" == str(re.findall(r"#\d{4}-\d{2}-\d{2}",message)):
        print(message)
        api.upload_zip(message,Address,Port,QID)
#群聊
def group_chat(GID, QID, Address, Port, message):
        # 用户格式
        stand = re.search(r"(.*)#(.*)#(.*)", message, flags=0)
 #权限者命令
        if message == '#创建数据库' and su_auth(GID, QID, Address, Port) == 0:
            DataBase.create_table()
            api.send_message_group(GID, Address, Port, '数据库创建完成')
        elif message == '#导入群成员QID' and su_auth(GID, QID, Address, Port) == 0:
            data = api.get_group_member_list(GID, Address, Port)
            for user_info in data['data']:
                GQID = user_info['user_id']
                DataBase.insert_into(GQID)
            api.send_message_group(GID, Address, Port, '群成员信息已导入')
        elif message == '#导出':
            path = os.listdir('Images')
            api.send_message_private(QID,Address,Port,path)
            api.send_message_private(QID, Address, Port, '请回复\n#日期\n以选择')


 #成员命令
        elif stand != None:
            stu_id = re.search(r"(.*)#", message, flags=0).group()
            class_ = re.search(r"#(.*)#", message, flags=0).group()
            name = re.search(r"#(.*)", message, flags=0).group()
            stu_id = stu_id.replace(class_, "")
            name = name.replace(class_, "")
            int(stu_id)
            class_ = class_.lstrip('#')
            class_ = class_.rstrip('#')
            DataBase.update_stu_number(stu_id, QID)
            DataBase.update_class(class_, QID)
            DataBase.update_name(name, QID)
            api.send_message_group(GID, Address, Port, '信息已录入')
        elif message == '#帮助':
            api.send_message_group(GID, Address, Port, '[CQ:image,file=Help.png]')
        elif '[CQ:image,file='in message:
            url=message.split('url=')
            url=url[1]
            str(url)
            pic_url=url.rstrip("]")#后接下载模块
            api.pic_download(pic_url,QID)
            api.send_message_group(GID, Address, Port, '截图已保存')