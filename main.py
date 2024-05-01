import bcrypt
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

from bd.database import SessionLocal
from models.order import Order
from screens.login_screen import LoginScreen
from screens.one_order_screen import OneOrderScreen
from screens.profile_screen import ProfileScreen
from screens.orders_screen import OrdersScreen



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
        # Создание объекта сессии и передача его в приложение
        self.db_session = SessionLocal()

    def build(self):
        self.root = WindowManager()  # Set WindowManager as the root
        Window.size = (1080 / 3, 2000 / 3)
        # Window.fullscreen = 'auto'
        self.root.add_widget(OrdersScreen(name='orders_screen'))
        self.root.add_widget(OneOrderScreen(name='one_order_screen'))
        self.root.add_widget(LoginScreen(name='login_screen'))
        self.root.add_widget(ProfileScreen(name='profile_screen'))

        return Builder.load_file('styles/style_for_main.kv')

    # def change_order_status(self, order_id: int, new_status: str):
    #     Order.change_status(self.db_session, order_id, new_status)

    def submit_login_data(self, phone_number, password):
        login_screen = self.root.get_screen('login_screen')
        if login_screen:
            login_screen.submit_data(self.db_session, phone_number, password)




def encrypt_password(password):
    # Генерация соли
    salt = bcrypt.gensalt()
    # Хэширование пароля с использованием соли
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


if __name__ == '__main__':
    password = '1'
    encrypted_password = encrypt_password(password)
    print("Зашифрованный пароль:", encrypted_password)
    #  Зашифрованный пароль: b'$2b$12$6pVGF6spEu7C5JSOC56Bguf35EWNpAqiip6Z2wUH7ES3o3/hKfW66'
    app = MyApp()
    app.run()


