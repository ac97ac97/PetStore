"""用户登录窗口"""

import wx
import sys
import pymysql
import configparser
import wx.grid
import datetime

# from com.liyang.petstore.dao.account_dao.AccountDao import AccountDao

class MyFrame(wx.Frame):
    # 用户登录成功 保存当前登录用户信息
    Session = {}
    print(Session)

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

    def OnClose(self,evt):
        # 退出系统
        # 退出占有资源
        self.Destroy()
        # 退出系统
        sys.exit(0)


"""用户管理DAO"""
# from com.liyang.petstore.dao.base_dao import BaseDao

"""定义DAO基类"""



class BaseDao(object):
    def __init__(self):
        # self.config = configparser.ConfigParser()
        # self.config.read('config.ini', encoding='utf-8')
        # host = self.config['db']['host']
        # user = self.config['db']['user']
        # # 读取整数port数据
        # port = self.config.getint('db', 'port')
        # password = self.config['db']['password']
        # database = self.config['db']['database']
        # charset = self.config['db']['charset']
        # self.conn = pymysql.connect(
        #     host=host,
        #     user=user,
        #     port=port,
        #     password=password,
        #     database=database,
        #     charset=charset
        # )
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='petstore',
            charset='utf8'


         )

    def close(self):
        # 闭数据库连接
        self.conn.close();


class AccountDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findbyid(self, userid):
        account = None
        try:
            with self.conn.cursor() as cursor:
                # sql = 'select  userid,password,email,name,addr,city,country ,phone' \
                #       'from  accounts  where  userid=%s'
                sql='select * from accounts where userid =%s'
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
                sql = 'select productid,category,cname,ename,image,descn,listprice ,unitcost from  products where productid = %s'
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
        grid.SetSize(1000, 700)

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
        userid=LoginFrame.account['userid']
        print(userid+"调试------------")
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






# 自定义gridtablebase类用于商品网格

# 商品网格名
COLUMN_NAMES = ['商品编号', '商品类别', '商品中文名', '商品英文名']


class ProductListGridTable(wx.grid.GridTableBase):
    def __init__(self, data):
        super().__init__()
        self.colLables = COLUMN_NAMES
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(COLUMN_NAMES)

    def GetValue(self, rowidx, colidx):
        product = self.data[rowidx]
        if colidx == 0:
            return product['productid']

        elif colidx == 1:
            return product['category']

        elif colidx == 2:
            return product['cname']
        else:
            return product['ename']

    def GetColLabelValue(self, colidx):
        return self.colLables[colidx]

