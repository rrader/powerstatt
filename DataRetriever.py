class EUnsupported(Exception): pass

BAT_CHARGINGSTATE = 1
BAT_PRESENTRATE = 2
BAT_PRESENTVOLTAGE = 3
BAT_REMAININGCAPACITY = 4

# Interface:
class InfoGetter(object):
    def get_info(self, name):
        raise NotImplementedError
    def get_all_info(self):
        raise NotImplementedError

class IGSys(InfoGetter):
    def __init__(self, bat="BAT0"):
        s = lambda f:(lambda:self._read_file("/sys/class/power_supply/"+bat+"/"+f))
        self._params={BAT_CHARGINGSTATE : s("status"),
                      BAT_PRESENTRATE: s("current_now"),
                      BAT_PRESENTVOLTAGE: s("voltage_now"),
                      BAT_REMAININGCAPACITY: s("charge_now")}
        
    def _read_file(self, f):
        fl = open(f, "rb")
        return fl.readline().strip()
        
    def get_info(self, name):
        try:
            return self._params[name]()
        except KeyError:
            raise EUnsupported(name+" is unsupported here")
    
    def get_all_info(self):
        return dict(zip(self._params.keys(),map(lambda x: x(), self._params.values())))