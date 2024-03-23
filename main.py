from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
import re
from kivy.lang import Builder
from kivy.core.window import Window

from login_screen import LoginScreen
from profile_screen import ProfileScreen


class MyApp(MDApp):
    def build(self):
        #self.theme_cls.theme_style = "Light"
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(ProfileScreen(name="profile_screen"))
        #return Builder.load_file("styles/style_for_main.kv")
        return sm

    def switch_to_login_screen(self):
        self.root.current = "login_screen"


if __name__ == "__main__":
    app = MyApp()
    app.run()