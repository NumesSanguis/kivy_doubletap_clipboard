#!/usr/bin/kivy
# -*- coding: utf-8 -*-
# Creator: SurafuSoft

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.utils import platform


__version__ = '0.1.0'

from kivy.core.text import LabelBase

KIVY_FONTS = [
    {
        "name": "MeiryoUI",
        "fn_regular": "Meiryo_UI_regular.ttf"
    }
]

for font in KIVY_FONTS:
    LabelBase.register(**font)

Clipboard = None
CutBuffer = None


class TouchLabel(Label):
    # TextInput(): https://github.com/kivy/kivy/blob/master/kivy/uix/textinput.py

    def __init__(self, **kwargs):
        self._touch_count = 0
        super(TouchLabel, self).__init__(**kwargs)
        self.register_event_type('on_double_tap')

        # if platform == 'linux':
        self._ensure_clipboard()

    def _ensure_clipboard(self):
        global Clipboard, CutBuffer
        if not Clipboard:
            from kivy.core.clipboard import Clipboard, CutBuffer

    def on_touch_down(self, touch):
        print("hello")
        if self.disabled:
            return

        touch_pos = touch.pos
        if not self.collide_point(*touch_pos):
            return False
        if super(TouchLabel, self).on_touch_down(touch):
            return True

        # TODO Crashes app on Android !!!
        print(self.text)

        touch.grab(self)
        self._touch_count += 1
        if touch.is_double_tap:
            self.dispatch('on_double_tap')

    def on_double_tap(self, *args):
        # TODO Also crashes app on Android !!!
        Clipboard.copy(self.text)  # <-- How do I do this the correct way?
        print("Copied :D")


class DoubletapClipboardInterface(BoxLayout):
    pass


class DoubletapClipboardApp(App):

    def build(self):
        self.title = 'DoubletapClipboard'

        return(DoubletapClipboardInterface())


if __name__ == '__main__':
    DoubletapClipboardApp().run()
