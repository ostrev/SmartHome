from tkinter import *
from main_view import GUI
from models import DB
from tplink import DeviceControllerPlug, DeviceControllerLed
import json


class SmartHomeApp:
    def __init__(self, db):
        try:
            self.device_controller_p115 = DeviceControllerPlug(plug_device_ip, username, password)
            self.device_controller_l530 = DeviceControllerLed(led_device_ip, username, password)
        except Exception as e:
            print(f"Connection error!: {e}")

        self.db = db
        self.rooms = []
        self.devices = []

        try:
            self.update_live_parameters()
        except Exception as e:
            print(f"Connection error!: {e}")

    def add_room(self, name):
        if name:
            self.db.add_room(name)
            self.load_rooms_data()

    def edit_room(self, name, id):
        if name:
            self.db.edit_room(name, id)
            self.load_rooms_data()

    def add_device(self, name, room_id, type_device):
        if name and room_id:
            self.db.add_device(name, room_id, type_device)
            self.load_devices_data()

    def edit_device(self, id, name, dev_type, room):
        if name and dev_type and room:
            self.db.edit_device(id, name, dev_type, room)
            self.load_devices_data()

    def delete_device(self, dev_id):
        self.db.delete_device(dev_id)
        self.load_devices_data()

    def delete_room(self, room_id):
        self.db.delete_room(room_id)
        self.load_rooms_data()

    def load_rooms_data(self):
        self.rooms = self.db.get_items('rooms')

    def load_devices_data(self):

        devices_list = self.db.get_devices()
        self.devices.clear()
        for device in devices_list:
            id_dev = device[0]
            type_dev = device[3]
            device_data = self.db.get_full_data_for_device(id_dev, type_dev)
            temp1 = (id_dev, device[1], type_dev, device[2])
            temp2 = device_data[4:]
            result = temp1 + temp2
            # print(device_data)
            self.devices.append(result)

    def change_parameter_cct(self, dev_id, value):
        if dev_id == '1':  # hardcode that the device is my real device
            self.device_controller_l530.change_cct(value)
            cct = self.device_controller_l530.get_device_params_l530()[1]
            if cct == value:
                self.db.update_cct(dev_id, value)
        else:
            self.db.update_cct(dev_id, value)
        self.load_devices_data()

    def change_parameter_status(self, dev_id, value):
        if dev_id == '1':  # hardcode that the device is my real device
            self.device_controller_l530.change_status(value)
            status = self.device_controller_l530.get_device_params_l530()[4]
            if status:
                temp = 'ON'
            else:
                temp = 'OFF'
            if temp == value:
                self.db.update_status(dev_id, value)
        else:
            self.db.update_status(dev_id, value)
        self.load_devices_data()

    def change_parameter_intensity(self, dev_id, value):
        if dev_id == '1':  # hardcode that the device is my real device
            self.device_controller_l530.change_intensity(value)
            intensity = self.device_controller_l530.get_device_params_l530()[0]
            if intensity == value:
                self.db.update_intensity(dev_id, value)
        else:
            self.db.update_intensity(dev_id, value)
        self.load_devices_data()

    def change_parameter_rgb(self, dev_id, value, colour):
        if dev_id == '1':  # hardcode that the device is my real device
            self.device_controller_l530.change_rgb(value)
            hue = self.device_controller_l530.get_device_params_l530()[2]
            saturation = self.device_controller_l530.get_device_params_l530()[3]
            temp_tup = (hue, saturation)
            if temp_tup == value:
                self.db.update_rgb(dev_id, colour)
        else:
            self.db.update_rgb(dev_id, colour)
        self.load_devices_data()

    def change_plug_status(self, dev_id, value):
        if dev_id == '2':  # hardcode that the device is my real device
            self.device_controller_p115.change_plug_status(value)
            status = self.device_controller_p115.get_device_params_p115()[0]
            if status:
                temp = 'ON'
            else:
                temp = 'OFF'
            if temp == value:
                self.db.update_plug_status(dev_id, value)
        else:
            self.db.update_plug_status(dev_id, value)
        self.load_devices_data()

    def update_live_parameters(self):
        status, power, on_time, month_energy, today_energy = self.device_controller_p115.get_device_params_p115()
        self.db.update_plug_parameters(power, on_time, today_energy)

    def __del__(self):
        self.db.connection.close()


if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    led_device_ip = config['led_device_ip']
    plug_device_ip = config['plug_device_ip']
    username = config['username']
    password = config['password']

    root = Tk()
    db = DB()
    controller = SmartHomeApp(db)
    gui = GUI(root, controller)
    gui.run()
