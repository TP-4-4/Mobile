from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
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

class MyApp(MDApp):
    path_to_kv_file = "styles/style_for_order.kv"

    image = CoreImage("img/logo.png")
    width = image.width
    height = image.height

    number_ord = 123456
    summa = 1234
    addres = 'Ул. Станкевича, кв. 36'

    def build(self):
        # Window.fullscreen = 'auto'
        Window.size = (1080 / 3, 2000 / 3)
        return Builder.load_string(kv)

    def update_kv_file(self, text):
        with open(self.path_to_kv_file, "w") as kv_file:
            kv_file.write(text)


app = MyApp()
app.run()