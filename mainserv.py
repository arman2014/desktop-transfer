
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet import reactor, protocol
from PIL import ImageGrab, Image
import time, key_presser
from win32api import GetSystemMetrics
from time import sleep
import thread

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        if '[' in data:
            data = data.split('va')
            for i in range(len(data)-1):
                key_presser.Mouse().press_button(pos = ((int(eval(data[i])[0][0]*GetSystemMetrics(0)),int((eval(data[i])[0][1])*GetSystemMetrics(1)))),
                                                    button_name = "left",
                                                    button_up = eval(data[i])[1])
                
def main():
    thread.start_new_thread(imager, ())
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    print ' server started at port 8000'
    reactor.run()
    

def imager():
    print 'ok'
    while 1:
        try:
            ImageGrab.grab().save("E:\Desktop\FekrAazin\static\\arman\{}.jpg".format(0), "JPEG")
        except Exception as x:
            print 'moshkele khasi naboud hal shd'
            print x
        sleep(.3)


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
