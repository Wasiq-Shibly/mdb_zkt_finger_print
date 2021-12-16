import datetime
import pyodbc
import shutil
import time
from datetime import date

x=datetime.datetime.now()
#print(x)
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="attendance"
)

#start copy
original = r'C:\Program Files\ZKTeco\att2000.mdb'
target = r'C:\Users\Neways S & IT\Desktop\attsiam.mdb'
shutil.copyfile(original, target)
#copy file
conn = pyodbc.connect(
    r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Neways S & IT\Desktop\attsiam.mdb;'
    )
time_cursor = mydb.cursor()
sql = "SELECT max(date) from employee"
time_cursor.execute(sql)
time = time_cursor.fetchone()
print(time)

tmp_str = 'select USERINFO.Badgenumber, CHECKINOUT.CHECKTIME from CHECKINOUT INNER JOIN USERINFO on CHECKINOUT.USERID = USERINFO.USERID WHERE CHECKINOUT.CHECKTIME > #' + time[0].strftime('%m/%d/%Y %H:%M:%S %p') +'# '

cursor = conn.cursor()
cursor.execute(tmp_str)
result= cursor.fetchall()
mycursor = mydb.cursor()

for x in result:
    print("first loop:", x)
    mycursor = mydb.cursor()
    check_sql="SELECT date,employee_id from employee WHERE employee_id='"+x[0]+"' AND date LIKE '%"+ x[1].strftime('%y-%m-%d')+"%'"
    #print(check_sql)
    #print(x[0],x[10])
    mycursor.execute(check_sql)
    result2=mycursor.fetchall()
    if(len(result2)>0):

        print("                            in time vale: ",x[1],x[0],x[1])

        sql ="UPDATE employee SET `out_time` = '" +x[1].strftime('%H:%M:%S')+"' WHERE employee_id='"+x[0]+"' AND date LIKE '%"+ x[1].strftime('%y-%m-%d')+"%'"
        print(sql)
        mycursor.execute(sql)
        mydb.commit()

    else:
        sql = 'INSERT INTO employee (date,employee_id,in_time) VALUES (%s, %s, %s)'
        val = (x[1],x[0],x[1])
        mycursor.execute(sql, val)
        mydb.commit()
        print("out time :", x[1],x[0],x[1])


    # for y in result2:
    #     print("          2nd raw value: ",y)
