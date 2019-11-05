""""定订单管理Dao类"""
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


class OrderDetailDao(BaseDao):
    def __init__(self):
        super().__init__()


    def create(self,order):
        # 创建订单明细插入到数据库
        try:
            with self.conn.cursor() as cursor:
                sql = 'insert into orderdetails (orderid,productid,quantity,unitcost) ' \
                      'values(%s,%s,%s,%s)'
                self.conn.commit()
        except pymysql.DatabaseError as e:
            self.conn.rollback()
            print(e)

        finally:
            self.close()



