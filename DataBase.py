import sqlite3


def create_table():
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = '''CREATE TABLE Ds
               (QID NUMBER PRIMARY KEY,
                STU_ID NUMBER,
                NAME VARCHAR(255),
                CLASS VARCHAR(255));'''
    cursor.execute(sql_text)
    connection.close()


def insert_into(QID):
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    Stu_Number = 'NULL'
    Name = 'NULL'
    Class = 'NULL'
    data = (QID, Stu_Number, Name, Class)
    sql_text = "INSERT INTO Ds VALUES(?,?,?,?)"
    cursor.execute(sql_text, data)
    connection.commit()
    connection.close()


def update_stu_number(data, QID):
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    data = (data, QID)
    sql_text = "UPDATE Ds set STU_ID =?  where QID =?"
    cursor.execute(sql_text, data)
    connection.commit()
    connection.close()


def update_name(data, QID):
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    data = (data, QID)
    sql_text = "UPDATE Ds set NAME =?  where QID =?"
    cursor.execute(sql_text, data)
    connection.commit()
    connection.close()


def update_class(data, QID):
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    data = (data, QID)
    sql_text = "UPDATE Ds set CLASS =?  where QID =?"
    cursor.execute(sql_text, data)
    connection.commit()
    connection.close()


def select_Name(QID):
    connection = sqlite3.connect('DataSave.db')
    cursor = connection.cursor()
    sql_text = "SELECT NAME FROM Ds WHERE QID=%d"%QID
    cursor.execute(sql_text)
    res=cursor.fetchall()
    cursor.close()
    connection.close()
    result = ''.join(str(res))
    result=result.lstrip("[('")
    result=result.rstrip("',)]")
    return result