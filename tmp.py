import DataBase
import yaml
import os

GID = 691727298
conf = yaml.safe_load(open(r"Config" + os.sep + "config.yml"))

DataBase.delete_Bot_QID(str(conf['Bot_QID']),GID)
