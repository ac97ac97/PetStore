""""定义DAO基类"""
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


class ProductDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findall(self):
        # 查询所有商品信息
        products = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'select productid,cateory,cname,ename,image,descn,listprice ,unitcost' \
                      'from  products'
                cursor.execute(sql)
                result_all = cursor.fetchall()

                for row in result_all:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['descn'] = row[5]
                    product['listprice'] = row[6]
                    product['unitcost'] = row[7]
                    products.append(product)

        finally:
            self.close()

        return products

    def findbycat(self,catname):
        # 按照商品类别查询商品
        products = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'select productid,cateory,cname,ename,image,descn,listprice ,unitcost' \
                      'from  products where cateory=%s'
                cursor.execute(sql,catname)
                result_set = cursor.fetchall()

                for row in result_set:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['descn'] = row[5]
                    product['listprice'] = row[6]
                    product['unitcost'] = row[7]
                    products.append(product)

        finally:
            self.close()

        return products

    def findbyid(self, productid):
        # 按照商品类别查询商品
        products = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'select productid,cateory,cname,ename,image,descn,listprice ,unitcost' \
                      'from  products where productid=%s'
                cursor.execute(sql, productid)
                row=cursor.fetchone()

                if row is not None:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['descn'] = row[5]
                    product['listprice'] = row[6]
                    product['unitcost'] = row[7]

        finally:
            self.close()

        return product