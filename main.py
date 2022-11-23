import api
from flask import Flask, request
import process
import os
import yaml


conf = yaml.safe_load(open(r"Config"+os.sep+"config.yml"))
Address = conf['Server_IP']
Port = conf['Server_Port']
host = conf['Host_IP']
post_port = conf['Server_POST_Port']

app = Flask(__name__)


@app.route('/', methods=["POST"])
def post_data():
    """下面的request.get_json().get......是用来获取关键字的值用的，关键字参考go-cqhttp帮助文档"""
    data = request.get_json()
    if data['post_type'] == 'message':#判断收到的时消息而不是其他
        message= data['message']
        message_type = data['message_type']

        if message_type =='group':#收到群消息
            GID=data['group_id']#群号
            QID = data['user_id']#QQ号
            process.group_chat(GID,QID,Address,Port,message)


        elif message_type == 'private':#收到私聊消息
            QID = data['user_id']#QQ号
            process.private_chat( QID, Address, Port, message)

    return "OK"


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置

    app.run(host=host, port=post_port)  # 保证和我们在配置里填的一致