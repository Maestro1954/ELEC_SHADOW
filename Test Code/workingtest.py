from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: "vertical"
        size_hint: .2, .2
        spacing: "5dp"
       
        Button:
            text: "Video"
            on_press: root.on_button_click()
        Button:
            text: "Overlay"
            on_press: root.on_button_click()
        Button:
            text: "Zoom"
            on_press: root.on_button_click()
        Button:
            text: "Export"
            on_press: root.on_button_click()
    
        Button:
        
            text: 'Live feed and capture'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
    
        Button:
            text: 'My settings button'
        Button:
         #orientation: "vertical"
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

if __name__ == '__main__':
    TestApp().run()
