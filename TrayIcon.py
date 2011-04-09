import wx
import operator

class TrayIcon(wx.TaskBarIcon):
    def __init__(self,frame):
        super(TrayIcon, self).__init__()
        self.frame = frame
        self.SetIcon(self.get_icon(), "Power Managment")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.toggle_frame)
    
    def toggle_frame(self, m):
        f = self.frame
        csize = wx.ClientDisplayRect()[2:4]
        f.SetPosition(map(operator.__sub__,csize,f.GetSizeTuple()))
        f.Show(not f.IsShown())
    
    def get_icon(self):
        img = wx.EmptyBitmap(16,16)
        img.LoadFile("/home/roma/projects/pybattery/ico.png", wx.BITMAP_TYPE_ANY)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(img)
        return icon