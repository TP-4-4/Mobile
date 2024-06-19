from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage

from bd.database import SessionLocal
from models.courier import Courier  # Добавим импорт модели courier

class ProfileScreen(Screen):
    path_to_kv_file = './styles/style_for_profile.kv'
    image = CoreImage('img/logo.png')
    width = image.width
    height = image.height

    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        self.load_kv()

    # def on_pre_enter(self, *args):
    #     self.load_profile_data(App.get_running_app().db_session)

    def load_profile_data(self, db_session, courier_id):
        #courier_id = 1
        courier = Courier.get_courier_info_by_id(db_session, courier_id)  # Вот здесь вызывается метод из модели courier

        self.ids.last_name_label.text = str(courier.last_name)
        self.ids.first_name_label.text = str(courier.first_name)
        self.ids.middle_name_label.text = str(courier.middle_name)
       # self.ids.birth_date_label.text = str(courier.birth_date)
        self.ids.phone_number_label.text = str(courier.phone_number)

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())
