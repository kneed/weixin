#coindg:utf-8
import pymysql

db=pymysql.connect(host="localhost",port=3306,user="root",password="739535841",db="dangdang",charset="utf8")#连接数据库
cursor=db.cursor()#获取一个可供操作数据库的游标
a=['xieke','kexie']
p=['$50','$55']
for i ,j in zip(a,p):
    cursor.execute('INSERT INTO python(name,price)values(%s,%s)',(i,j))
    db.commit()
    print('successful')
