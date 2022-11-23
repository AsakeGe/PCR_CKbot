import sqlite3


def create_table(table_name):
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    table_name = ('group' + str(table_name))
    sql_text = '''CREATE TABLE %s 
               (QID INT PRIMARY KEY,
                STU_ID INT,
                NAME VARCHAR(255),
                CLASS VARCHAR(255),
                CHECK_POINT INT);''' % table_name
    cursor.execute(sql_text)
    cursor.close()
    connection.close()


def insert_into(QID, table_name):
    table_name = ('group' + str(table_name))
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    Stu_Number = 'NULL'
    Name = 'NULL'
    Class = 'NULL'
    CHECK_POINT = 0
    sql_text = '''INSERT INTO %s 
                    (QID, 
                    STU_ID, 
                    NAME, 
                    CLASS, 
                    CHECK_POINT) 
                    VALUES(%s,%s,%s,%s,%s)'''%(table_name, QID, Stu_Number, Name, Class, CHECK_POINT)
    cursor.execute(sql_text)
    cursor.close()
    connection.commit()
    connection.close()


def update_major_data(table_name,QID,STU_ID,NAME,CLASS):
    table_name = ('group' + str(table_name))
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = '''UPDATE %s 
                  SET STU_ID =%s, 
                      NAME  ='%s', 
                      CLASS  ='%s'  
                      WHERE QID =%s'''%(table_name, STU_ID, NAME, CLASS, QID)
    cursor.execute(sql_text)
    cursor.close()
    connection.commit()
    connection.close()

def update_check_point(table_name,STU_ID,Point):
    table_name = ('group' + str(table_name))
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = '''UPDATE %s 
                      SET CHECK_POINT = %s  
                          WHERE STU_ID = %s ''' % (table_name, Point, STU_ID)
    cursor.execute(sql_text)
    cursor.close()
    connection.commit()
    connection.close()


def select_Name(QID, table_name):
    table_name = ('group' + str(table_name))
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = "SELECT NAME FROM '%s'  WHERE QID=%s" % (table_name, QID)
    cursor.execute(sql_text)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    result = ''.join(str(res))
    result = result.lstrip("[('")
    result = result.rstrip("',)]")
    return result

def select_Stu_id(QID, table_name):
    table_name = ('group' + str(table_name))
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = "SELECT STU_ID FROM '%s'  WHERE QID=%s" % (table_name, QID)
    cursor.execute(sql_text)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    result = ''.join(str(res))
    result = result.lstrip("[('")
    result = result.rstrip("',)]")
    return result
def selest_unsendpic_name(table_name):#查找没交图片名字
    table_name = ('group' + str(table_name))
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = "SELECT NAME FROM '%s'  WHERE CHECK_POINT=0" % (table_name)
    cursor.execute(sql_text)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return res