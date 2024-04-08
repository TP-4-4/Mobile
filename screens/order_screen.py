from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class OrderScreen(Screen):
    path_to_kv_file = './styles/style_for_order.kv'

    def __init__(self, **kwargs):
        super(OrderScreen, self).__init__(**kwargs)
        self.load_kv()

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())
