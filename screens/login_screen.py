from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import re

from sqlalchemy.orm import Session

from services.auth import authenticate_user


def validate_phone_number(phone_number):
    pattern = re.compile(r'^(?:\+7|8)\d{10}$')

    if pattern.match(phone_number):
        return True
    else:
        return False


class LoginScreen(Screen):
    path_to_kv_file = './styles/style_for_login.kv'

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.load_kv()

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

    def submit_data(self, db_session, phone_number, password):
        # Передача объекта сессии напрямую в функцию аутентификации
        user = authenticate_user(db_session, phone_number, password)
        if user:
            print('Authentication successful!')
            self.manager.current = 'orders_screen'  # Переход на экран заказа
            self.ids.phone_number_field.text = ''
            self.ids.password_field.text = ''
            self.ids.error_label.text = ''
            user_id = user.id
            print("User ID:", user_id)

            profile_screen = self.manager.get_screen('profile_screen')
            if profile_screen:
                profile_screen.load_profile_data(db_session, user_id)

            orders_screen = self.manager.get_screen('orders_screen')
            if orders_screen:
                orders_screen.load_orders_data(db_session, user_id)

        else:
            if self.ids.phone_number_field.text != '' or self.ids.password_field.text != '':
                self.ids.error_label.text = "Неверный номер телефона или пароль"
                print('Authentication failed. Invalid credentials.')

