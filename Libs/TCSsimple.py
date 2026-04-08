import time
from Motor import *
import BSSconfig

class TCSsimple:
    def __init__(self, server, config):
        self.s = server

        bssconf = BSSconfig.BSSconfig()
        bl_object = bssconf.getBLobject()
        # TCスリットの情報をbeamline.iniから取得
        slit_name = config.get("axes", "tc_slits")
        self.tcs_height = Motor(self.s, f"bl_{bl_object}_{slit_name}_height", "mm")
        self.tcs_width = Motor(self.s, f"bl_{bl_object}_{slit_name}_width", "mm")
        self.tcs_vert = Motor(self.s, f"bl_{bl_object}_{slit_name}_vertical", "mm")
        self.tcs_hori = Motor(self.s, f"bl_{bl_object}_{slit_name}_horizontal", "mm")

    def getApert(self):
        # get values
        self.ini_height = self.tcs_height.getApert()
        self.ini_width = self.tcs_width.getApert()
        return float(self.ini_height[0]), float(self.ini_width[0])

    def setApert(self, height, width):
        self.tcs_height.move(height)
        self.tcs_width.move(width)
        print("current tcs aperture : %8.5f %8.5f\n" % (height, width))

if __name__ == "__main__":
    import socket
    import os
    from configparser import ConfigParser, ExtendedInterpolation

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("%s/beamline.ini" % os.environ['ZOOCONFIGPATH']) 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.get('server','blanc_address'), 10101))

    tcs = TCSsimple(s, config)
    h, w = tcs.getApert()
    print("Initial aperture: %8.5f %8.5f\n" % (h, w))
    # tcs.setApert(0.3, 0.2)
    # time.sleep(2)
    # h, w = tcs.getApert()
    # print("New aperture: %8.5f %8.5f\n" % (h, w))
