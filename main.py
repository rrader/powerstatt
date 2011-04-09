#!/usr/bin/python2
# -*- coding: utf-8 -*- 

import wx
import DataRetriever as dr
import sys

class TrayIcon(wx.TaskBarIcon):
    def __init__(self,frame):
        super(TrayIcon, self).__init__()
        self.frame = frame
        self.SetIcon(self.get_icon(), "Power Managment")
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.mouse_up)
    
    def mouse_up(self, m):
        self.frame.Show(not self.frame.IsShown())
    
    def get_icon(self):
        img = wx.EmptyBitmap(16,16)
        img.LoadFile("/home/roma/projects/pybattery/ico.png", wx.BITMAP_TYPE_ANY)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(img)
        return icon

class Main(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Battery state", style=wx.BORDER_DEFAULT, size=(240,120,))
        self.panel = wx.Panel(self, -1)
        self._params = {dr.BAT_CHARGINGSTATE : "Charging state",
                        dr.BAT_PRESENTRATE : "Present rate",
                        dr.BAT_PRESENTVOLTAGE : "Present voltage",
                        dr.BAT_REMAININGCAPACITY : "Remaining capacity"}
        self._ys=[10,35,60,85]
        make_text_ctrl = lambda y: wx.TextCtrl(self.panel, -1, "", pos=(150, y), style=wx.TE_READONLY, size=(80,-1))
        make_static_text = lambda text, y: wx.StaticText(self.panel, -1, text, pos=(10, y))
        self._st = map(make_static_text, self._params.values(), self._ys)
        self._ed = dict(zip( self._params, map(make_text_ctrl, self._ys) ))
        #updater
        self.info_getter = dr.IGSys("BAT0")
        self.fill_info(None)
        self.Bind(wx.EVT_TIMER, self.fill_info)
        self.timer = wx.Timer(self)
        self.timer.Start(3000)
        self.fill_info(None)
        self.tray = TrayIcon(self)
        
        
    def get_info(self):
        return self.info_getter.get_all_info()
        
    def fill_info(self, t):
        m = self.get_info()
        r = map(lambda x:m[x], self._params)
        map(lambda x,val:self._ed[x].SetValue(val), self._params, r)


class MyApp(wx.App):
    def OnInit(self):
        frame = Main(None)
        frame.Center(wx.BOTH)
        frame.Show(False)
        return True
    
def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    app = MyApp()
    app.MainLoop()
    
if __name__ == '__main__':
    main()