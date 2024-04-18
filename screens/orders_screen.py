from kivy.animation import Animation
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton

from models.order import Order


class OrdersScreen(Screen):
    path_to_kv_file = './styles/style_for_orders.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(OrdersScreen, self).__init__(**kwargs)
        self.load_kv()

    def load_orders_data(self, db_session, user_id):
        orders = Order.get_orders_by_user_id(db_session, user_id)
        orders_layout = self.ids.orders_layout
        orders_layout.clear_widgets()

        for index, order in enumerate(orders):
            order_number_label = Label(text=str(order.order_number), font_size='20sp', text_size=(150, None), font_name='styles/Montserrat-ExtraBold.ttf',
                                       color=(1, 0.478, 0, 1))
            # total_amount_label = Label(text=str(order.total_amount), font_size='13sp', text_size=(150, None), font_name='styles/Montserrat-SemiBold.ttf',
            #                            color=(0, 0, 0, 0.6))
            address_label = Label(text=str(order.address), font_size='13sp', text_size=(150, None), font_name='styles/Montserrat-Bold.ttf',
                                  color=(0, 0, 0, 0.6))

            move_button = MDIconButton(
                icon='img/next.png',  # Путь к вашей иконке
                on_release=lambda btn, order_id=order.id: self.move_order(db_session, order_id)
            )

            orders_layout.add_widget(order_number_label)
            #orders_layout.add_widget(total_amount_label)
            orders_layout.add_widget(address_label)
            orders_layout.add_widget(move_button)

    def move_order(self, db_session, order_id):
        self.manager.current = 'one_order_screen'
        one_order_screen = self.manager.get_screen('one_order_screen')
        if one_order_screen:
            one_order_screen.load_order_data(db_session, order_id)

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

