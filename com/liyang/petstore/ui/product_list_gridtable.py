import wx.grid

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
