import time

import openrouteservice
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage, Image
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivymd.uix.button import MDFillRoundFlatButton

from models.map import Map
from models.order import Order, StatusEnum
import polyline
from kivy.graphics import Line

from services.map import MapBuilder


class OneOrderScreen(Screen):
    path_to_kv_file = './styles/style_for_one_order.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(OneOrderScreen, self).__init__(**kwargs)
        self.map_builder = MapBuilder()
        self.load_kv()
        self.cancel_button = None
        self.map_button = None
        self.finish_button = None
        self.accept_button = None

    def load_order_data(self, db_session, order_id):
        order = Order.get_order_by_id(db_session, order_id)
        status = order.status if order else None

        self.ids.order_number_label.text = str(order.order_number)
        self.ids.address_label.text = str(order.address)
        self.ids.total_amount_label.text = str(order.total_amount)
        self.ids.name_client_label.text = 'Kate'
        self.ids.phone_number_client_label.text = '89518579473'

        if status == StatusEnum.COMPLETED:
            self.ids.completed.text = 'Заказ Завершён'

        if status == StatusEnum.CANCELED:
            self.ids.canceled.text = 'Заказ Отменён'


        elif status == StatusEnum.NOT_ACCEPTED:
            self.accept_button = MDFillRoundFlatButton(text='Принять', size_hint=(None, None), height='36dp',
                                                       md_bg_color=(1, 0.478, 0, 1),
                                                       pos_hint={'center_x': 0.5, 'top': 0.2})
            self.accept_button.bind(
                on_release=lambda instance: self.accept_order(db_session, order_id, self.accept_button))
            self.add_widget(self.accept_button)

        elif status == StatusEnum.ACCEPTED:
            self.show_additional_buttons(db_session, order_id)

    def accept_order(self, db_session, order_id, accept_button):
        Order.change_status(db_session, order_id, StatusEnum.ACCEPTED)
        self.remove_widget(accept_button)
        self.show_additional_buttons(db_session, order_id)

    def show_additional_buttons(self, db_session, order_id):
        order = Order.get_order_by_id(db_session, order_id)
        print(order.status, 'dddd22')
        if order.status == StatusEnum.ACCEPTED:
            self.map_button = MDFillRoundFlatButton(text='Карта', size_hint=(None, None),
                                                    font_name='styles/Montserrat-ExtraBold.ttf', font_size='12sp',
                                                    md_bg_color=(1, 0.478, 0, 1),
                                                    pos_hint={'center_x': 0.7, 'top': 0.25})
            self.map_button.bind(on_release=lambda instance: self.show_map(db_session, order_id))

            self.finish_button = MDFillRoundFlatButton(text='Завершить', size_hint=(None, None),
                                                       font_name='styles/Montserrat-ExtraBold.ttf', font_size='12sp',
                                                       md_bg_color=(1, 0.478, 0, 1),
                                                       pos_hint={'center_x': 0.5, 'top': 0.15})
            self.finish_button.bind(on_release=lambda instance: self.finish_order(db_session, order_id))

            self.cancel_button = MDFillRoundFlatButton(text='Отменить', size_hint=(None, None),
                                                       font_name='styles/Montserrat-ExtraBold.ttf', font_size='12sp',
                                                       md_bg_color=(1, 0.478, 0, 2),
                                                       pos_hint={'center_x': 0.3, 'top': 0.25})
            self.cancel_button.bind(on_release=lambda instance: self.cancel_order(db_session, order_id))

            self.add_widget(self.cancel_button)
            self.add_widget(self.map_button)
            self.add_widget(self.finish_button)

    def cancel_order(self, db_session, order_id):

        confirmation_popup = Popup(
            title='     Подтверждение отмены заказа',
            content=Label(text='Вы уверены, что хотите отменить заказ?'),
            size_hint=(None, None),
            size=(350, 180),
            separator_color=[1, 0.478, 0, 1],
            background_color=[4, .4, .2, 1]
        )

        confirm_button = MDFillRoundFlatButton(text='Да', font_name='styles/Montserrat-ExtraBold.ttf',
                                               md_bg_color=(1, 0.478, 0, 1), size_hint_x=None)
        confirm_button.bind(
            on_release=lambda instance: self.confirm_cancel_order(db_session, order_id, confirmation_popup))

        cancel_button = MDFillRoundFlatButton(text='Нет', font_name='styles/Montserrat-ExtraBold.ttf',
                                              md_bg_color=(1, 0.478, 0, 1))
        cancel_button.bind(on_release=confirmation_popup.dismiss)
        confirmation_popup.content = BoxLayout(orientation='horizontal',
                                               padding=25, spacing=90)
        confirmation_popup.content.add_widget(confirm_button)
        confirmation_popup.content.add_widget(cancel_button)

        confirmation_popup.open()

    def confirm_cancel_order(self, db_session, order_id, popup):
        popup.dismiss()
        Order.change_status(db_session, order_id, StatusEnum.CANCELED)
        self.remove_buttons()
        self.ids.canceled.text = 'Заказ Отменён'

    def show_map(self, db_session, order_id):
        coord = Map.get_coord_by_id(db_session, order_id)

        route_coordinates = [(39.20563, 51.65714), (39.20572, 51.65716), (39.20576, 51.65719),
                             (39.20535, 51.65733),
                             (39.20532, 51.65736), (39.20527, 51.65747), (39.20514, 51.6576), (39.20503, 51.6577),
                             (39.20445, 51.65818), (39.20377, 51.65874), (39.20321, 51.6592), (39.20253, 51.65977),
                             (39.20151, 51.66062), (39.20029, 51.66161), (39.19967, 51.6621), (39.19918, 51.6625),
                             (39.19719, 51.66413), (39.1957, 51.66536), (39.19555, 51.6653), (39.19481, 51.66501),
                             (39.19439, 51.66485), (39.19403, 51.66469), (39.19317, 51.66434), (39.19201, 51.6653),
                             (39.19039, 51.66575), (39.19024, 51.6658), (39.19033, 51.66593), (39.19098, 51.66683),
                             (39.19209, 51.66652)]

        map_popup = self.map_builder.create_map_popup()
        map_view = self.map_builder.create_map_with_route(coord.start_longitude, coord.start_latitude,
                                                          coord.end_longitude, coord.end_latitude)
        map_popup.content = map_view

        map_popup.open()

        index = 0

        def update_map_content(dt):
            nonlocal index
            if index < len(route_coordinates):
                self.map_builder.update_route(map_view, route_coordinates, index)
                index += 1
            else:
                Clock.unschedule(update_map_content)

        Clock.schedule_interval(update_map_content, 2)

    def finish_order(self, db_session, order_id):
        Order.change_status(db_session, order_id, StatusEnum.COMPLETED)
        self.remove_buttons()
        self.ids.completed.text = 'Заказ Завершён'

    def remove_buttons(self):
        if self.accept_button:
            self.remove_widget(self.accept_button)
            self.accept_button = None
        if self.cancel_button:
            self.remove_widget(self.cancel_button)
            self.cancel_button = None
        if self.map_button:
            self.remove_widget(self.map_button)
            self.map_button = None
        if self.finish_button:
            self.remove_widget(self.finish_button)
            self.finish_button = None
        self.ids.completed.text = ''
        self.ids.canceled.text = ''

    def on_pre_leave(self, *args):
        self.remove_buttons()

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())
