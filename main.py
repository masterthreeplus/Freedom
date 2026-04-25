from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import threading
import requests
import time

class PremiumPassApp(App):
    def build(self):
        self.stop_event = threading.Event()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.status_label = Label(text="[Status: Ready]", font_size='22sp', size_hint_y=0.1)
        layout.add_widget(self.status_label)
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.log_label = Label(text="Welcome to Premium Pass...", size_hint_y=None, halign='left', valign='top', text_size=(400, None))
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        self.scroll_view.add_widget(self.log_label)
        layout.add_widget(self.scroll_view)
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.2)
        self.start_btn = Button(text="START BYPASS", background_color=(0, 0.8, 0, 1))
        self.start_btn.bind(on_press=self.start_engine)
        self.stop_btn = Button(text="STOP", background_color=(0.8, 0, 0, 1), disabled=True)
        self.stop_btn.bind(on_press=self.stop_engine)
        btn_layout.add_widget(self.start_btn)
        btn_layout.add_widget(self.stop_btn)
        layout.add_widget(btn_layout)
        return layout

    def update_log(self, msg):
        Clock.schedule_once(lambda dt: self._append_text(msg))

    def _append_text(self, msg):
        self.log_label.text += f"\n{msg}"
        self.scroll_view.scroll_y = 0

    def start_engine(self, instance):
        self.stop_event.clear()
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.status_label.text = "[Status: Running...]"
        self.update_log("[*] Initializing Turbo Engine...")
        threading.Thread(target=self.bypass_logic, daemon=True).start()

    def stop_engine(self, instance):
        self.stop_event.set()
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = "[Status: Stopped]"
        self.update_log("[!] Engine Shutdown.")

    def bypass_logic(self):
        while not self.stop_event.is_set():
            try:
                self.update_log("[*] Checking connection...")
                # ဤနေရာတွင် bypass လုပ်မည့် logic ထည့်နိုင်သည်
                time.sleep(5)
            except Exception as e:
                self.update_log(f"[X] Error: {e}")
                break

if __name__ == "__main__":
    PremiumPassApp().run()

