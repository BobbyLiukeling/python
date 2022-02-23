import pymysql

connect = pymysql.Connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="867425",
    db="zhichengariticle",
    charset="utf8"
)
cursor = connect.cursor()
sql = "SELECT * from question "

cursor.execute(sql)
N = cursor.fetchall()
article = []
for i in N:
    print(i)
