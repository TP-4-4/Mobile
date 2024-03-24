from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


class OrderScreen(Screen):
    path_to_kv_file = "styles/style_for_order.kv"

    def on_enter(self):
        Window.size = (1080 / 3, 2000 / 3)
        self.load_kv()


    def load_kv(self):
        with open(self.path_to_kv_file, "r", encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())
