import sqlite3
from datetime import datetime


class DB:
    def __init__(self):
        self.db_name = "smart-home.sqlite"
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_database()

    def create_database(self):
        create_table_query_rooms = """
                CREATE TABLE IF NOT EXISTS rooms (
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
                """
        create_table_query_smart_devices = """
                CREATE TABLE IF NOT EXISTS smart_devices (
                    smart_device_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    room_id INTEGER,
                    type_device TEXT,
                    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
                )
                """
        create_table_query_electricity_devices = """
                CREATE TABLE IF NOT EXISTS electricity_devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    smart_device_id INTEGER,
                    name TEXT,
                    type_device TEXT,
                    status TEXT,
                    power INTEGER,
                    FOREIGN KEY (smart_device_id) REFERENCES smart_devices(smart_device_id)
                )
                """
        create_table_query_lighting_devices = """
                CREATE TABLE IF NOT EXISTS lighting_devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    smart_device_id INTEGER,
                    name TEXT,
                    type_device TEXT,
                    status TEXT,
                    intensity INTEGER,
                    CCT INTEGER,
                    RGB TEXT,
                    lux FLOAT,
                    power INTEGER,
                    FOREIGN KEY (smart_device_id) REFERENCES smart_devices(smart_device_id)

                )
                """
        create_table_query_heating_devices = """
                CREATE TABLE IF NOT EXISTS heating_devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    smart_device_id INTEGER,
                    name TEXT,
                    type_device TEXT,
                    status TEXT,
                    power INTEGER,
                    temperature_set INTEGER,
                    temperature INTEGER,
                    FOREIGN KEY (smart_device_id) REFERENCES smart_devices(smart_device_id)

                )
                """
        create_table_query_ac_devices = """
                CREATE TABLE IF NOT EXISTS ac_devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    smart_device_id INTEGER,
                    name TEXT,
                    type_device TEXT,
                    status TEXT,
                    power INTEGER,
                    temperature_set INTEGER,
                    temperature INTEGER,
                    FOREIGN KEY (smart_device_id) REFERENCES smart_devices(smart_device_id)

                )
                """
        create_table_query_vent_devices = """
                CREATE TABLE IF NOT EXISTS vent_devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    smart_device_id INTEGER,
                    name TEXT,
                    type_device TEXT,
                    status TEXT,
                    power INTEGER,
                    temperature INTEGER,
                    humidity_set INTEGER,
                    humidity INTEGER,
                    FOREIGN KEY (smart_device_id) REFERENCES smart_devices(smart_device_id)
                )
                """
        create_table_query_history = """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                device_id INTEGER,
                room_id INTEGER,
                power_value FLOAT,
                temperature_value FLOAT,
                humidity_value FLOAT,
                lux_value FLOAT,
                FOREIGN KEY (device_id) REFERENCES smart_devices(smart_device_id),
                FOREIGN KEY (room_id) REFERENCES rooms (room_id)
            )
        """
        self.cursor.execute(create_table_query_rooms)
        self.cursor.execute(create_table_query_smart_devices)
        self.cursor.execute(create_table_query_electricity_devices)
        self.cursor.execute(create_table_query_lighting_devices)
        self.cursor.execute(create_table_query_heating_devices)
        self.cursor.execute(create_table_query_ac_devices)
        self.cursor.execute(create_table_query_vent_devices)
        self.cursor.execute(create_table_query_history)
        self.connection.commit()

    def add_room(self, name):
        insert_query = """
                INSERT INTO rooms (name)
                VALUES (?)
                """
        values = (name,)
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def edit_room(self, name, id):
        update_query = "UPDATE rooms SET name = ? WHERE room_id = ?"
        self.cursor.execute(update_query, (name, id))
        self.connection.commit()

    def add_device(self, name, room_id, type_device):
        insert_query = """
                INSERT INTO smart_devices (name, room_id, type_device)
                VALUES (?, ?, ?)
                """
        values = (name, room_id, type_device)
        self.cursor.execute(insert_query, values)

        # Add devices to correct type table
        smart_device_id = self.cursor.lastrowid

        status = None
        power = None
        intensity = None
        CCT = None
        RGB = None
        lux = None
        temperature_set = None
        temperature = None
        humidity_set = None
        humidity = None
        if type_device == "LED":
            insert_query = """
                INSERT INTO lighting_devices (smart_device_id, name, type_device, status, intensity, CCT, RGB, lux, power)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            values = (smart_device_id, name, type_device, status, intensity, CCT, RGB, lux, power)
            self.cursor.execute(insert_query, values)
        elif type_device == "Electricity":
            insert_query = """
                            INSERT INTO electricity_devices (smart_device_id, name, type_device, status, power)
                            VALUES (?, ?, ?, ?, ?)
                            """
            values = (smart_device_id, name, type_device, status, power)
            self.cursor.execute(insert_query, values)
        elif type_device == "Heating":
            insert_query = """
                INSERT INTO heating_devices (smart_device_id, name, type_device, status, power, temperature_set, temperature)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """
            values = (smart_device_id, name, type_device, status, power, temperature_set, temperature)
            self.cursor.execute(insert_query, values)
        elif type_device == "AC":
            insert_query = """
                            INSERT INTO ac_devices (smart_device_id, name, type_device, status, power, temperature_set, temperature)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """
            values = (smart_device_id, name, type_device, status, power, temperature_set, temperature)
            self.cursor.execute(insert_query, values)
        elif type_device == "Vent":
            insert_query = """
                            INSERT INTO vent_devices (smart_device_id, name, type_device, status, power, temperature, humidity_set, humidity)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """
            values = (smart_device_id, name, type_device, status, power, temperature, humidity_set, humidity)
            self.cursor.execute(insert_query, values)
        self.connection.commit()

    def edit_device(self, id, name, dev_type, room):
        update_query = "UPDATE smart_devices SET name = ?, room_id = ?, type_device = ?  WHERE smart_device_id = ?"
        self.cursor.execute(update_query, (name, int(room), dev_type, int(id)))
        self.connection.commit()

    def delete_device(self, device_id):
        try:
            self.connection.execute("BEGIN")
            self.cursor.execute("DELETE FROM electricity_devices WHERE smart_device_id = ?", (device_id,))
            self.cursor.execute("DELETE FROM lighting_devices WHERE smart_device_id = ?", (device_id,))
            self.cursor.execute("DELETE FROM heating_devices WHERE smart_device_id = ?", (device_id,))
            self.cursor.execute("DELETE FROM ac_devices WHERE smart_device_id = ?", (device_id,))
            self.cursor.execute("DELETE FROM vent_devices WHERE smart_device_id = ?", (device_id,))
            self.cursor.execute("DELETE FROM smart_devices WHERE smart_device_id = ?", (device_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error: {str(e)}")

    def delete_room(self, room_id):
        try:
            self.connection.execute("BEGIN")
            self.cursor.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error: {str(e)}")

    def get_items(self, table):
        query = f"SELECT * FROM {table}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def get_devices(self):
        query = f"SELECT * FROM smart_devices"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def get_full_data_for_device(self, id_dev, type_dev):
        table_name = ''
        if type_dev == "LED":
            table_name = "lighting_devices"
        elif type_dev == "AC":
            table_name = "ac_devices"
        elif type_dev == "Vent":
            table_name = "vent_devices"
        elif type_dev == "Heating":
            table_name = "heating_devices"
        elif type_dev == "Electricity":
            table_name = "electricity_devices"

        query = f"SELECT * FROM {table_name} WHERE smart_device_id=?"
        self.cursor.execute(query, (id_dev,))
        rows = self.cursor.fetchone()
        return rows

    def update_cct(self, device_id, new_cct, update_db=True):
        update_query = "UPDATE lighting_devices SET CCT = ? WHERE id = ?"
        self.cursor.execute(update_query, (new_cct, device_id))
        if update_db:
            self.update_rgb(device_id, 'None', update_db=False)

        self.connection.commit()

    def update_status(self, device_id, new_status):
        update_query = "UPDATE lighting_devices SET status = ? WHERE id = ?"
        self.cursor.execute(update_query, (new_status, device_id))
        self.connection.commit()

    def update_intensity(self, device_id, new_intensity):
        update_query = "UPDATE lighting_devices SET intensity = ? WHERE id = ?"
        self.cursor.execute(update_query, (new_intensity, device_id))
        self.connection.commit()

    def update_rgb(self, device_id, new_rgb, update_db=True):
        update_query = "UPDATE lighting_devices SET RGB = ? WHERE id = ?"
        self.cursor.execute(update_query, (new_rgb, device_id))
        if update_db:
            self.update_cct(device_id, 'None', update_db=False)
        self.connection.commit()

    def update_plug_status(self, device_id, new_status):
        update_query = "UPDATE electricity_devices SET status = ? WHERE smart_device_id = ?"
        self.cursor.execute(update_query, (new_status, int(device_id)))
        self.connection.commit()

    def update_plug_parameters(self, *args):
        device_id = 1  # Hardcode
        power, on_time, total_energy = args

        update_query = "UPDATE electricity_devices SET power = ? WHERE id = ?"
        self.cursor.execute(update_query, (power, device_id))
        update_query = "UPDATE electricity_devices SET time = ? WHERE id = ?"
        self.cursor.execute(update_query, (on_time, device_id))

        self.connection.commit()

    def update_history(self, device_id, room_id, power_value, temperature_value, humidity_value, lux_value):
        timestamp = datetime.now()
        insert_query = """
            INSERT INTO history (timestamp, device_id, room_id, power_value, temperature_value, humidity_value, lux_value, )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (timestamp, device_id, room_id, power_value, temperature_value, humidity_value, lux_value)
        self.cursor.execute(insert_query, values)
        self.connection.commit()
