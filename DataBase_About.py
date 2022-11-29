import redis
import sqlite3
import yaml
import os

config = yaml.safe_load(open(r"Config" + os.sep + "RedisDB_Config.yml", encoding='utf-8'))
host1 = config['Host']
port1 = config['Port']
database1 = config['DataBase1']
database2 = config['DataBase2']
connects1 = config['Max_connection']
pool = redis.ConnectionPool(host=host1, port=port1, db=database1, max_connections=connects1, decode_responses=True)
rdb = redis.Redis(connection_pool=pool)

pool2 = redis.ConnectionPool(host=host1, port=port1, db=database2, max_connections=connects1, decode_responses=True)
rdb2 = redis.Redis(connection_pool=pool2)

class Redis_db :
    # 检查AOF持久化是否开启
    def checkaof(self):
        if rdb.config_get('appendonly')['appendonly'] == 'no':
            rdb.config_set('appendonly', 'yes')
            rdb.config_rewrite()
        else:
            return 0

    #查询键值
    def select_kv(key):
        value = rdb.get(str(key))
        return value

    # 创建检查点的键值
    def create_kv_check_point(point):
        rdb.set('check_point', point)
        return 0

    # 创建GID与班级的键值
    def create_kv_gid_class(GID, class_):
        rdb.set(str(GID), str(class_))
        return 0

    # 创建班级与QID的集合 循环添加，一次一个
    def create_set_class_QID(class_,QID):
        rdb.sadd(class_,QID)
        return 0

    # 创建QID与学号的键值
    def create_kv_qid_stuid(QID, stuid):
        rdb.set(str(QID), str(stuid))
        return 0

    # 创建学号的集合
    def create_set_stuid(GID,stuid):
        class_ = Redis_db.select_kv(GID)
        rdb.sadd('{}'.format(class_), str(stuid))
        return 0

    # 创建学号与姓名的键值
    def create_kv_stuid_name(stuid, name):
        rdb.set(str(stuid), str(name))
        return 0

    # 创建文件应交学号集合
    def create_set_should_upload_stuid(stuid):
        rdb.sadd('应交',str(stuid))
        return 0

    # 求差文件实交学号集合
    def create_set_fact_upload_stuid(stuid):
        rdb.sadd('实交',str(stuid))
        return 0

    def unupload_stuid(self):
        rdb.sdiffstore('结果','应交','实交')
        result = []
        result.append(rdb.smembers('结果'))
        result.append(rdb.scard('结果'))
        #result P1:未交人学号 P2:未交人数
        rdb.delete('应交')
        rdb.delete('实交')
        return result

    # 创建已加群号集合
    def create_set_gid(gid):
        rdb.sadd('群号',str(gid))
        return 0

    # 删除机器人Q号
    def delete_bot_set(class_, bot_qid):
        rdb.srem(class_,bot_qid)
        return 0

    # 集合查询
    def select_set(name):
        sset = rdb.smembers(name)
        return sset

    # 删除应交&实交&结果集合
    def delete_set(self):
        rdb.delete('应交')
        rdb.delete('实交')
        rdb.delete('结果')
        return 0

class Rdb2 :
    def create_kv_stuid_qid(stuid, QID):
        rdb2.set(stuid,QID)
        return 0

    def select_kv(key):
        value = rdb2.get(str(key))
        return value