class LoginFrame(MyFrame):
    session = {}
    user = 'j2ee'
    def __init__(self):
        super().__init__(title='用户登录', size=(340, 230))
        # 创建页面控件
        accountid_st = wx.StaticText(self.contentpanel, label='账号:')
        password_st = wx.StaticText(self.contentpanel, label='密码:')

        self.accountid_txt = wx.TextCtrl(self.contentpanel)
        user = self.accountid_txt.GetValue()
        print(user+'--++--')

        self.password_txt = wx.TextCtrl(self.contentpanel, style=wx.TE_PASSWORD)
        # 创建FlexGrid布局fgs对象
        fgs = wx.FlexGridSizer(2, 2, 20, 20)
        fgs.AddMany([
            (accountid_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
            (self.accountid_txt, 1, wx.CENTER | wx.EXPAND),
            (password_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
            (self.password_txt, 1, wx.CENTER | wx.EXPAND)
        ])
        # 设置FlexGrid布局对象
        fgs.AddGrowableRow(0, 1)
        fgs.AddGrowableRow(1, 1)
        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 4)
        # 创建按扭对象
        okb_btn = wx.Button(parent=self.contentpanel, label='确定')
        self.Bind(wx.EVT_BUTTON, self.okb_btn_onclick, okb_btn)

        cancel_btn = wx.Button(parent=self.contentpanel, label='取消')
        self.Bind(wx.EVT_BUTTON, self.cancel_btn_onclick, cancel_btn)
        # 创建水平的hbox对象
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(okb_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        hbox.Add(cancel_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        # 创建垂直box将fgs和hbox添加到垂直box上
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(fgs, -1, wx.CENTER | wx.ALL | wx.EXPAND, border=25)
        vbox.Add(hbox, wx.CENTER, wx.BOTTOM, border=20)
        self.contentpanel.SetSizer(vbox)

    def okb_btn_onclick(self,event):
        # 确定按钮事件处理
        dao = AccountDao()
        account = dao.findbyid(self.accountid_txt.GetValue())
        password = self.password_txt.GetValue()
        if account is not None and account['password'] == password:

            print('登录成功')
            print(account)
            next_frame=ProductListFrame()
            next_frame.Show()
            self.Hide()

        else:
            print('登录失败')
            dlg = wx.MessageDialog(self, '您输入的账号或密码有错误，请重新输入。', '登录失败', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def cancel_btn_onclick(self, event):
        # 取消按钮事件
        self.Destroy()
        sys.exit(0)
    print(user)
    dao = AccountDao()
    account = dao.findbyid(user)
    print(account)


# 商品类别
CATEGORYS = ['鱼类', '狗类', '爬行类', '猫类', '鸟类']


class ProductListFrame(MyFrame):
    def __init__(self):
        super().__init__(title='商品列表窗口', size=(1000, 900))
        # 购物车 键是选择商品的id 值是商品的数量
        self.cart = {}
        # 选中商品
        self.selecteddata = {}
        # 创建dao对象
        dao = ProductDao()
        # 查询所有数据
        self.data = dao.findall()
        # 创建分窗口
        splitter = wx.SplitterWindow(self.contentpanel, style=wx.SP_3DBORDER)
        # 创建分窗口的左侧面板
        self.leftpanel = self.createleftpanel(splitter)
        # 创建分窗口的右面板
        self.rightpanel = self.createrightpanel(splitter)
        # 设置分隔窗口的左右布局
        splitter.SplitVertically(self.leftpanel, self.rightpanel, 630)
        # 设置最小的窗口尺寸
        splitter.SetMinimumPaneSize(630)
        # 设置整个窗口是垂直布局
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.contentpanel.SetSizer(vbox)
        # 添加顶部对象topbox到vbox
        vbox.Add(self.oncreatetopbox(), 1, flag=wx.EXPAND | wx.ALL, border=20)
        # 添加底部对象splitter到vbox中
        vbox.Add(splitter, 1, flag=wx.EXPAND | wx.ALL, border=10)
        # 当前创建frame对象创建并添加到默认状态栏中
        self.CreateStatusBar()
        self.SetStatusText('准备就绪')

    def oncreatetopbox(self):
        # 创建顶部布局管理器topbox
        # 创建静态文本
        pc_st = wx.StaticText(parent=self.contentpanel, label='选择商品类别： ', style=wx.ALIGN_RIGHT)
        # 创建按钮对象
        search_btn = wx.Button(parent=self.contentpanel, label='查询')
        reset_btn = wx.Button(parent=self.contentpanel, label='重置')
        choice = wx.Choice(self.contentpanel, choices=CATEGORYS, name='choice')
        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.search_btn_onclick, search_btn)
        self.Bind(wx.EVT_BUTTON, self.reset_btn_onclick, reset_btn)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.AddSpacer(200)
        box.Add(pc_st, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=10)
        box.Add(choice, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        box.Add(search_btn, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)
        box.Add(reset_btn, 1, flag=wx.FIXED_MINSIZE | wx.ALL, border=5)

        box.AddSpacer(260)
        return box

    def createleftpanel(self, parent):
        # 创建分隔窗口的左侧面板

        panel = wx.Panel(parent)

        # 创建网格对象
        grid = wx.grid.Grid(panel, name='grid')
        # 绑定网格处理事件
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.selectrow_handler)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.selectrow_handler)

        # 初始化网格
        self.initgrid()
        # 创建水平box管理器
        box = wx.BoxSizer(wx.HORIZONTAL)
        # 设置水平box管理grid网格
        box.Add(grid, 1, flag=wx.ALL, border=5)
        panel.SetSizer(box)
        return panel

    def initgrid(self):
        # 初始化网格对象
        #   网格名称获得网格对象
        grid = self.FindWindowByName('grid')
        # 创建网格中所需要的表格
        table = ProductListGridTable(self.data)
        # # 设置网格表格属性
        grid.SetTable(table, True)

        rowsizeinfo = wx.grid.GridSizesInfo(40, [])
        # 设置网格所有行高
        grid.SetRowSizes(rowsizeinfo)
        colsizeinfo = wx.grid.GridSizesInfo(0, [100, 80, 130, 200])
        # 设置网格列宽
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

    def createrightpanel(self, parent):
        # 创建分隔窗口的右侧面板
        # panel = wx.Panel(parent, wx.TAB_TRAVERSAL | wx.BORDER_DOUBLE)
        panel = wx.Panel(parent)
        panel.SetBackgroundColour(wx.WHITE)

        # 显示第一张图片
        imagepath = 'F:\\Python_project\\py_for\\venv\\src\\ctrl_project3\\PetStore\\resources\\images\\' + self.data[0]['image']
        # imagepath = ''
        image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
        image_sbitmap = wx.StaticBitmap(panel, bitmap=image, name='image_sbitmap')

        # 商品的市场价格
        slistprice = "商品市场价: ￥{0:.2f}".format(self.data[0]['listprice'])
        listprice_st = wx.StaticText(panel, label=slistprice, name='listprice')

        # 市场价格
        sunitcost = "商品单价: ￥{0:.2f}".format(self.data[0]['unitcost'])
        unitcost_st = wx.StaticText(panel, label=sunitcost, name='unitcost')

        # 商品描述
        descn = "商品描述: {0}".format(self.data[0]['descn'])
        descn_st = wx.StaticText(panel, label=descn, name='descn')

        # 创建按钮对象
        addcart_btn = wx.Button(panel, label='添加购物车')
        seecart_btn = wx.Button(panel, label='查看购物车')
        # 绑定事件处理
        self.Bind(wx.EVT_BUTTON, self.addcart_btn_onclick, addcart_btn)
        self.Bind(wx.EVT_BUTTON, self.seecart_btn_onclick, seecart_btn)

        box = wx.BoxSizer(wx.VERTICAL)
        box.AddSpacer(50)
        box.Add(image_sbitmap, 1, flag=wx.CENTER | wx.ALL, border=30)
        box.AddSpacer(50)
        box.Add(listprice_st, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.Add(unitcost_st, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.Add(descn_st, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.AddSpacer(20)
        box.Add(addcart_btn, 1, flag=wx.EXPAND | wx.ALL, border=10)
        box.Add(seecart_btn, 1, flag=wx.EXPAND | wx.ALL, border=10)
        panel.SetSizer(box)

        return panel

    def search_btn_onclick(self, event):
        # 查询1按钮处理事件

        # 通过名称查询choice控价
        choice = self.FindWindowByName('choice')
        # 获得选中类别索引
        selectcatidx = choice.GetSelection()

        if selectcatidx >= 0:
            # 获得选中商品类别
            catename = CATEGORYS[selectcatidx]

            # 根据类别查询dao
            dao = ProductDao()
            self.data = dao.findbycat(catename)

            # 初始化网格
            self.initgrid()

    def reset_btn_onclick(self, event):
        # 重置按钮处理事件

        # 查询所有商品
        dao = ProductDao()
        self.data = dao.findall()
        # 初始化网格
        self.initgrid()

    def addcart_btn_onclick(self, event):
        # 添加购物车事件处理

        if len(self.selecteddata) == 0:
            self.SetStatusText('请先选择商品')
            return
        # 获得选择的商品id
        productid = self.selecteddata['productid']
        if productid in self.cart.keys():  # 判断购物车是否有该商品
            # 获得商品数量
            quantity = self.cart[productid]
            self.cart[productid] = (quantity + 1)
        else:  # 购购物车中还没有商品
            self.cart[productid] = 1

        # 显示在状态栏
        self.SetStatusText('商品{0}添加到购物车'.format(productid))
        print(self.cart)

    def seecart_btn_onclick(self,event):
        # 查看添加到购物车事件处理

        next_frame=CartFrame(self.cart,self)
        next_frame.Show()
        self.Hide()

    def selectrow_handler(self, event):
        # 选择网格行事件处理
        srowidx = event.GetRow()
        if srowidx >= 0:
            print(self.data[srowidx])
            self.selecteddata = self.data[srowidx]
            self.SetStatusText('选择第{0}行数据'.format(srowidx + 1))
            #F:\Python_project\py_for\venv\src\ctrl_project3\PetStore\resources\images\fish3.jpg
            # 显示选择的照片
            imagepath = 'F:\\Python_project\\py_for\\venv\\src\\ctrl_project3\\PetStore\\resources\\images\\' + self.selecteddata['image']
            # imagepath = ''
            image = wx.Bitmap(imagepath, wx.BITMAP_TYPE_ANY)
            # 通过名称查询子窗口
            image_sbitmap = self.FindWindowByName('image_sbitmap')
            image_sbitmap.SetBitmap(image)

            # 商品的市场价格
            slistprice = "商品市场价: ￥{0:.2f}".format(self.selecteddata['listprice'])
            listprice_st = self.FindWindowByName('listprice')
            listprice_st.SetLabelText(slistprice)

            # 市场价格
            sunitcost = "商品单价: ￥{0:.2f}".format(self.selecteddata['unitcost'])
            unitcost_st = self.FindWindowByName('unitcost')
            unitcost_st.SetLabelText(sunitcost)

            # 商品描述
            descn = "商品描述: {0}".format(self.selecteddata['descn'])
            descn_st = self.FindWindowByName('descn')
            descn_st.SetLabelText(descn)

            self.rightpanel.Layout()

        event.Skip()




class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        loginFrame = LoginFrame()
        loginFrame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主事件循环
