#!/home/dkundapura/.virtualenvs/harman_bot/bin/python
import pymysql
print("Trying to establish connection")
conn = pymysql.connect("dkundapura.mysql.pythonanywhere-services.com", "dkundapura", "liaison@123", "dkundapura$harman")
#conn = pymssql.connect("127.0.0.1:3306", "dkundapura", "liaison@123", "dkundapura$harman")
cursor = conn.cursor()
#cursor.execute('SELECT * FROM Users')

f = open("cas_users.csv", "rt")
y = f.readline()
y = f.readline()
while (y):
    insert_string = "insert into Users (user_id,lastname,firstname,middlename,suffix,title,username,password,email,dateadded,cas_id) values ('"
    a=y.rstrip().split(",")
    j="','"
    j = j.join(a)
    insert_string = insert_string + j + "');"
    print(insert_string)
    cursor.execute(insert_string)
    y = f.readline()
conn.commit()    
conn.close()
