"""@Author : ArmanBabaie"""
#showing client's desktop by using twisted and kivy
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet import protocol

m_pos = [[1,0],2]
sc_n = 0
f_data = ''
event = 'mouse'
class EchoProtocol(protocol.Protocol):
    global m_pos, sc_n, f_data, event
    def connectionMade(self,):
        self.factory.app.on_connection(self.transport)
    def dataReceived(self, data):
        global m_pos, sc_n, f_data, event
        "As soon as any data is received, write it back."
        if 'shouroue shod'  not in data and 'tamoom shod' not in data:
            f_data += data
        if 'shouroue shod' in data:
            data = data.replace('shouroue shod','')
            f_data = data
        if 'tamoom shod' in data:
            data = data.replace('tamoom shod','')
            f_data += data
            self.factory.app.view(data)
            self.transport.write('gereftam')
            file = open('images/'+str(sc_n+1)+'.jpg','wb')
            file.write(f_data)
            file.close()
            sc_n+=1
            f_data = ''
            event = 'img'

class EchoFactory(protocol.Factory):
    protocol = EchoProtocol

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, WipeTransition, SlideTransition, SwapTransition
from kivy.graphics import *
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import time, io

class Monitoring(Screen):
    
    global sc_n, m_pos
    
    def __init__(self,app,**kwargs):
        super(Monitoring, self).__init__(**kwargs)
        #Clock.schedule_interval(self.screen,.001)
        self.app = app
        self.app.transport = None
        self.premisson = True
        self.x = 0

    def screen(self, data):
        global sc_n
        self.add_widget(Image(source = 'images/'+str(sc_n)+'.jpg',
                              allow_stretch = True,
                              keep_ratio = False,
                              nocache = True,))
        """if self.premisson:
            self.x+=1
            self.premisson = False
            f = open('images/'+str(self.x)+'.jpg','wb')
            f.write(data)
            f.close()
            self.app.transport.write('gereftam')
            time.sleep(.1)
            self.premisson = True
            print " It's drew
                yeah!"
        """
        
    def on_touch_down(self,touch):
        global m_pos
        if self.app.transport:
            self.app.transport.write(str([[touch.x/Window.width,(Window.height-touch.y)/Window.height],False])+'va')

    def on_touch_up(self,touch):
        global m_pos
        if self.app.transport:
            self.app.transport.write(str([[touch.x/Window.width,(Window.height-touch.y)/Window.height],True])+'va')



class TwistedServerApp(App):
    def build(self):
        sm = ScreenManager()
        self.a = Monitoring(self,name='Monitor')
        sm.add_widget(self.a)
        sm.current = 'Monitor'
        self.sm = sm
        reactor.listenTCP(8080, EchoFactory(self))
        return sm
    def view(self,data):
        self.a.screen(data)
    def on_connection(self,transport):
        self.transport = transport
        print 'connection :)'

        return msg
    
if __name__ == '__main__':
    TwistedServerApp().run()
