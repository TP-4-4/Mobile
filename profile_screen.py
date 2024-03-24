from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage

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

class ProfileScreen(Screen):
    path_to_kv_file = "styles/style_for_profile.kv"
    last_name = 'Лобова'
    name = 'Екатерина'
    otchectvo = 'Николаевна'
    databirth = '2003-08-08'
    number = '+79518579473'

    image = CoreImage("img/logo.png")
    width = image.width
    height = image.height

    def on_enter(self):
        Window.size = (1080 / 3, 2000 / 3)
        self.load_kv()

    def load_kv(self):
        with open(self.path_to_kv_file, "r", encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

    def update_kv_file(self, text):
        with open(self.path_to_kv_file, "w") as kv_file:
            kv_file.write(text)
