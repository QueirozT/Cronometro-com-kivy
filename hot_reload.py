from kivy.lang import Builder
from kivymd.tools.hotreload.app import MDApp


class HotReload(MDApp):
    kV_FILES = ['app/cronometro.kv']
    DEBUG = True
    
    def build_app(self):
        return Builder.load_file('app/cronometro.kv')

        
HotReload().run()
