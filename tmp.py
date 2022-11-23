import os
import datetime
import DataBase

GID = 691727298

path = 'Images' + os.sep + datetime.date.today().strftime('%Y-%m-%d')
datanames = os.listdir(path)
list = []
for i in datanames:
    list.append(i[:8])
for id in list:
    print(id)
    DataBase.update_check_point(GID,id,1)
name = DataBase.selest_unsendpic_name(GID)

print(name)
print(type(name))
print(name[1])
