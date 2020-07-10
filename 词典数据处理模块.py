'''
数据处理模块
    根据dict_server的指令获取
    与数据库交互
'''
import pymysql

class Database:
    def __init__(self):
        # 链接数据库
        self.db = pymysql.connect(host="localhost",
                             port=3306,
                             user="root",
                             password='123456',
                             database="dict",
                             charset="utf8")

    def cursor(self):
        # 创建游标 (调用sql语句,获取执行结果)
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        # 关闭游标和数据库
        self.cur.close()
        self.db.close()

    #注册
    def register(self,name,passwd):
        sql = 'select name from user where name=%s;'
        self.cur.execute(sql,[name])
        r = self.cur.fetchone()#获取结果
        #查询到结果则不允许注册
        if r:
            return False

        #讲信息插入数据库
        sql = 'insert into user (name,passwd) values (%s,%s);'
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    #登录
    def login(self,name,passwd):
        sql = 'select name from user where name=%s and passwd=%s;'
        self.cur.execute(sql,[name,passwd])
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    #插入历史记录
    def insert_history(self,name,word):
        sql = 'select id from user where name=%s;'
        self.cur.execute(sql,[name])
        user_id = self.cur.fetchone()[0]
        #插入历史记录
        sql = 'insert into hist (word,user_id) values (%s,%s);'
        try:
            self.cur.execute(sql,[word,user_id])
            self.db.commit()
        except:
            self.db.rollback()

    #查单词
    def query(self,word):
        sql = 'select mean from words where word=%s ;'
        self.cur.execute(sql,[word])
        r = self.cur.fetchone()
        if r:
            return r[0]

    #查询历史记录
    def history(self,name):
        # name word time
        sql = 'select name,word,time from user inner join hist on user.id=hist.user_id where name =%s order by time desc limit 10;'
        self.cur.execute(sql,[name])

        #((name,word,time),(),())
        return self.cur.fetchall()

































