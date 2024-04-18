from kivy.animation import Animation
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton

from models.order import Order, StatusEnum


class OneOrderScreen(Screen):
    path_to_kv_file = './styles/style_for_one_order.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(OneOrderScreen, self).__init__(**kwargs)
        self.load_kv()
        self.cancel_button = None
        self.map_button = None
        self.finish_button = None
        self.accept_button = None

    def on_pre_leave(self, *args):
        self.remove_additional_buttons()


    def load_order_data(self, db_session, order_id):
        order = Order.get_order_by_id(db_session, order_id)
        status = order.status if order else None


        self.ids.order_number_label.text = str(order.order_number)
        self.ids.address_label.text = str(order.address)
        self.ids.total_amount_label.text = str(order.total_amount)
        self.ids.name_client_label.text = 'Kate'
        self.ids.phone_number_client_label.text = '89518579473'

        back_button = MDIconButton(
            icon='img/back.png',
            on_release=lambda btn, order_id=order.id: self.back_order(),
            pos_hint={'left': 0.7, 'top': 0.8}
        )
        self.add_widget(back_button)

        if status == StatusEnum.NOT_ACCEPTED:
            self.accept_button = MDFillRoundFlatButton(text='Принять', size_hint=(None, None), height='36dp',
                                                md_bg_color=(1, 0.478, 0, 1), pos_hint={'center_x': 0.3, 'top': 0.6})
            self.accept_button.bind(on_release=lambda instance: self.accept_order(db_session, order_id, self.accept_button))
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
            self.map_button = MDFillRoundFlatButton(text='Карта', size_hint=(None, None), height='36dp',
                                                  md_bg_color=(1, 0.478, 0, 1), pos_hint={'center_x': 0.7, 'top': 0.6})
            self.map_button.bind(on_release=lambda instance: self.show_map())

            self.finish_button = MDFillRoundFlatButton(text='Завершить', size_hint=(None, None), height='36dp',
                                                  md_bg_color=(1, 0.478, 0, 1), pos_hint={'center_x': 0.5, 'top': 0.5})
            self.finish_button.bind(on_release=lambda instance: Order.change_status(db_session, order_id, StatusEnum.COMPLETED))

            self.cancel_button = MDFillRoundFlatButton(text='Отменить', size_hint=(None, None), height='36dp',
                                                  md_bg_color=(1, 0.478, 0, 1), pos_hint={'center_x': 0.1, 'top': 0.5})
            self.cancel_button.bind(on_release=lambda instance: Order.change_status(db_session, order_id, StatusEnum.CANCELED))

            self.add_widget(self.cancel_button)
            self.add_widget(self.map_button)
            self.add_widget(self.finish_button)

    def remove_additional_buttons(self):
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

    def show_map(self):
        map_image = self.ids.map_image
        if map_image.opacity == 0:
            Animation(opacity=1, duration=0).start(map_image)
        else:
            Animation(opacity=0, duration=0).start(map_image)

    def back_order(self):
        self.manager.current = 'orders_screen'


    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())


