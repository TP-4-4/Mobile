from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

kv = '''
#:import KivyLexer kivy.extras.highlight.KivyLexer
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer

BoxLayout:

    # CodeInput:
    #     lexer: KivyLexer()
    #     style_name: "native"
    #     on_text: app.update_kv_file(self.text)
    #     size_hint_x: .7

    HotReloadViewer:
        size_hint_x: .3
        path: app.path_to_kv_file
        errors: True
        errors_text_color: 1, 0, 0, 1
        errors_background_color: app.theme_cls.bg_dark

'''

class OrderScreen(Screen):
    path_to_kv_file = "styles/style_for_order.kv"

    def on_enter(self):
        Window.size = (1080 / 3, 2000 / 3)
        self.load_kv()


    def load_kv(self):
        with open(self.path_to_kv_file, "r", encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

    def update_kv_file(self, text):
        with open(self.path_to_kv_file, "w") as kv_file:
            kv_file.write(text)


# app = MyApp()
# app.run()