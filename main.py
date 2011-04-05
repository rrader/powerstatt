#!/usr/bin/python2
# -*- coding: utf-8 -*- 

import wx
import re

class EUnsupported(Exception): pass

# Interface:
class InfoGetter(object):
    def get_info(self, name):
        pass
    def get_all_info(self):
        pass
    
class IGSys(InfoGetter):
    def __init__(self, bat="BAT0"):
        s = lambda f:"/sys/class/power_supply/"+bat+"/"+f
        self._params={"charging state" : s("status"),
                      "present rate": s("current_now"),
                      "present voltage": s("voltage_now"),
                      "remaining capacity": s("charge_now")}
        
    def _read_file(self, f):
        fl = open(f, "rb")
        return fl.readline().strip()
        
    def get_info(self, name):
        try:
            fl = self._params[name]
            return self._read_file(fl)
        except KeyError:
            raise EUnsupported(name+" is unsupported here")
    
    def get_all_info(self):
        return dict(zip(self._params.keys(),map(lambda x: self._read_file(x), self._params.values())))

class IGProc(InfoGetter):
    def __init__(self, bat="BAT0"):
        self.file = "/proc/acpi/battery/"+bat+"/state"
        
    def get_info(self, name):
        f = open(self.file, "rb")
        l = f.readlines()
        try:
            return dict(map(lambda x:[x[1], x[2]], map(lambda m:re.split("(.*): *(.*)", m), l)))[name]
        except KeyError:
            raise EUnsupported(name+" is unsupported here")
        f.close()
        
    def get_all_info(self):
        f = open(self.file, "rb")
        l = f.readlines()
        return dict(map(lambda x:[x[1], x[2]], map(lambda m:re.split("(.*): *(.*)", m), l)))
        f.close()

class Main(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Battery state", style=wx.BORDER_DEFAULT, size=(240,120,))
        self.panel = wx.Panel(self, -1)
        self._params=["charging state", "present rate", "present voltage", "remaining capacity"]
        self._ys=[10,35,60,85]
        make_text_ctrl = lambda y: wx.TextCtrl(self.panel, -1, "", pos=(150, y), style=wx.TE_READONLY, size=(80,-1))
        make_static_text = lambda text, y: wx.StaticText(self.panel, -1, text, pos=(10, y))
        self._st = map(make_static_text, self._params, self._ys)
        self._ed = dict(zip( self._params, map(make_text_ctrl, self._ys) ))
        #updater
        self.info_getter = IGSys("BAT0")
        self.fill_info(None)
        self.Bind(wx.EVT_TIMER, self.fill_info)
        self.timer = wx.Timer(self)
        self.timer.Start(3000)
        self.fill_info(None)
        
    def get_info(self):
        return self.info_getter.get_all_info()
        
    def fill_info(self, t):
        m = self.get_info()
        r = map(lambda x:m[x], self._params)
        map(lambda x,val:self._ed[x].SetValue(val), self._params, r)
        
    
if __name__ == '__main__':
    app = wx.App()
    m=Main(None)
    m.Show();
    app.MainLoop()
    
