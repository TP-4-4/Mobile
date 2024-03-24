from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
import re

def validate_phone_number(phone_number):
    # Паттерн для проверки на корректность российского мобильного номера
    pattern = re.compile(r'^(?:\+7|8)\d{10}$')

    # Проверка соответствия введенного номера паттерну
    if pattern.match(phone_number):
        return True
    else:
        return False

class LoginScreen(Screen):
    path_to_kv_file = "styles/style_for_login.kv"

    def on_enter(self):
        # Window.fullscreen = 'auto'
        Window.size = (1080 / 3, 2000 / 3)
        self.load_kv()

    def load_kv(self):
        with open(self.path_to_kv_file, "r", encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

    def submit_data(self, phone_number, password):
        #if validate_phone_number(phone_number):
        print("Submitted data:")
        print("Phone number:", phone_number)
        print("Password:", password)
        # Вставьте здесь код для обработки введенных данных
        #else:
        #    print("Invalid phone number. Please enter a valid Russian mobile phone number.")
