from kivy.animation import Animation
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from models.order import Order


class OrderScreen(Screen):
    path_to_kv_file = './styles/style_for_order.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.load_kv()

    def on_pre_enter(self, *args):
        self.load_order_data(App.get_running_app().db_session)

    def load_order_data(self, db_session):
        user_id = 1
        orders = Order.get_orders_by_user_id(db_session, user_id)  # Вот здесь вызывается метод из модели User
        print(orders)
        print(orders[0].order_number, orders[0].address, orders[0].total_amount)

    def show_map(self):
        map_image = self.ids.map_image
        if map_image.opacity == 0:
            Animation(opacity=1, duration=0).start(map_image)
        else:
            Animation(opacity=0, duration=0).start(map_image)

    def switch_buttons(self):
        accept_button = self.ids.accept_button
        cancel_button = self.ids.cancel_button
        map_button = self.ids.map_button
        complete_button = self.ids.complete_button
        map_image = self.ids.map_image

        if accept_button.opacity == 1:
            Animation(opacity=0, duration=0).start(accept_button)
            Animation(opacity=1, duration=0).start(cancel_button)
            Animation(opacity=1, duration=0).start(map_button)
            Animation(opacity=1, duration=0).start(complete_button)
        else:
            Animation(opacity=0, duration=0).start(cancel_button)
            Animation(opacity=1, duration=0).start(accept_button)
            Animation(opacity=0, duration=0).start(map_button)
            Animation(opacity=0, duration=0).start(complete_button)
            if map_image.opacity == 1:
                Animation(opacity=0, duration=0).start(map_image)

    def complete_order(self):
        completed_label = self.ids.completed_label
        accept_button = self.ids.accept_button
        cancel_button = self.ids.cancel_button
        map_button = self.ids.map_button
        complete_button = self.ids.complete_button
        map_image = self.ids.map_image
        if completed_label.opacity == 0:
            Animation(opacity=0, duration=0).start(accept_button)
            Animation(opacity=1, duration=0).start(completed_label)
            Animation(opacity=0, duration=0).start(map_button)
            Animation(opacity=0, duration=0).start(map_image)
            Animation(opacity=0, duration=0).start(cancel_button)
            Animation(opacity=0, duration=0).start(complete_button)

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

