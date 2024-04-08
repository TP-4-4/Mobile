from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from bd.database import SessionLocal
from screens.login_screen import LoginScreen
from screens.profile_screen import ProfileScreen
from screens.order_screen import OrderScreen



kv = '''
#:import KivyLexer kivy.extras.highlight.KivyLexer
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer

BoxLayout:

    # CodeInput:
    #     lexer: KivyLexer()
    #     style_name: 'native'
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
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_session = SessionLocal()
    def build(self):
        sm = WindowManager()
        Window.size = (1080 / 3, 2000 / 3)
        # Window.fullscreen = 'auto'
        sm.add_widget(OrderScreen(name='order_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(ProfileScreen(name='profile_screen'))

        return Builder.load_file('styles/style_for_main.kv')
        # return sm

    def submit_login_data(self, phone_number, password):
        login_screen = self.root.get_screen('login_screen')
        login_screen.submit_data(phone_number, password)


if __name__ == '__main__':
    app = MyApp()
    app.run()
