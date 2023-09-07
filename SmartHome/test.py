from tkinter import *
from tkinter import ttk


def main_window():
    main_root = Tk()
    main_root.title("Smart Home Manager")
    main_root.geometry("1920x1080")  # Задаване на размерите на главния прозорец

    # Създаване на рамка за бутоните и самите бутони
    buttons_frame = ttk.Frame(main_root)
    buttons_frame.pack(side=RIGHT, fill=Y)

    button1 = ttk.Button(buttons_frame, text="Main", command=lambda: show_data("Бутон 1 беше натиснат"))
    button2 = ttk.Button(buttons_frame, text="Electricity", command=lambda: show_data("Бутон 2 беше натиснат"))
    button3 = ttk.Button(buttons_frame, text="Lighting", command=lambda: show_data("Бутон 3 беше натиснат"))

    # Позициониране на бутоните вдясно
    button1.pack(side=TOP, fill=X)
    button2.pack(side=TOP, fill=X)
    button3.pack(side=TOP, fill=X)


    # Визуализация на данните от бутоните
    display_frame = ttk.Frame(main_root)
    display_frame.pack(side=LEFT, fill=X)
    data_label = ttk.Label(display_frame, text="", )  # Label за данните
    data_label.pack()

    def show_data(data):
        data_label.config(text=data)  # Променя текста в Label с избраната информация

    main_root.mainloop()


if __name__ == "__main__":
    main_window()
