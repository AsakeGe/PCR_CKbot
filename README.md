# PCR_CKbot

QQ自动收集核酸采样证明并汇总机器人，目前已经基本可用，但仅限收集与打包发送。

## 使用

### 关于go-cqhttp部分：
  * 需要搭配 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 使用。
  * 在配置 go-cqhttp 时，请选择 "HTTP API"
  * 在config.yml中，开启POST
  * 在config.yml中，将 "- url: http://0.0.0.0:5701/ # 地址" 中 “0.0.0.0” 更改为本项目运行设备的IP地址
  * 请牢记在config.yml中设置的正、反向端口，地址
  * 关于本项目的部分：
    * 首先，也是最重要的一点，目前还未做到完全体功能，故仍旧存在使用门槛
    * 在main.py中：
      * Address = '127.0.0.1'
      * Port = 5700
      * app.run(host='0.0.0.0', port=5701)
    * Address 更改为 go-cqhttp 的接收服务器地址
    * Port 更改为 go-cqhttp 的接收端口
    * host 更改为本机地址或保留不变也可 
    * port更改为go-cqhttp的POST端口
    * 运行即可

### 帮助
  * 私聊向机器人发送 #帮助 即可获取使用说明 

### 其他
  * 目前仅针对西安邮电大学每日核酸统计设计，其他要使用的话，建议魔改。
