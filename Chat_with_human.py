import os
import re
import yaml
import DataBase_About
import Deep_Process

def message_process(information, bot_qid, Address, Port):
    try:
        message_type = information['message_type']  # 消息来源，群聊（group），私聊（private）
        message = information['message']  # 消息内容
        gid = information['group_id']  # 发送消息的群的群号
        qid = information['user_id']  # 发送消息的个人的QID
        group_role = information['sender']['role']  # 群内发送消息的个人在群中的身份：群主（owner）、管理员（admin）、普通成员（member）
    except KeyError as group_id :
        message_type = information['message_type']  # 消息来源，群聊（group），私聊（private）
        message = information['message']  # 消息内容
        qid = information['user_id']  # 发送消息的个人的QID
    try:
        if re.match("#", message[:1]) != None: # 以"#"开头的指令判断，正确向下进行

            if message_type == 'group':  # 群聊
                # 群聊
                if group_role == 'admin' or group_role == 'owner':  # 群管理员命令

                    if message[1:5] == '创建班级':
                        DataBase_About.Redis_db.create_kv_gid_class(gid,message[6:])
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '班级已创建')
                    elif message[1:] == '导入群成员':
                        if DataBase_About.Redis_db.select_kv(gid) == None :
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '未创建班级，请先创建班级后再尝试')
                        else :
                            qid_list = Deep_Process.ToCqhttp.get_group_member_list(gid,Address,Port)
                            class_ = DataBase_About.Redis_db.select_kv(gid)  # gid<>class /Key & Value
                            for a in qid_list :
                                DataBase_About.Redis_db.create_set_class_QID(class_, a)
                            DataBase_About.Redis_db.delete_bot_set(class_,bot_qid)
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已导入群成员QID')


                    elif message[1:] == '开启收集':
                        # Collect_Point == 0
                        DataBase_About.Redis_db.create_kv_check_point(0)
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已开始收集核酸采样截图')

                    elif message[1:] == '停止收集':
                        # Collect_Point == 1
                        DataBase_About.Redis_db.create_kv_check_point(1)
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已停止收集核酸采样截图')

                    elif message[1:] == '未上传':
                        try:
                            Deep_Process.LocalProcess.get_infolderpic_ID(gid,Address,Port)
                        except FileNotFoundError as WinError :
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '今日未上传核酸采样截图')

                    elif message[1:] == 'at未上传':
                         Deep_Process.LocalProcess.at_process(gid,Address,Port)

                    elif message[1:3] == '导出':
                        path = os.listdir('Images')
                        out = []
                        for i in path:
                            out.append(i[:10])
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, out)
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '请回复\n#日期（YYYY-MM-DD）\n以选择')


                    elif re.match('\d{4}-\d{2}-\d{2}',message[1:]) != None:
                        # 发送
                        Deep_Process.LocalProcess.mk_send_zip(message[1:], Address, Port, qid, gid)
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '文件已打包，且通过私信发送，请查收。')
                    elif message[1:3] == '学号':
                        DataBase_About.Redis_db.create_kv_qid_stuid(qid,message[4:])
                        DataBase_About.Rdb2.create_kv_stuid_qid(message[4:], qid)
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已录入学号')

                    elif message[1:3] == '姓名':
                        if DataBase_About.Redis_db.select_kv(qid) == None :
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '请先录入学号')
                        else:
                            stuid = DataBase_About.Redis_db.select_kv(qid)
                            DataBase_About.Redis_db.create_kv_stuid_name(stuid,message[4:])
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已录入姓名')


                    ##############
                    elif message[1:3] == '测试':
                        print()
                    ##############


                elif group_role == 'member': # 群成员命令-普通
                    if message[1:3] == '学号':
                        DataBase_About.Redis_db.create_kv_qid_stuid(qid,message[4:])
                        DataBase_About.Rdb2.create_kv_stuid_qid(message[4:],qid)
                        Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已录入学号')
                    elif message[1:3] == '姓名':
                        if DataBase_About.Redis_db.select_kv(qid) == None :
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '请先录入学号')
                        else:
                            stuid = DataBase_About.Redis_db.select_kv(qid)
                            DataBase_About.Redis_db.create_kv_stuid_name(stuid,message[4:])
                            Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '已录入姓名')

            elif message_type == 'private':  # 私聊
                if message[1:3] == '帮助':
                    text =  '''\n指令：\n群聊指令：\n管理员指令：\n1：#创建班级：XXXX\n2：#导入群成员【第一次，创建表，包括群成员QID，学号，班级，姓名，检查点】\n3：#未上传【本群内今日未上传核酸采样数据人员名单以人数】\n4：#at未上传【@本群内今日未上传核酸采样数据人员，提醒上传】\n5：#导出：YYYY-MM-DD【打包导出本群内指定日期截图，以私聊形式发送给请求导出管理员】\n6:#排除管理员 【管理员不参与信息收集】\n7:#开启收集 【此时开始下载群内发来的所有图片】\n8:#关闭收集 【此时停止下载群内发来的所有图片】\n9:#保存数据 【将redis中数据存入DataSave.db中】\n所有成员指令：\n1：#学号：xxxx\n2：#班级：xxxx\n3：#姓名：xxxx\n私聊指令：\n1：【待定】\n'''
                    Deep_Process.ToCqhttp.send_message_private(qid, Address, Port, text)
        # 图片收集
        elif '[CQ:image,file=' in message and re.search('subType=1',message) == None :
            try:
                url = re.search(r'url=.*', message).group()[4:].rstrip(']')
                Deep_Process.LocalProcess.pic_download(url, qid, gid)
                Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '截图已收录')
            except TypeError as unsupported:
                Deep_Process.ToCqhttp.send_message_group(gid, Address, Port, '请录入个人信息，学号及姓名')




    finally:
        print('over')


