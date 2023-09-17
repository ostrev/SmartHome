from tkinter import *
from tkinter import ttk


class GUI:
    def __init__(self, root, controller):
        self.main_root = root
        self.main_root.configure(bg="#ffffff")
        self.main_root.title("Smart Home Manager")
        self.main_root.geometry("1920x1080")
        self.main_root.resizable(width=False, height=False)
        self.main_root['padx'] = 10
        self.main_root['pady'] = 10

        self.smart = controller
        self.image = PhotoImage(file="smart-home-img.png")
        self.image = self.image.subsample(4)

        # ALL Frames and widget
        self.buttons_frame = None
        self.status_frame = None
        self.display_frame = None
        self.main_treeview_frame = None
        self.div_frame = None
        self.operation_frame = None
        self.device_treeview_frame = None
        # TREEVIEW
        self.device_treeview = None
        self.rooms_treeview = None

        self.selected_device = None
        self.selected_room = None
        # LOAD
        self.smart.load_rooms_data()
        self.smart.load_devices_data()
        self.create_main_window()
        #  BIND

    def main_window(self):
        for widget in self.main_root.winfo_children():
            widget.destroy()
        self.create_main_window()
        self.selected_device = None
        self.selected_room = None

    def create_main_window(self):
        # Create BUTTON FRAME
        self.buttons_frame = Frame(self.main_root, bg="grey", width=300)
        self.buttons_frame.pack(side=RIGHT, fill=Y)
        self.buttons_frame.pack_propagate(False)

        buttons_separator0 = Frame(self.buttons_frame, height=15, bg="grey")
        buttons_separator1 = Frame(self.buttons_frame, height=15, bg="grey")
        buttons_separator2 = Frame(self.buttons_frame, height=15, bg="grey")
        buttons_separator3 = Frame(self.buttons_frame, height=15, bg="grey")

        button1 = Button(self.buttons_frame, text="Main", command=lambda: self.main_window(), height=2)
        button2 = Button(self.buttons_frame, text="Add Device",
                         command=lambda: self.create_device(self.operation_frame), height=2)
        button3 = Button(self.buttons_frame, text="Edit Device", command=lambda: self.edit_device(self.operation_frame),
                         height=2)
        button4 = Button(self.buttons_frame, text="Remove Device", command=lambda: self.delete_device(), height=2)

        button5 = Button(self.buttons_frame, text="Add Room",
                         command=lambda: self.create_rooms(self.operation_frame), height=2)
        button6 = Button(self.buttons_frame, text="Edit Room",
                         command=lambda: self.edit_room(self.operation_frame), height=2)
        button7 = Button(self.buttons_frame, text="Remove Room", command=lambda: self.delete_room(), height=2)

        button8 = Button(self.buttons_frame, text="Update Status", command=lambda: self.update_status(), height=2)

        buttons_separator0.pack(side=TOP, fill=X)
        button1.pack(side=TOP, fill=X)
        buttons_separator1.pack(side=TOP, fill=X)
        button2.pack(side=TOP, fill=X)
        button3.pack(side=TOP, fill=X)
        button4.pack(side=TOP, fill=X)
        buttons_separator2.pack(side=TOP, fill=X)
        button5.pack(side=TOP, fill=X)
        button6.pack(side=TOP, fill=X)
        button7.pack(side=TOP, fill=X)
        buttons_separator3.pack(side=TOP, fill=X)
        button8.pack(side=TOP, fill=X)

        # Create STATUS FRAME
        status_frame_all = Frame(self.main_root, bg="grey", width=500)
        status_frame_all.pack(side=RIGHT, fill=Y)

        status_frame_lab = Frame(status_frame_all, bg="grey", width=500)
        status_frame_lab.pack(side=TOP)
        separator = Frame(status_frame_lab, height=15, bg="grey")
        separator.pack(side=TOP, fill=X)

        font_style = ("Helvetica", 16)
        text_color = "#d6a523"
        status_label = Label(status_frame_lab, text="STATUS", bg="grey", font=font_style, fg=text_color)
        status_label.pack(side=TOP)

        self.status_frame = Frame(status_frame_all, bg="grey", width=500)
        self.status_frame.pack(side=RIGHT, fill=Y)
        self.status_frame.pack_propagate(False)

        # Create DISPLAY FRAME
        self.display_frame = Frame(self.main_root, padx=15, bg="grey")
        self.display_frame.pack(side=LEFT, fill=BOTH)
        separator = Frame(self.display_frame, height=15, bg="grey")
        separator.pack(side=TOP, fill=X)
        data_label = Label(self.display_frame, text="YOUR ROOMS", bg="grey", font=font_style, fg=text_color)
        data_label.pack(side=TOP)

        # Create MAIN TREEVIEW FRAME for ROOMS
        self.main_treeview_frame = Frame(self.display_frame, padx=15, bg="#ffffff", height=400, width=1100)
        self.main_treeview_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.main_treeview_frame.pack_propagate(False)

        columns = ("Number", "Rooms",)
        self.rooms_treeview = ttk.Treeview(self.main_treeview_frame, columns=columns, show="headings")
        self.rooms_treeview.heading("Rooms", text="Rooms", anchor="center")
        self.rooms_treeview.heading("Number", text="Number", anchor="center")
        self.rooms_treeview.column("Number", width=75, stretch=True)
        self.rooms_treeview.column("Rooms", width=300, stretch=True)
        self.rooms_treeview.pack(side=RIGHT, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        # Insert img
        image_label = Label(self.main_treeview_frame, image=self.image)
        image_label.pack(side=LEFT, padx=10, pady=10)
        self.rooms_treeview.bind("<<TreeviewSelect>>", self.handle_room_selection)

        # Create div for OPERATION and DEVICE TREEVIEW
        self.div_frame = Frame(self.display_frame, padx=15, pady=15, bg="#d9d7d1", height=400)
        self.div_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.div_frame.pack_propagate(False)

        self.operation_frame = Frame(self.div_frame, padx=15, bg="#d9d7d1", height=400, width=200)
        self.operation_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.operation_frame.pack_propagate(False)

        self.device_treeview_frame = Frame(self.div_frame, padx=15, bg="#d9d7d1", height=400, width=500)
        self.device_treeview_frame.pack(side=LEFT, fill=BOTH, expand=True)
        self.device_treeview_frame.pack_propagate(False)

        self.create_device_treeview()
        # LOAD ROOMS and DEVICES

        self.load_rooms(self.rooms_treeview)
        self.load_devices(self.device_treeview)

    def load_rooms(self, treeview):
        treeview.delete(*treeview.get_children())
        rooms = self.smart.rooms
        for room in rooms:
            treeview.insert("", "end", values=room[:2], tags=("row",))

    def load_devices(self, treeview):
        treeview.delete(*treeview.get_children())
        devices = self.smart.devices
        for device in devices:
            treeview.insert("", "end", values=device, tags=("row",))

    def create_rooms(self, operation):
        for widget in operation.winfo_children():
            widget.destroy()

        room_label = Label(operation, text="Add room", font=('Helvetica', 16), bg="#d9d7d1")
        room_name_label = Label(operation, text="Name: ", bg="#d9d7d1")
        room_entry = ttk.Entry(operation)
        button = ttk.Button(operation, text="Add", command=lambda: self.add_room(room_entry.get()))

        room_label.pack(side=TOP)
        room_name_label.pack(side=TOP)
        room_entry.pack(side=TOP)

        button.pack(side=TOP)

    def edit_room(self, operation):
        for widget in operation.winfo_children():
            widget.destroy()

        def save(id):
            self.smart.edit_room(room_entry.get(), room_id)
            for widget in operation.winfo_children():
                widget.destroy()

            self.load_rooms(self.rooms_treeview)

            if self.selected_room:
                self.rooms_treeview.focus_set()
                children_device = self.rooms_treeview.get_children()
                for i, child in enumerate(children_device):
                    child_id = int(self.rooms_treeview.item(child, 'values')[0])
                    if child_id == id:
                        self.rooms_treeview.focus(children_device[i])
                        self.rooms_treeview.selection_set(children_device[i])

        if self.selected_room:
            item_values = self.rooms_treeview.item(self.selected_room, "values")
            room_id = int(item_values[0])

            room_label = Label(operation, text="Edit room", font=('Helvetica', 16), bg="#d9d7d1")
            room_label.pack(side=TOP)

            room_name_label = Label(operation, text="Name: ", bg="#d9d7d1")
            room_name_label.pack(side=TOP)

            room_entry = ttk.Entry(operation)
            room_entry.pack(side=TOP)
            room_entry.insert(0, item_values[1])

            button = ttk.Button(operation, text="Save", command=lambda: save(room_id))
            button.pack(side=TOP)

    def delete_room(self):
        if self.selected_room:
            items_values = self.rooms_treeview.item(self.selected_room, "values")
            room_id = int(items_values[0])
            self.smart.delete_room(room_id)
            self.main_window()

    def create_device(self, operation):
        for widget in operation.winfo_children():
            widget.destroy()
        device_label = Label(operation, text="Add device", font=('Helvetica', 16), bg="#d9d7d1")
        device_name_label = Label(operation, text="Name: ", bg="#d9d7d1")
        device_entry = ttk.Entry(operation)

        type_device = ("LED", "Electricity", "Heating", "AC", "Vent")
        type_label = Label(operation, text="Type", bg="#d9d7d1")
        type_combobox = ttk.Combobox(operation, values=type_device)

        room_label = Label(operation, text="Room: ", bg="#d9d7d1")

        room_names = self.smart.rooms
        room_combobox = ttk.Combobox(operation, values=room_names)

        button = ttk.Button(operation, text="Add", command=lambda: self.add_device(
            device_entry.get(),
            room_combobox.get(),
            type_combobox.get()))

        device_label.pack(side=TOP)
        device_name_label.pack(side=TOP)
        device_entry.pack(side=TOP)
        type_label.pack(side=TOP)
        type_combobox.pack(side=TOP)
        room_label.pack(side=TOP)
        room_combobox.pack(side=TOP)
        button.pack(side=TOP)

    def edit_device(self, operation):
        for widget in operation.winfo_children():
            widget.destroy()

        def save(id, name, room, dev_type):
            self.smart.edit_device(id, name, dev_type, room)
            self.update_status()
            for widget in operation.winfo_children():
                widget.destroy()

        if self.selected_device:
            items_values = self.device_treeview.item(self.selected_device, "values")
            dev_id = int(items_values[0])

            device_label = Label(operation, text="Edit device", font=('Helvetica', 16), bg="#d9d7d1")
            device_label.pack(side=TOP)
            device_name_label = Label(operation, text="Name: ", bg="#d9d7d1")
            device_name_label.pack(side=TOP)
            device_entry = ttk.Entry(operation)
            device_entry.pack(side=TOP)
            device_entry.insert(0, items_values[1])

            type_device = ("LED", "Electricity", "Heating", "AC", "Vent")
            type_label = Label(operation, text="Type", bg="#d9d7d1")
            type_label.pack(side=TOP)
            type_combobox = ttk.Combobox(operation, values=type_device)
            type_combobox.pack(side=TOP)
            type_combobox.set(items_values[2])

            room_label = Label(operation, text="Room: ", bg="#d9d7d1")
            room_label.pack(side=TOP)
            room_names = self.smart.rooms
            room_combobox = ttk.Combobox(operation, values=room_names)
            room_combobox.pack(side=TOP)
            room_combobox.set(items_values[3])

            button = ttk.Button(operation, text="Save", command=lambda: save(
                dev_id,
                device_entry.get(),
                room_combobox.get()[0],
                type_combobox.get()))
            button.pack(side=TOP)

    def add_device(self, name, room, type_device):
        room_id = room.split(' ')[0]

        self.smart.add_device(name, room_id, type_device)
        self.load_devices(self.device_treeview)

        for widget in self.operation_frame.winfo_children():
            widget.destroy()

    def add_room(self, name):
        for room in self.smart.rooms:
            if room[1] == name:
                error_root = Tk()
                error_root.title('Error')
                error_root.geometry("500x200")
                string_error = f'{name} is already created'
                Label(error_root, text=string_error).pack()
                print('Error')
                return

        self.smart.add_room(name)
        self.load_rooms(self.rooms_treeview)
        for widget in self.operation_frame.winfo_children():
            widget.destroy()

    def delete_device(self):
        if self.selected_device:
            items_values = self.device_treeview.item(self.selected_device, "values")
            dev_id = int(items_values[0])
            self.smart.delete_device(dev_id)
            self.main_window()

    def create_device_treeview(self):
        columns = ("ID", "Name", "Type", "Room", "Status")
        self.device_treeview = ttk.Treeview(self.device_treeview_frame, columns=columns, show="headings")
        for col in columns:
            self.device_treeview.heading(col, text=col, anchor="center")
            if col == 'ID':
                self.device_treeview.column(col, width=50, stretch=False, anchor="center")
            else:
                self.device_treeview.column(col, width=120, stretch=True)
        self.device_treeview.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)  # Set height of the row

        tree_scrollbar = ttk.Scrollbar(self.device_treeview_frame, orient="vertical",
                                       command=self.device_treeview.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.device_treeview.configure(yscrollcommand=tree_scrollbar.set)
        self.load_devices(self.device_treeview)
        self.device_treeview.bind("<<TreeviewSelect>>", self.handle_device_selection)

    def handle_room_selection(self, event):
        self.selected_room = self.rooms_treeview.selection()
        if self.selected_room:
            dev_id = int(self.rooms_treeview.item(self.selected_room, "values")[0])
            self.device_treeview.delete(*self.device_treeview.get_children())
            for device in self.smart.devices:
                if device[3] == dev_id:
                    self.device_treeview.insert("", "end", values=device, tags=("row",))

    def handle_device_selection(self, event):
        self.selected_device = self.device_treeview.selection()
        if self.selected_device:
            device_data = self.device_treeview.item(self.selected_device, "values")
            device_type = device_data[2]
            if device_type == 'LED':
                print(device_data)
                self.create_led_status(device_data)
            elif device_type == 'Electricity':
                self.create_electricity_status(device_data)
                print(device_data)
            else:
                self.create_hvac_status(device_data)
                print(device_data)

    def create_led_status(self, device_data):
        for widget in self.status_frame.winfo_children():
            widget.pack_forget()

        def on_cct_change(dev_id):
            new_cct_value = int(cct_var.get())
            self.smart.change_parameter_cct(dev_id, new_cct_value)
            if self.selected_device:
                data = list(self.device_treeview.item(self.selected_device, "values"))
                data[6] = new_cct_value
                data[7] = None
                rgb_menu.set("None")
                new_tuple = tuple(data)
                self.device_treeview.item(self.selected_device, values=new_tuple)
                self.device_treeview.update()

        def on_status_change(dev_id):
            new_status_value = status_var.get()
            self.smart.change_parameter_status(dev_id, new_status_value)
            if self.selected_device:
                data = list(self.device_treeview.item(self.selected_device, "values"))
                data[4] = new_status_value
                new_tuple = tuple(data)
                self.device_treeview.item(self.selected_device, values=new_tuple)
                self.device_treeview.update()

        def on_intensity_change(dev_id):
            new_intensity_value = intensity_var.get()
            self.smart.change_parameter_intensity(dev_id, new_intensity_value)
            if self.selected_device:
                data = list(self.device_treeview.item(self.selected_device, "values"))
                data[5] = new_intensity_value
                new_tuple = tuple(data)
                self.device_treeview.item(self.selected_device, values=new_tuple)
                self.device_treeview.update()

        def on_rgb_change(dev_id):
            selected_option = rgb_menu.get()
            selected_value = None
            for option in rgb_options:
                if option[0] == selected_option:
                    selected_value = (option[1], option[2])
                    print(f"Selected value: {selected_value}")

            self.smart.change_parameter_rgb(dev_id, selected_value, selected_option)
            if self.selected_device:
                data = list(self.device_treeview.item(self.selected_device, "values"))
                data[7] = selected_option
                data[6] = None
                cct_menu.set("None")

                new_tuple = tuple(data)
                self.device_treeview.item(self.selected_device, values=new_tuple)
                self.device_treeview.update()

        status = device_data[4]
        intensity = device_data[5]
        cct = device_data[6]
        rgb = device_data[7]

        # STATUS
        status_label = Label(self.status_frame, text="Status:")
        status_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        status_var = StringVar()
        Label(self.status_frame, textvariable=status_var)  # this is line to fix not loading ot combobox
        status_entry = ttk.Combobox(self.status_frame, textvariable=status_var, values=["ON", "OFF"])
        status_entry.pack(side=TOP)
        separator = Frame(self.status_frame, height=50, bg="grey")
        separator.pack(side=TOP, fill=X)

        status_var.set(status)
        status_entry.bind("<<ComboboxSelected>>",
                          lambda event, device_id=device_data[0]: on_status_change(device_id))

        # INTENSITY
        intensity_label = Label(self.status_frame, text="Intensity:")
        intensity_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        intensity_var = IntVar()
        intensity_label_two = Label(self.status_frame, textvariable=intensity_var)
        intensity_label_two.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        intensity_scale = Scale(
            self.status_frame,
            variable=intensity_var,
            from_=10, to=100,
            orient=HORIZONTAL,
            length=200,
            resolution=10)
        intensity_scale.pack(side=TOP)
        separator = Frame(self.status_frame, height=50, bg="grey")
        separator.pack(side=TOP, fill=X)
        intensity_var.set(intensity)
        intensity_scale.bind("<ButtonRelease-1>",
                             lambda event, device_id=device_data[0]: on_intensity_change(device_id))

        # CCT
        cct_label = Label(self.status_frame, text="Color Temperature:")
        cct_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        cct_var = StringVar()
        Label(self.status_frame, textvariable=cct_var)
        cct_menu = ttk.Combobox(self.status_frame, textvariable=cct_var,
                                values=["None", "2700", "3000", "4000", "6000"])
        cct_menu.pack(side=TOP)
        separator = Frame(self.status_frame, height=50, bg="grey")
        separator.pack(side=TOP, fill=X)
        cct_var.set(cct)
        cct_menu.bind("<<ComboboxSelected>>",
                      lambda event, device_id=device_data[0]: on_cct_change(device_id))

        # COLOUR
        rgb_options = [("None", None), ("Blue", 240, 100), ("Red", 0, 100), ("Green", 90, 100)]
        rgb_label = Label(self.status_frame, text="Color:")
        rgb_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        rgb_var = StringVar()
        Label(self.status_frame, textvariable=rgb_var)
        rgb_menu = ttk.Combobox(self.status_frame, textvariable=rgb_var)
        rgb_menu['values'] = [option[0] for option in rgb_options]
        rgb_menu.pack(side=TOP)
        rgb_var.set(rgb)
        rgb_menu.bind("<<ComboboxSelected>>",
                      lambda event, device_id=device_data[0]: on_rgb_change(device_id))

    def create_electricity_status(self, device_data):
        for widget in self.status_frame.winfo_children():
            widget.pack_forget()

        status = device_data[4]
        power = float(int(device_data[5]) / 1000)
        plug_time = device_data[7]

        def on_status_change(dev_id):
            new_status_value = status_var.get()
            self.smart.change_plug_status(dev_id, new_status_value)
            if self.selected_device:
                data = list(self.device_treeview.item(self.selected_device, "values"))
                data[4] = new_status_value
                new_tuple = tuple(data)
                self.device_treeview.item(self.selected_device, values=new_tuple)
                self.device_treeview.update()

        # STATUS
        status_label = Label(self.status_frame, text="Status:")
        status_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        status_var = StringVar()
        Label(self.status_frame, textvariable=status_var)  # this is line to fix not loading ot combobox
        status_entry = ttk.Combobox(self.status_frame, textvariable=status_var, values=["ON", "OFF"])
        status_entry.pack(side=TOP)
        separator = Frame(self.status_frame, height=50, bg="grey")
        separator.pack(side=TOP, fill=X)
        status_var.set(status)
        status_entry.bind("<<ComboboxSelected>>",
                          lambda event, device_id=device_data[0]: on_status_change(device_id))
        power_label = Label(self.status_frame, text="Power in W:")
        power_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        power_var = StringVar()
        power_label_w = Label(self.status_frame, textvariable=power_var)
        power_label_w.pack(side=TOP)
        separator = Frame(self.status_frame, height=50, bg="grey")
        separator.pack(side=TOP, fill=X)
        power_var.set(power)

        plug_time_label = Label(self.status_frame, text="Time in seconds:")
        plug_time_label.pack(side=TOP)
        separator = Frame(self.status_frame, height=5, bg="grey")
        separator.pack(side=TOP, fill=X)
        plug_time_var = StringVar()
        plug_time_label_w = Label(self.status_frame, textvariable=plug_time_var)
        plug_time_label_w.pack(side=TOP)
        plug_time_var.set(plug_time)

    def create_hvac_status(self, device_data):
        for widget in self.status_frame.winfo_children():
            widget.pack_forget()

    def update_status(self):
        if self.selected_device:
            selected_device_id = int(self.device_treeview.item(self.selected_device, "values")[0])

        self.smart.update_live_parameters()  # take parameters from real device and update DB
        self.smart.load_devices_data()  # load parameters in devices list
        self.load_devices(self.device_treeview)  # load devices in treeview

        # set selected device row after updating
        if self.selected_device:
            self.device_treeview.focus_set()
            children_device = self.device_treeview.get_children()
            for i, child in enumerate(children_device):
                child_id = int(self.device_treeview.item(child, 'values')[0])
                if child_id == selected_device_id:
                    self.device_treeview.focus(children_device[i])
                    self.device_treeview.selection_set(children_device[i])

    def run(self):
        self.main_root.mainloop()
