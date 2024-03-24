from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import re
from kivy.lang import Builder
from kivy.core.window import Window

from login_screen import LoginScreen
from profile_screen import ProfileScreen
from order_screen import OrderScreen


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

class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    number_ord = 123456
    summa = 1234
    addres = 'Ул. Станкевича, кв. 36'
    image = CoreImage("img/logo.png")
    width = image.width
    height = image.height


    def build(self):
        #self.theme_cls.theme_style = "Light"
        sm = ScreenManager()
        sm.add_widget(OrderScreen(name="order_screen"))
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(ProfileScreen(name="profile_screen"))


        return Builder.load_file("styles/style_for_main.kv")
       # return sm

    def switch_to_login_screen(self):
        self.root.current = "login_screen"

    def submit_login_data(self, phone_number, password):
        # Получаем экземпляр LoginScreen из ScreenManager
        login_screen = self.root.get_screen("login_screen")
        # Вызываем метод submit_data
        login_screen.submit_data(phone_number, password)

    def switch_to_order_screen(self):
        self.root.current = "order_screen"

    def switch_to_profile_screen(self):
        self.root.current = "profile_screen"


if __name__ == "__main__":
    app = MyApp()
    app.run()