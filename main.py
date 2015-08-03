from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
    def dataReceived(self, data):
        pass

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app
    def clientConnectionLost(self, conn, reason):
        pass
    def clientConnectionFailed(self, conn, reason):
        pass
    
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
from kivy.uix.image import Image, AsyncImage
from kivy.core.image import Image as CoreImage
import time, io


class Monitoring(Screen):  
    def __init__(self,app,**kwargs):
        super(Monitoring, self).__init__(**kwargs)
        Clock.schedule_interval(self.screen,.01)
        self.app = app
        self.premisson = True
        self.x = 0

    def screen(self,dt):
        self.add_widget(AsyncImage(source = "http://192.168.93.50:8080/static/arman/0.jpg", nocache = True,allow_stretch = True,keep_ratio = False ))
    def on_touch_down(self,touch):
        if self.app.transport:
            self.app.transport.write(str([[touch.x/Window.width,(Window.height-touch.y)/Window.height],False])+'va')

    def on_touch_up(self,touch):
        if self.app.transport:
            self.app.transport.write(str([[touch.x/Window.width,(Window.height-touch.y)/Window.height],True])+'va')

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    def build(self):
        reactor.connectTCP('192.168.93.50', 8000, EchoFactory(self))
        sm = ScreenManager()
        self.a = Monitoring(self,name='Monitor')
        sm.add_widget(self.a)
        sm.current = 'Monitor'
        self.sm = sm
        return sm
    def on_connection(self,transport):
        self.transport = transport
        return self.transport
if __name__ == '__main__':
    TwistedClientApp().run()
