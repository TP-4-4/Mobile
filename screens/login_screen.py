from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import re

from models.order import Order
from services.auth import authenticate_courier
from services.map import MapBuilder


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
        self.map_builder = MapBuilder()
        self.load_kv()

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

    def submit_data(self, db_session, phone_number, password, map_builder):
        self.map_builder = map_builder
        courier = authenticate_courier(db_session, phone_number, password)
        if courier:
            print('Authentication successful!')
            self.manager.current = 'orders_screen'  # Переход на экран заказа
            self.ids.phone_number_field.text = ''
            self.ids.password_field.text = ''
            self.ids.error_label.text = ''
            courier_id = courier.id
            print("courier ID:", courier_id)

            accepted_orders_count = Order.count_accepted_orders(db_session)
            if accepted_orders_count > 0:
                if not self.map_builder.gps_started:
                    self.map_builder.start_gps(courier_id)
                if not self.map_builder.gps_check_started:
                    self.map_builder.start_gps_status_check(courier_id)
                    self.map_builder.start_gps(courier_id)

            else:
                self.map_builder.stop_gps()
                # проверить включён ли gps

            profile_screen = self.manager.get_screen('profile_screen')
            if profile_screen:
                profile_screen.load_profile_data(db_session, courier_id)

            orders_screen = self.manager.get_screen('orders_screen')
            if orders_screen:
                orders_screen.load_orders_data(db_session, courier_id, self.map_builder)

        else:
            if self.ids.phone_number_field.text != '' or self.ids.password_field.text != '':
                self.ids.error_label.text = "Неверный номер телефона или пароль"
                print('Authentication failed. Invalid credentials.')

