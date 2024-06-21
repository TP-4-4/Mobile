from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage, Image
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFillRoundFlatButton

from models.map import Map
from models.order import Order, StatusEnum
from models.user import User

from kivy.graphics import RoundedRectangle

from services.map import MapBuilder


class CustomButton(MDFillRoundFlatButton):
    background = ObjectProperty()

    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        with self.canvas.before:
            self.background = RoundedRectangle(pos=self.pos, size=self.size)

    def on_size(self, instance, value):
        self.background.size = value

    def on_pos(self, instance, value):
        self.background.pos = value


class OneOrderScreen(Screen):
    path_to_kv_file = './styles/style_for_one_order.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(OneOrderScreen, self).__init__(**kwargs)
        self.back_button = None
        self.map_builder = MapBuilder()
        self.load_kv()
        self.cancel_button = None
        self.map_button = None
        self.finish_button = None
        self.accept_button = None
        self.map_shown = False

    def load_order_data(self, db_session, order_id, map_builder):

        order = Order.get_order_by_id(db_session, order_id)
        status = order.status if order else None

        user = User.get_user_info_by_id(db_session, order.user_id)

        self.map_builder = map_builder
        self.ids.order_number_label.text = 'ORD' + str(order_id)
        self.ids.address_label.text = str(user.address)
        self.ids.total_amount_label.text = str(order.total_cost)
        self.ids.name_client_label.text = user.first_name + ' ' + user.last_name
        self.ids.phone_number_client_label.text = user.email

        self.back_button = MDFillRoundFlatButton(text='Назад', size_hint=(None, None),
                                                 font_name='styles/Montserrat-ExtraBold.ttf', font_size='12sp',
                                                 md_bg_color=(1, 0.478, 0, 1),
                                                 pos_hint={'right': 0.95, 'top': 0.97}, )
        self.back_button.bind(on_release=lambda instance: self.switch_to_orders_screen(db_session, order.courier_id))
        self.add_widget(self.back_button)

        if status == StatusEnum.COMPLETED:
            self.ids.completed.text = 'Заказ Завершён'

        if status == StatusEnum.CANCELED:
            self.ids.canceled.text = 'Заказ Отменён'


        elif status == StatusEnum.NOT_ACCEPTED:
            self.accept_button = MDFillRoundFlatButton(text='Принять', size_hint=(None, None),
                                                       font_name='styles/Montserrat-ExtraBold.ttf', font_size='12sp',
                                                       md_bg_color=(1, 0.478, 0, 1),
                                                       pos_hint={'center_x': 0.5, 'top': 0.2})
            self.accept_button.bind(
                on_release=lambda instance: self.accept_order(db_session, order_id, self.accept_button,
                                                              order.courier_id))
            self.add_widget(self.accept_button)

        elif status == StatusEnum.ACCEPTED:
            self.show_additional_buttons(db_session, order_id)

    def switch_to_orders_screen(self, db_session, courier_id):
        orders_screen = self.manager.get_screen('orders_screen')
        if orders_screen:
            self.manager.current = 'orders_screen'
            orders_screen.load_orders_data(db_session, courier_id, self.map_builder)

    def accept_order(self, db_session, order_id, accept_button, courier_id):
        Order.change_status(db_session, order_id, StatusEnum.ACCEPTED)

        accepted_orders_count = Order.count_accepted_orders(db_session)
        if accepted_orders_count > 0:
            if not self.map_builder.gps_started:
                self.map_builder.start_gps(courier_id)
            if not self.map_builder.gps_check_started:
                self.map_builder.start_gps_status_check(courier_id)
        else:
            self.map_builder.stop_gps()

        self.remove_widget(accept_button)
        self.show_additional_buttons(db_session, order_id)

    def show_additional_buttons(self, db_session, order_id):
        order = Order.get_order_by_id(db_session, order_id)
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
            self.finish_button.bind(
                on_release=lambda instance: self.finish_order(db_session, order_id, order.courier_id))

            self.cancel_button = MDFillRoundFlatButton(text='Отменить', size_hint=(None, None),
                                                       font_name='styles/Montserrat-ExtraBold.ttf', font_size='12sp',
                                                       md_bg_color=(1, 0.478, 0, 2),
                                                       pos_hint={'center_x': 0.3, 'top': 0.25})
            self.cancel_button.bind(
                on_release=lambda instance: self.cancel_order(db_session, order_id, order.courier_id))

            self.add_widget(self.cancel_button)
            self.add_widget(self.map_button)
            self.add_widget(self.finish_button)

    def cancel_order(self, db_session, order_id, courier_id):
        window_width, window_height = Window.size

        popup_width = window_width * 0.75
        popup_height = window_height * 0.2

        confirmation_popup = Popup(
            title='Подтверждение отмены заказа',
            title_font='styles/Montserrat-ExtraBold.ttf',
            title_align='center',
            size_hint=(None, None),
            size=(popup_width, popup_height),
            separator_color=[1, 1, 1, 1],
            background_color=[255, 255, 255, 1],
            title_color=[1, 0.478, 0, 1],
            overlay_color=[1, 0.478, 0, 0.41],
        )

        confirm_button = MDFillRoundFlatButton(text='Да', font_name='styles/Montserrat-ExtraBold.ttf',
                                               md_bg_color=(1, 0.478, 0, 1), size_hint_x=None)
        confirm_button.bind(
            on_release=lambda instance: self.confirm_cancel_order(db_session, order_id, confirmation_popup, courier_id))

        cancel_button = MDFillRoundFlatButton(text='Нет', font_name='styles/Montserrat-ExtraBold.ttf',
                                              md_bg_color=(1, 0.478, 0, 1))
        cancel_button.bind(on_release=confirmation_popup.dismiss)

        confirm_layout = AnchorLayout(anchor_x='left', anchor_y='center')
        confirm_layout.add_widget(confirm_button)

        cancel_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        cancel_layout.add_widget(cancel_button)

        buttons_layout = GridLayout(cols=2, padding=popup_width / 10)
        buttons_layout.add_widget(confirm_layout)
        buttons_layout.add_widget(cancel_layout)

        confirmation_popup.content = buttons_layout

        confirmation_popup.open()

    def confirm_cancel_order(self, db_session, order_id, popup, courier_id):
        popup.dismiss()
        Order.change_status(db_session, order_id, StatusEnum.CANCELED)

        accepted_orders_count = Order.count_accepted_orders(db_session)
        if accepted_orders_count > 0:
            if not self.map_builder.gps_started:
                self.map_builder.start_gps(courier_id)
            if not self.map_builder.gps_check_started:
                self.map_builder.start_gps_status_check(courier_id)
        else:
            self.map_builder.stop_gps()

        self.remove_buttons()
        self.ids.canceled.text = 'Заказ Отменён'

    def show_map(self, db_session, order_id):
        coord = Map.get_coord_by_id(db_session, order_id)

        map_popup = self.map_builder.create_map_popup()
        map_view = self.map_builder.create_map_with_route(coord.start_longitude, coord.start_latitude,
                                                          coord.end_longitude, coord.end_latitude)
        center_lat = (coord.start_latitude + coord.end_latitude) / 2
        center_lon = (coord.start_longitude + coord.end_longitude) / 2
        map_view.center_on(center_lat, center_lon)
        map_popup.content = map_view

        update_event = Clock.schedule_interval(lambda dt: self.map_builder.update_route(map_view), 1)

        map_popup.bind(on_dismiss=lambda *args: Clock.unschedule(update_event))

        map_popup.open()

    def confirm_finish_order(self, db_session, order_id, popup, courier_id):
        popup.dismiss()
        Order.change_status(db_session, order_id, StatusEnum.COMPLETED)

        accepted_orders_count = Order.count_accepted_orders(db_session)
        if accepted_orders_count > 0:
            if not self.map_builder.gps_started:
                self.map_builder.start_gps(courier_id)
            if not self.map_builder.gps_check_started:
                self.map_builder.start_gps_status_check(courier_id)
        else:
            self.map_builder.stop_gps()

        self.remove_buttons()
        self.ids.completed.text = 'Заказ Завершён'

    def finish_order(self, db_session, order_id, courier_id):
        window_width, window_height = Window.size

        popup_width = window_width * 0.75
        popup_height = window_height * 0.2

        confirmation_popup = Popup(
            title='Подтверждение завершения заказа',
            title_font='styles/Montserrat-ExtraBold.ttf',
            title_align='center',
            size_hint=(None, None),
            size=(popup_width, popup_height),
            separator_color=[1, 1, 1, 1],
            background_color=[255, 255, 255, 1],
            title_color=[1, 0.478, 0, 1],
            overlay_color=[1, 0.478, 0, 0.41],
        )

        confirm_button = MDFillRoundFlatButton(text='Да', font_name='styles/Montserrat-ExtraBold.ttf',
                                               md_bg_color=(1, 0.478, 0, 1), size_hint_x=None)
        confirm_button.bind(
            on_release=lambda instance: self.confirm_finish_order(db_session, order_id, confirmation_popup, courier_id))

        cancel_button = MDFillRoundFlatButton(text='Нет', font_name='styles/Montserrat-ExtraBold.ttf',
                                              md_bg_color=(1, 0.478, 0, 1))
        cancel_button.bind(on_release=confirmation_popup.dismiss)

        confirm_layout = AnchorLayout(anchor_x='left', anchor_y='center')
        confirm_layout.add_widget(confirm_button)

        cancel_layout = AnchorLayout(anchor_x='right', anchor_y='center')
        cancel_layout.add_widget(cancel_button)

        buttons_layout = GridLayout(cols=2, padding=popup_width / 10)
        buttons_layout.add_widget(confirm_layout)
        buttons_layout.add_widget(cancel_layout)

        confirmation_popup.content = buttons_layout

        confirmation_popup.open()

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
