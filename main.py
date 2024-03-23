from kivymd.app import MDApp
import re
from kivy.lang import Builder
from kivy.core.window import Window


def validate_phone_number(phone_number):
    # Паттерн для проверки на корректность российского мобильного номера
    pattern = re.compile(r'^(?:\+7|8)\d{10}$')

    # Проверка соответствия введенного номера паттерну
    if pattern.match(phone_number):
        return True
    else:
        return False


kv = '''
#:import KivyLexer kivy.extras.highlight.KivyLexer
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer

BoxLayout:

    # CodeInput:
    #     lexer: KivyLexer()
    #     style_name: "native"
    #     on_text: app.update_kv_file(self.text)
    #     size_hint_x: .7
    
    HotReloadViewer:
        size_hint_x: .3
        path: app.path_to_kv_file
        errors: True
        errors_text_color: 1, 1, 0, 1
        errors_background_color: app.theme_cls.bg_dark

'''

class MyApp(MDApp):
    path_to_kv_file = "styles.kv"
    def build(self):
        #Window.fullscreen = 'auto'
        Window.size = (1080 / 3, 2000 / 3)
        return Builder.load_string(kv)

    def submit_data(self, phone_number, password):
        if validate_phone_number(phone_number):
            print("Submitted data:")
            print("Phone number:", phone_number)
            print("Password:", password)
            # Вставьте здесь код для обработки введенных данных
        else:
            print("Invalid phone number. Please enter a valid Russian mobile phone number.")

    def update_kv_file(self, text):
        with open(self.path_to_kv_file, "w") as kv_file:
            kv_file.write(text)


if __name__ == '__main__':
    app = MyApp()
    app.run()
