import Control
from flask import Flask, request
app = Flask(__name__)
'''监听端口，获取QQ信息'''
@app.route('/', methods=["POST"])
def post_data():
    '下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式'
    if request.get_json().get('message_type')=='private':# 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        Control.privacy_chat_massage_process(uid,message)
        #Control.keyword(message, uid) # 将 Q号和原始信息传到我们的后台

    if request.get_json().get('message_type')=='group':# 如果是群聊信息
        gid = request.get_json().get('group_id') # 获取群号
        uid = request.get_json().get('sender').get('user_id') # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message') # 获取原始信息
        Control.group_chat_massage_process(uid,message,gid)
        #Control.keyword(message, uid, gid) # 将 Q号和原始信息传到我们的后台
    return 'OK'
if __name__ == '__main__':
    app.run(debug=False, host='192.168.3.204', port=5701)# 此处的 host和 port对应上面 yml文件的设置

