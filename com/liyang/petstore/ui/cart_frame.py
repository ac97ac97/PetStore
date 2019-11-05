# 商品购物车窗口
import datetime
import sys
import wx
import wx.grid
import pymysql
import configparser


# import carttable

class BaseDao(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='petstore',
            charset='utf8'

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
                sql = 'select orderid,userid,orderdate from  orders'
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

    def create(self, order):
        # 创建订单插入到数据库
        orders = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'insert into orders (orderid,userid,orderdate,status,amount) values(%s,%s,%s,%s,%s)'
                affectedcount = cursor.execute(sql, order)
                print('成功插入{0}条数据'.format(affectedcount))
                self.conn.commit()
        except pymysql.DatabaseError as e:
            self.conn.rollback()
            print(e)

        finally:
            self.close()


class OrderDetailDao(BaseDao):
    def __init__(self):
        super().__init__()

    def create(self, order):
        # 创建订单明细插入到数据库
        try:
            with self.conn.cursor() as cursor:
                sql = 'insert into orderdetails (orderid,productid,quantity,unitcost) values(%s,%s,%s,%s)'
                self.conn.commit()
        except pymysql.DatabaseError as e:
            self.conn.rollback()
            print(e)

        finally:
            self.close()


class ProductDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findall(self):
        # 查询所有商品信息
        products = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'select productid,category,cname,ename,image,descn,listprice ,unitcost from  products'
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

    def findbycat(self, catname):
        # 按照商品类别查询商品
        products = []
        try:
            with self.conn.cursor() as cursor:
                sql = 'select productid,category,cname,ename,image,descn,listprice ,unitcost from  products where category=%s'
                cursor.execute(sql, catname)
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
                sql = 'select productid,cateory,cname,ename,image,descn,listprice ,unitcost from  products where productid = %s'
                cursor.execute(sql, productid)
                row = cursor.fetchone()

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


class MyFrame(wx.Frame):
    # 用户登录成功 保存当前登录用户信息
    Session = {}

    def __init__(self, title, size):
        super().__init__(parent=None, title=title, size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)

        self.Center()
        self.contentpanel = wx.Panel(parent=self)
        ico = wx.Icon('F:\\Python_project\\py_for\\venv\\src\\ctrl_project3\\PetStore\\resources\\icon\\dog4.ico',
                      wx.BITMAP_TYPE_JPEG)
        # 设置窗口图标
        self.SetIcon(ico)
        # 设置窗口的最大和最想尺寸
        self.SetSizeHints(size, size)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, evt):
        # 退出系统
        # 退出占有资源
        self.Destroy()
        # 退出系统
        sys.exit(0)
# 自定义gridtablebase类 用于购物出网格

# 购物车网格列名

COLUMUN_NAMES=['商品编号','商品名','商品单价','数量','商品应付金额']

class CartGridTable(wx.grid.GridTableBase):
    def __init__(self,data):
        super().__init__()
        self.colLabels=COLUMUN_NAMES
        self.data=data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(COLUMUN_NAMES)

    def GetValue(self, rowidx, colidx):
        product=self.data[rowidx]

        if colidx == 0:
            return product['productid']
        elif colidx ==1:
            return product['cname']
        elif colidx ==2:
            return product['unitcost']
        elif colidx ==3:
            return product['quantity']
        else:
            return product['amount']

    def GetColLabelValue(self, colidx):
        return self.colLabels[colidx]

    def SetValue(self, rowidx, colidx, value):
        # 只允许修改数量列

        if colidx !=3:
            return
        #获得商品数量
        try:
            quantity=int(value)
        except:
            # 输入非数字不能修改
            return
        # 商品数量不能小于0
        if quantity < 0:
            return

        # 更新数量列
        self.data[rowidx]['quantity'] = quantity
        # 计算商品应付金额
        amount=self.data[rowidx]['unitcost'] * quantity
        # 更新商品应付金额列
        self.data[rowidx]['amount']=amount

