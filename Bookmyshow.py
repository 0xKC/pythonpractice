
import winsound
import urllib.request
import io
import threading
import time

exitFlag = 0
inorbit = "Inorbit Mall"
majeera = "Cinepolis"
forum = "suresh"
gvk = "GVK one"


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


class myThread (threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

        self.lol = "http://in.bookmyshow.com/getJSData/?file=/data/js/GetShowTimesByEvent_HYD_ET00032119_20160729.js&cmd=GETSHOWTIMESBYEVENTWEB&ec=ET00032119&dc=20160729&rc=HYD&_=1469786412509"
        self.dishoom = "https://in.bookmyshow.com/serv/getData/?cmd=GETSHOWTIMESBYEVENTANDVENUE&f=json&dc=20160729&vc=INHY&ec=ET00037453"
        self.gentleman = "https://in.bookmyshow.com/serv/getData/?cmd=GETSHOWTIMESBYEVENTANDVENUE&f=json&dc=20160729&vc=INHY&ec=ET00032119";
        self.bahubali="http://in.bookmyshow.com/getJSData/?file=/data/js/GetShowTimesByEvent_HYD_ET00016239_20150710.js&cmd=GETSHOWTIMESBYEVENTWEB&ec=ET00016239&dc=20150710&rc=HYD&_=1436260725";
    def run(self):
        while exitFlag == 0 :
            opener = AppURLopener()
            response = opener.open(self.dishoom)
            print(response)
            #response = urllib.request.urlopen(self.gentleman)
            buf = io.BytesIO(response.read())
            data = buf.read()
            my_decoded_str = data.decode(encoding="UTF-8")
           # print(my_decoded_str.lower())
            if inorbit.lower() in my_decoded_str.lower():
                print("FOUND : " + inorbit)
                winsound.Beep(100,2000)
            if majeera.lower() in my_decoded_str.lower():
                print("FOUND : " + majeera)
                winsound.Beep(200,2000)
            if forum.lower() in my_decoded_str.lower():
                print("FOUND : " + forum)
                winsound.Beep(300,2000)
            if gvk.lower() in my_decoded_str.lower():
                print("FOUND : " + gvk)
                winsound.Beep(400,2000)
            time.sleep(self.counter)

thread1 = myThread(2)
thread1.start()
