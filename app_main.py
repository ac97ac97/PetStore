import wx
# 省略基类 后续添加
class App(wx.App):
    def OnInit(self):
        frame = LoginFrame()
        frame.show()
        return True


if __name__=='__main__':
    app = App()
    app.MainLoop()