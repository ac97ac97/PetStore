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


class OrderDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findall(self):
        # 查询查询所有商品的订单信息
        orders = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'select orderid,userid,orderdate' \
                      'from  orders'
                cursor.execute(sql)
                result_set = cursor.fetchall()

                for row in result_set:
                    order = {}
                    order['orderid'] = row[0]
                    order['userid'] = row[1]
                    order['orderdate'] = row[2]
                    orders.append(order)

        finally:
            self.close()

        return orders

    def create(self,order):
        # 创建订单插入到数据库
        orders = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'insert into orders (orderid,userid,orderdate,status,amount) ' \
                      'values(%s,%s,%s,%s,%s)'
                affectedcount=cursor.execute(sql,order)
                print('成功插入{0}条数据'.format(affectedcount))
                self.conn.commit()
        except pymysql.DatabaseError as e:
            self.conn.rollback()
            print(e)

        finally:
            self.close()

