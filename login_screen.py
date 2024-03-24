from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import re


def validate_phone_number(phone_number):
    pattern = re.compile(r'^(?:\+7|8)\d{10}$')

    if pattern.match(phone_number):
        return True
    else:
        return False


class LoginScreen(Screen):
    path_to_kv_file = 'styles/style_for_login.kv'

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.load_kv()

    def load_kv(self):
        with open(self.path_to_kv_file, 'r', encoding='utf-8') as kv_file:
            Builder.load_string(kv_file.read())

    def submit_data(self, phone_number, password):
        # if validate_phone_number(phone_number):
        print('Submitted data:')
        print('Phone number:', phone_number)
        print('Password:', password)
        # else:
        #    print('Invalid phone number. Please enter a valid Russian mobile phone number.')
