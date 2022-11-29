import os
import yaml
from flask import Flask, request

import Chat_with_human
import DataBase_About

config=yaml.safe_load(open(r"Config"+os.sep+"config.yml",encoding='utf-8'))

Address = config['Server_IP']
Send_Port = config['Server_Port']
Host = config['Host_IP']
Receive_Port = config['Server_POST_Port']
Bot_QID = config['Bot_QID']
app = Flask(__name__)

#检查数据库持久化
DataBase_About.Redis_db().checkaof()

@app.route('/', methods=["POST"])
def post_data():
    """下面的request.get_json().get......是用来获取关键字的值用的，关键字参考go-cqhttp帮助文档"""
    data = request.get_json()
    if data['post_type'] == 'message':  # 判断收到的时消息而不是其他
        Chat_with_human.message_process(data, Bot_QID, Address, Send_Port)

    return "OK"

if __name__ == '__main__':
    app.run(host=Host, port=Receive_Port)  # 保证和我们在配置里填的一致
