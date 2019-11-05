import sys
import wx

class MyFrame(wx.Frame):
    # 用户登录成功 保存当前登录用户信息
    Session={}
    def __init__(self,title,size):
        super().__init__(parent=None,title=title,size=size,style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)

        self.Center()
        self.contentpanel=wx.Panel(parent=self)
        icon=wx.Icon('F:\\Python_project\\py_for\\venv\\src\\ctrl_project3\\PetStore\\resources\\images\\dog4.jpg',wx.BITMAP_TYPE_ICO)
        # 设置窗口图标
        self.SetIcon(icon)
        # 设置窗口的最大和最想尺寸
        self.SetSizeHints(size,size)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
    def OnClose(self):
        # 退出系统
        # 退出占有资源
        self.Destroy()
        # 退出系统
        sys.exit(0)