class CartFrame(MyFrame):
    def __init__(self,cart,product_list_frame):
        super().__init__(title="商品购物车", size=(1000, 700))

        # 购物车，键是选择商品id 值是商品的数量
        self.cart = cart
        self.product_list_frame = product_list_frame
        # 加载数据到data
        self.data = self.loaddata()
        # 设置整个窗口的布局是垂直box布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.contentpanel.SetSizer(vbox)

        # 添加顶部对象（topbox）到vbox
        vbox.Add(self.createtopbox(), 1, flag=wx.EXPAND | wx.ALL, border=10)
        # 添加底部对象grid到vbox
        vbox.Add(self.creategrid(), 1, flag=wx.CENTER | wx.FIXED_MINSIZE | wx.ALL, border=10)

        # 为当前frame对象添加默认状态栏
        self.CreateStatusBar()
        self.SetStatusText("准备就绪")

    def creategrid(self):
        # 创建购物表格
        # 创建网格对象
        grid = wx.grid.Grid(self.contentpanel, name='grid')

        # 初始化网格
        # 创建网格中所需要的表格
        table = CartGridTable(self.data)
        # 设置网格的表格属性
        grid.SetTable(table, True)
        grid.SetSizer(1000, 600)

        rowsizeinfo = wx.grid.GridSizesInfo(40, [])
        # 设置网格所有行高
        grid.SetRowSizes(rowsizeinfo)
        colsizeinfo = wx.grid.GridSizesInfo(176, [])
        # 设置网格所有列宽
        grid.SetColSizes(colsizeinfo)
        # 设置单元格默认字体

        grid.SetDefaultCellFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))
        # 设置行和列标题的默认字体
        grid.SetLabelFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))
        # 设置网格选择模式为行选择
        grid.SetSelectionMode(grid.wxGridSelectRows)
        # 设置不能通过拖动改变行高度
        grid.DisableDragRowSize()
        # 设置不能通过拖动改变 列宽度
        grid.DisableDragColSize()
        return grid

    def createtopbox(self):
        # 创建顶部布局管理器topbox
        # 创建按钮对象
        return_btn = wx.Button(parent=self.contentpanel, label="返回商品列表")
        sumbit_btn = wx.Button(parent=self.contentpanel, label="提交订单")
        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.return_btn_onclick, return_btn)
        self.Bind(wx.EVT_BUTTON, self.sumbit_btn_onclick, sumbit_btn)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.AddSpacer(350)
        box.Add(return_btn, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.AddSpacer(20)
        box.Add(sumbit_btn, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.AddSpacer(30)
        return box

    def loaddata(self):
        # 根据购物车中保存的商品id 查询出商品的其他属性
        data = []
        keys = self.cart.keys()
        for productid in keys:
            # 创建dao对象
            dao = ProductDao()
            product = dao.findbyid(productid)

            row = {}
            row['productid'] = product['productid']  # 商品编号
            row['cname'] = product['cname']  # 商品名
            row['unitcost'] = product['unitcost']  # 商品单价
            row['quantity'] = self.cart[productid]  # 数量
            # 计算商品应付金额
            amount = row['unitcost'] * row['quantity']
            row['amount'] = amount
            data.append(row)
        return data

    def return_btn_onclick(self, event):
        # 返回商品列表按钮处理
        # 更新购物车
        for gridrowdata in self.data:
            productid = gridrowdata['productid']  # 商品编号
            quantity = gridrowdata['quantity']  # 数量
            self.cart[productid] = quantity

        self.product_list_frame.Show()
        self.Hide()

    def sumbit_btn_onclick(self, event):
        # 提交按钮处理事件
        # 生成订单
        self.generateorders()
        dlg = wx.MessageDialog(self, '订单已生成，等待付款。', '信息', wx.YES_NO | wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_YES:
            # 等待付款
            print('等待付款...')
            pass  # 后期再此处添加功能性代码

        # 退出系统
        self.Destroy()
        sys.exit(0)
        dlg.Destroy()

    def generateorders(self):
        # 生成订单

        orderdate=datetime.datetime.today()
        # 从用户session中取出用户id
        userid=MyFrame.Session['userid']
        orderid=int(orderdate.timestamp() * 1000)
        status=0
        amount=self.getorderamount()

        order=orderid,userid,orderdate,status,amount

        # 下单时间由数据库自动生成不用设置

        # 穿件订单
        orderDao = OrderDao()
        orderDao.create(order)

        for row in self.data:
            orderdetail=orderid,row['productid'],row['quantity'],row['unitcost']
            orderdetaildao=OrderDetailDao()
            # 创建订单明细
            orderdetaildao.create(orderdetail)

    def getorderamount(self):
        #计算订单应付总金额
        totalamount=0.0
        for row in self.data:
            totalamount += float(row['amount'])

        return totalamount


