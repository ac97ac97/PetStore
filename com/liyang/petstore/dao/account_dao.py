"""用户管理DAO"""
from com.liyang.petstore.dao.base_dao import BaseDao

"""定义DAO基类"""
import pymysql
import configparser


class BaseDao(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        host = self.config['db']['host']
        user = self.config['db']['user']
        # 读取整数port数据
        port = self.config.getint('db', 'port')
        password = self.config['db']['password']
        database = self.config['db']['database']
        charset = self.config['db']['charset']
        self.conn = pymysql.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database,
            charset=charset
        )

    def close(self):
        """"关闭数据库连接"""
        self.conn.close();


class AccountDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findbyid(self, userid):
        account = None
        try:
            with self.conn.cursor() as cursor:
                sql = 'select  userid,password,email,name,addr,city,country ,phone' \
                      'from  accounts  where  userid=%s'
                # sql='select * from accounts where userid =%s'
                cursor.execute(sql, userid)
                row = cursor.fetchone()
                if row is not None:
                    account = {}
                    account['userid'] = row[0]
                    account['password'] = row[1]
                    account['email'] = row[2]
                    account['name'] = row[3]
                    account['addr'] = row[4]
                    account['city'] = row[5]
                    account['country'] = row[6]
                    account['phone'] = row[7]
        finally:
            self.close()
        return account
