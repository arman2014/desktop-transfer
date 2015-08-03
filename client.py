# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
An example client. Run simpleserv.py first before running this.
"""
from twisted.internet import reactor, protocol
# a client protocol
import PIL
from PIL import ImageGrab
from PIL import Image
import time, key_presser
from win32api import GetSystemMetrics
class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
        
    def connectionMade(self):
        ImageGrab.grab().save("n.jpg", "JPEG")
        """basewidth = 300#GetSystemMetrics(0)
        img = Image.open('n.jpg')
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        img.save('n.jpg')"""
        file = open('n.jpg','rb').read()    
        self.transport.write('shouroue shod'+file+'tamoom shod')
        print 'frstdm'
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        #print data
        xn = 0
        if 'gereftam' in data:
            xn = 1
            data  = data.replace('gereftam','')
        if '[' in data:
            print data
            data = data.split('va')
            
            for i in range(len(data)-1):
                print eval(data[i]) , 'hami'
                key_presser.Mouse().press_button(pos = ((int(eval(data[i])[0][0]*GetSystemMetrics(0)),int((eval(data[i])[0][1])*GetSystemMetrics(1)))),
                                                    button_name = "left",
                                                    button_up = eval(data[i])[1])
                print eval(data[i])[1], 'makhsouse'
        if xn == 1:
            self.connectionMade()
        
    def connectionLost(self, reason):
        print "connection lost"

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        print reason
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        print reason


    # this connects the protocol to a server running on port 8000
def main():
    f = EchoFactory()
    IP = raw_input("\"\"Server IP :\"\"")
    PORT = input("\"\"Server PORT(8000) :\"\"")
    reactor.connectTCP(IP, PORT, f)
    reactor.run()

    # this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
