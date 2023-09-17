from PyP100 import PyL530
from PyP100 import PyP110


class DeviceControllerLed:
    def __init__(self, ip, username, password):
        self.l530 = PyL530.L530(ip, username, password)
        self.l530.handshake()
        self.l530.login()

    def get_device_params_l530(self):
        dev_state = self.l530.getDeviceInfo()["result"]['default_states']['state']
        state = self.l530.getDeviceInfo()["result"]['device_on']
        intensity = dev_state['brightness'] if 'brightness' in dev_state else None
        cct = dev_state['color_temp'] if 'color_temp' in dev_state else None
        hue = dev_state['hue'] if 'hue' in dev_state else None
        saturation = dev_state['saturation'] if 'saturation' in dev_state else None

        return intensity, cct, hue, saturation, state

    def change_cct(self, value):
        new_cct = int(value)
        self.l530.setColorTemp(new_cct)

    def change_status(self, value):
        if value == 'ON':
            self.l530.turnOn()
        else:
            self.l530.turnOff()

    def change_intensity(self, value):
        new_intensity = int(value)
        self.l530.setBrightness(new_intensity)

    def change_rgb(self, value):
        new_hue = int(value[0])
        new_saturation = int(value[1])
        self.l530.setColor(new_hue, new_saturation)


class DeviceControllerPlug:
    def __init__(self, ip, username, password):
        self.p115 = PyP110.P110(ip, username, password)
        self.p115.handshake()
        self.p115.login()

    def get_device_params_p115(self):
        status = self.p115.getDeviceInfo()['result']['device_on']
        on_time = self.p115.getDeviceInfo()['result']["on_time"]

        dev_state = self.p115.getEnergyUsage()['result']

        power = dev_state['current_power']
        month_energy = self.p115.getEnergyUsage()["result"]["month_energy"]
        today_energy = self.p115.getEnergyUsage()["result"]["today_energy"]

        return status, power, on_time, month_energy, today_energy

    def change_plug_status(self, value):
        if value == 'ON':
            self.p115.turnOn()
        else:
            self.p115.turnOff()
