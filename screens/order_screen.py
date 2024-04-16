from kivy.animation import Animation
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton

from models.order import Order


class OrderScreen(Screen):
    path_to_kv_file = './styles/style_for_order.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.load_kv()

    def load_order_data(self, db_session, user_id):
        orders = Order.get_orders_by_user_id(db_session, user_id)
        order_layout = self.ids.order_layout
        order_layout.clear_widgets()

        for index, order in enumerate(orders):
            order_number_label = Label(text=str(order.order_number), font_size='20sp', text_size=(100, None), font_name='styles/Montserrat-ExtraBold.ttf',
                                       color=(1, 0.478, 0, 1))
            total_amount_label = Label(text=str(order.address), font_size='13sp', text_size=(100, None), font_name='styles/Montserrat-SemiBold.ttf',
                                       color=(0, 0, 0, 0.6))
            address_label = Label(text=str(order.total_amount), font_size='13sp', text_size=(100, None), font_name='styles/Montserrat-Bold.ttf',
                                  color=(0, 0, 0, 1))

            order_layout.add_widget(order_number_label)
            order_layout.add_widget(total_amount_label)
            order_layout.add_widget(address_label)

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

