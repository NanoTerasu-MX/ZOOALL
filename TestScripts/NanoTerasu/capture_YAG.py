import WebSocketBSS
import Capture
import time
import os

if __name__=="__main__":
    capture_dir = "/data/mxstaff/AlignmentData/2025B/251108/monitor_beam/"
    websock = WebSocketBSS.WebSocketBSS()
    cap = Capture.Capture()
    cap.prep()
    cap.setBright(15000)

    for i in range(1,1001):
        fname_cross=os.path.join(capture_dir,
                                 f"cross_{i:03d}.ppm")
        fname_nocross=os.path.join(capture_dir,
                                   f"nocross_{i:03d}.ppm")
        websock.shutter("open")
        time.sleep(1.0)
        cap.capture(fname_nocross,cross=False,wait_time=2.0)
        cap.capture(fname_cross,cross=True,wait_time=2.0)
        time.sleep(1.0)
        cap.unsetCross()
        websock.shutter("close")
        time.sleep(54.0)
