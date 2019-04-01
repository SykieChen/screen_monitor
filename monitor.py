#!/usr/local/bin/python3
from PIL import ImageGrab
import json
import requests
import time


class Monitor(object):
    def load(self, config_file):
        config = json.load(config_file)
        self.area = tuple(config["area"])
        self.time_out = config["time_out"]
        self.call_back = "https://api.telegram.org/bot%s/sendMessage" % config["telegram"]["bot_token"]
        self.chat_id = config["telegram"]["chat_id"]
        self.net_retry = config["telegram"]["retry"]
        self.debug = config["debug"]
        if "proxy" in config:
            self.proxy = config["proxy"]
        else:
            self.proxy = None
        self.log("Started.")

    def log(self, text):
        print("[%s] %s" %
              (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), text))

    def push(self):
        payload = {
            "text": "*大変だ！*画面が固まったっぽい！",
            "chat_id": self.chat_id,
            "parse_mode": "Markdown"
        }
        _retry = self.net_retry
        while _retry > 0:
            try:
                self.log("Sending notification...")
                # requests.post(self.call_back, data=payload, timeout=10, proxies=self.proxy)
                _retry = -1
            except:
                self.log("Network error, retry.")
                _retry -= 1
        if 0 == _retry:
            self.log("Could not connect to server, check if fucked by GFW.")
            return False
        else:
            self.log("Message sent!")
            return True

    def start(self):
        _img_old = ImageGrab.grab(bbox=self.area)
        while 1:
            time.sleep(self.time_out)
            _img_new = ImageGrab.grab(bbox=self.area)
            if _img_new == _img_old:
                self.log("Screen stuck!")
                self.push()
                while (input("Deal with the stuck, then type OK to resume...").upper() != "OK"):
                    pass
                self.log("Monitor resumed.")
            else:
                self.log("Screen moving, OK.")
            _img_old = _img_new.copy()
            if self.debug: _img_old.save("screenshot.bmp")
            


if __name__ == "__main__":
    monitor = Monitor()
    with open("config.json", "r") as config:
        monitor.load(config)
    monitor.start()
