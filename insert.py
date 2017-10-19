# _*_ coding:utf-8 _*_

import pymysql
db = pymysql.connect(
                     host="47.93.5.189",
                      user="root",
                      password="edison",
                        database="spark",
                        charset="utf8"
                      )
cursor = db.cursor()

def update(txn,id):
    #sql = "update mzhan_user set age=%s where user_id=%s" % (int(str(id)[-2:]),id )
    #txn.execute(sql)
    try:
        sql = "insert into person(name,age) VALUES ('%s',%s)" %(id[1], int(str(id[0])[-2:]))
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
    pass

ids = []
with open('data') as f:
    import json
    ids = json.loads(f.read())
for item in ids:
    print(item)
    update("", item)
