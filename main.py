import bcrypt
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from bd.database import SessionLocal
from clear_cache import clear_cache_folder
from models.order import Order
from screens.login_screen import LoginScreen
from screens.one_order_screen import OneOrderScreen
from screens.profile_screen import ProfileScreen
from screens.orders_screen import OrdersScreen
from services.map import MapBuilder

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
    current_order_id = None
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_session = SessionLocal()
        self.map_builder = MapBuilder()
        self.icon = 'img/icon.png'

    def on_pause(self):
        # This method is called when the application is paused.
        # Returning True indicates that the app can be paused.
        print("Application is pausing...")
        self.map_builder.start_background_service()
        return True

    def on_resume(self):
        # This method is called when the application is resumed.
        print("Application is resuming...")
        self.map_builder.stop_background_service()

    def build(self):
        self.root = WindowManager()  # Set WindowManager as the root
        Window.fullscreen = 'auto'

        self.root.add_widget(OrdersScreen(name='orders_screen'))
        self.root.add_widget(OneOrderScreen(name='one_order_screen'))
        self.root.add_widget(LoginScreen(name='login_screen'))
        self.root.add_widget(ProfileScreen(name='profile_screen'))


        return Builder.load_file('styles/style_for_main.kv')


    def submit_login_data(self, phone_number, password):
        login_screen = self.root.get_screen('login_screen')
        if login_screen:
            login_screen.submit_data(self.db_session, phone_number, password, self.map_builder)




def encrypt_password(password):
    # Генерация соли
    salt = bcrypt.gensalt()
    # Хэширование пароля с использованием соли
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


if __name__ == '__main__':
    clear_cache_folder()
    password = '1'
    encrypted_password = encrypt_password(password)
    print("Зашифрованный пароль:", encrypted_password)
    #  Зашифрованный пароль: b'$2b$12$6pVGF6spEu7C5JSOC56Bguf35EWNpAqiip6Z2wUH7ES3o3/hKfW66'
    app = MyApp()
    app.run()




