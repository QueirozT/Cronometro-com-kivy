import sys
from itertools import cycle
        
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from plyer import vibrator, notification


class Cycle:
    """Define o Ciclo do Timer"""
    def __init__(self):
        self.cicle = cycle([Timer(1), Timer(2)])
    
    def __iter__(self):
        return self
        
    def __next__(self):
        return next(self.cicle)


class Timer:
    """Cria a Lógica do Timer"""
    def __init__(self, time):
        self.time = time * 60
        
    def decrementar(self):
        self.time -= 1
        return self.time
    
    def __str__(self):
        return '{:02d}:{:02d}'.format(*divmod(self.time, 60))


class SetTime(MDCard):
    value = StringProperty('')
    def fechar(self):
        if self.value.isnumeric():
            self.parent.cycle = cycle([Timer(int(self.value))])
            self.parent.timer_string = str(self.parent.cycle.__next__())
            self.parent._time = self.parent.cycle.__next__()
        self.parent.remove_widget(self)


class Pomodoro(MDFloatLayout):
    timer_string = StringProperty('00:00')
    button_string = StringProperty('Iniciar')
    running = BooleanProperty(False)
    cycle = cycle([Timer(0)])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._time = next(self.cycle)
        self.timer_string = str(self._time)
    
    def setTime(self):
        self.add_widget(SetTime())

    def start(self):
        self.button_string = 'Pausar'
        if not self.running:
            self.running = True
            self.timer_string = str(self._time)
            self.state = Clock.schedule_interval(self.update, 1)
        if self.timer_string == '00:00':
            self.cycle = cycle([Timer(0)])
            self.setTime()
    
    def stop(self):
        self.button_string = 'Iniciar'
        if self.running:
            self.running = False
            self.state.cancel()
    
    def click(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def update(self, *args):
        time = self._time.decrementar()
        self.timer_string = str(self._time)
        if time <= 0:
            self.stop()
            self._time = next(self.cycle)
            self.timer_string = '00:00'
            if sys.platform != 'win32' and sys.platform != 'linux':
                vibrator.vibrate(1)
                notification.notify('Alerta','O tempo acabou!')


class MeuApp(MDApp):
    def change_color(self):
        theme = self.theme_cls.theme_style
        if theme == 'Dark':
            self.theme_cls.theme_style = 'Light'
        else:
            self.theme_cls.theme_style = 'Dark'
    
    def build(self):
        self.theme_cls.primary_palette = 'DeepPurple'
        self.theme_cls.primary_hue = '700'
        return Builder.load_file('app/cronometro.kv')
