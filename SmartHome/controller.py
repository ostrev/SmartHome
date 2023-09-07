import tkinter as tk
from random import randint

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home")

        self.electricity_label = tk.Label(root, text="Electricity")
        self.electricity_label.pack()

        self.voltage_label = tk.Label(root, text="Voltage")
        self.voltage_label.pack()

        self.power_label = tk.Label(root, text="Power")
        self.power_label.pack()

        self.light_label = tk.Label(root, text="Light")
        self.light_label.pack()

        self.dimmer_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Dimmer")
        self.dimmer_slider.pack()

        self.heating_label = tk.Label(root, text="Heating")
        self.heating_label.pack()

        self.temperature_label = tk.Label(root, text="Temperature")
        self.temperature_label.pack()

        self.rooms_temperature_label = tk.Label(root, text="Rooms Temperature")
        self.rooms_temperature_label.pack()

        self.outdoor_temperature_label = tk.Label(root, text="Outdoor Temperature")
        self.outdoor_temperature_label.pack()

        self.update_button = tk.Button(root, text="Update", command=self.update_values)
        self.update_button.pack()

    def update_values(self):
        self.electricity_label.config(text=f"Electricity: {randint(0, 100)} kW")
        self.voltage_label.config(text=f"Voltage: {randint(200, 240)} V")
        self.power_label.config(text=f"Power: {randint(0, 500)} W")
        self.light_label.config(text=f"Light: {'On' if self.dimmer_slider.get() > 0 else 'Off'}")
        self.heating_label.config(text=f"Heating: {'On' if self.temperature_slider.get() > 0 else 'Off'}")
        self.temperature_label.config(text=f"Temperature: {self.temperature_slider.get()} °C")
        self.rooms_temperature_label.config(text=f"Rooms Temperature: {randint(18, 25)} °C")
        self.outdoor_temperature_label.config(text=f"Outdoor Temperature: {randint(5, 30)} °C")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
