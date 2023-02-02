import csv
import json
from uuid import uuid4
from tkinter import ttk
from event import Event
import tkinter as tk


class Application(tk.Tk):
    events = []

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.load_events()
        container = tk.Frame(self, background="#B5B5B5")
        container.pack(side="top", fill="both", expand=True)
        style = ttk.Style()

        style.configure('TButton', font=('calibri', 10, 'bold'), borderwidth='4')
        self.frames = {}

        for F in (StartPage, CreateEvent, RegisterForEvent, EventInfo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def remove_event(self, uuid):
        for event in self.events:
            if event.uuid == uuid:
                self.events.remove(event)
        with open("events.json") as file:
            start_dict = json.load(file)
            for index, event in enumerate(start_dict["events"]):
                if event["uuid"] == uuid.__str__():
                    start_dict["events"].pop(index)

        with open("events.json", "w") as file:
            json.dump(start_dict, file, indent=4)

    def add_event(self):
        new_event = self.frames[CreateEvent]
        event = Event(
            uuid4(),
            new_event.name.get(),
            new_event.date.get(),
            new_event.time.get(),
            new_event.address.get(),
            new_event.guests.get(),
            new_event.spiker_name.get(),
            new_event.spiker_phone.get(),
        )
        self.events.append(event)

        self.frames[StartPage].update()
        with open("events.json") as file:
            events = json.load(file)
            try:
                events["events"].append({
                    "uuid": event.uuid.__str__(),
                    "name": event.name,
                    "date": event.date,
                    "time": event.time,
                    "address": event.address,
                    "guests": event.guests,
                    "spiker_name": event.spiker_name,
                    "spiker_phone": event.spiker_phone
                })
            except Exception:
                events["events"] = []
                events["events"].append({
                    "uuid": event.uuid.__str__(),
                    "name": event.name,
                    "date": event.date,
                    "time": event.time,
                    "address": event.address,
                    "guests": event.guests,
                    "spiker_name": event.spiker_name,
                    "spiker_phone": event.spiker_phone
                })
        with open("events.json", "w") as file:
            json.dump(events, file, indent=4)
        self.show_frame(StartPage)

    def save_event(self):
        new_event = self.frames[CreateEvent]
        self.events.append(
            Event(
                None,
                new_event.name.get(),
                new_event.date.get(),
                new_event.time.get(),
                new_event.address.get(),
                new_event.guests.get(),
                new_event.spiker_name.get(),
                new_event.spiker_phone.get(),
            )
        )
        frame = self.frames[StartPage]
        print(self.events)
        frame.tkraise()

    def show_info(self, event):
        self.show_frame(EventInfo)
        frame = self.frames[EventInfo]
        frame.name.config(text=event.name)
        frame.date.config(text=event.date)
        frame.time.config(text=event.time)
        frame.address.config(text=event.address)
        frame.guests.config(text=str(event.guests))
        frame.spiker_name.config(text=event.spiker_name)
        frame.spiker_phone.config(text=event.spiker_phone)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.clear_entry()

    def register_for_event(self):
        user = self.frames[RegisterForEvent]
        events = self.frames[StartPage]
        event_ids = []
        for event in events.events:
            if event.var.get():
                event_ids.append(event.event.uuid.__str__())
        user_name = user.name.get()
        user_email = user.name.get()
        user_phone = user.name.get()
        with open("registered_guests.json") as file:
            start_dict = json.load(file)
            try:
                start_dict["users"].append({
                    "event_ids": event_ids,
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_phone": user_phone
                })
            except Exception:
                start_dict["users"] = []
                start_dict["users"].append({
                    "event_ids": event_ids,
                    "user_name": user_name,
                    "user_email": user_email,
                    "user_phone": user_phone
                })
        with open("registered_guests.json", "w") as file:
            json.dump(start_dict, file, indent=4)
        self.show_frame(StartPage)

    def load_events(self):
        with open("events.json") as file:
            json_events = json.load(file)["events"]
            for event in json_events:
                self.events.append(
                    Event(
                        event["uuid"],
                        event["name"],
                        event["date"],
                        event["time"],
                        event["address"],
                        event["guests"],
                        event["spiker_name"],
                        event["spiker_phone"],
                    )
                )

    def clear_entry(self):
        create_ev = self.frames[CreateEvent]
        create_ev.name.delete(0, tk.END)
        create_ev.date.delete(0, tk.END)
        create_ev.time.delete(0, tk.END)
        create_ev.address.delete(0, tk.END)
        create_ev.guests.delete(0, tk.END)
        create_ev.spiker_phone.delete(0, tk.END)
        create_ev.spiker_name.delete(0, tk.END)

        reg_for_ev = self.frames[RegisterForEvent]
        reg_for_ev.name.delete(0, tk.END)
        reg_for_ev.user_email.delete(0, tk.END)
        reg_for_ev.user_phone.delete(0, tk.END)


class StartPage(tk.Frame):

    def __init__(self, parent, controller: Application):
        tk.Frame.__init__(self, parent, background="#B5B5B5")
        self.controller = controller
        self.config(padx=50, pady=10)
        self.ev_frame = tk.Frame(self, background="#B5B5B5")
        self.events = []

        for event in controller.events:
            item = EventItem(self.ev_frame, event, lambda n: self.remove_events(n), self.on_check,
                             lambda e: controller.show_info(e))
            item.pack(fill="x", anchor="n")
            self.events.append(item)
        self.ev_frame.pack(expand=True, fill="both")

        self.fill_form_btn = ttk.Button(self, text="Заполнить анкету",
                                        command=lambda: controller.show_frame(RegisterForEvent))
        self.fill_form_btn.pack(side="right", anchor="se", pady=8)
        self.fill_form_btn["state"] = tk.DISABLED
        ttk.Button(self, text="Добавить", command=lambda: controller.show_frame(CreateEvent)).pack(
            anchor="se",
            side="right",
            padx=(0, 10),
            pady=8
        )

    def remove_events(self, uuid):
        index = 0
        for event in self.controller.events:
            if event.uuid == uuid:
                index = self.controller.events.index(event)

        self.controller.remove_event(uuid)
        self.events[index].destroy()
        del self.events[index]

    def update(self):
        for ev in self.events:
            ev.destroy()

        self.events = []

        for event in self.controller.events:
            item = EventItem(self.ev_frame, event, lambda n: self.remove_events(n), self.on_check,
                             lambda e: self.controller.show_info(e))
            item.pack(fill="x", anchor="n")
            self.events.append(item)

    def on_check(self):
        has_selected_events = False
        for event in self.events:
            if event.var.get():
                has_selected_events = True
        if has_selected_events:
            self.fill_form_btn["state"] = tk.NORMAL
        else:
            self.fill_form_btn["state"] = tk.DISABLED


class RegisterForEvent(tk.Frame):
    bg_color = "#D9D9D9"

    def __init__(self, parent, controller: Application):
        tk.Frame.__init__(self, parent, background=self.bg_color)
        self.controller = controller
        tk.Label(self, text="Запись на мероприятие:", anchor="w", bg=self.bg_color).pack(fill="x")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        self.name = tk.Entry(self)
        self.user_email = tk.Entry(self, width=30)
        self.user_phone = tk.Entry(self, width=15)
        self.initUI()

    def initUI(self):
        self.config(padx=50, pady=10)

        tk.Label(self, text="ФИО:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.name.pack(anchor="w")

        tk.Label(self, text="Почта:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.user_email.pack(anchor="w")

        tk.Label(self, text="Телефон:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.user_phone.pack(anchor="w")

        ttk.Button(self, text="Записаться", command=lambda: self.controller.register_for_event()).pack(
            anchor="se",
            side="right",
            padx=(0, 10),
            pady=8
        )
        ttk.Button(self, text="Отмена", command=lambda: self.controller.show_frame(StartPage)).pack(
            anchor="se",
            side="right",
            padx=(0, 10),
            pady=8
        )


class EventItem(tk.Frame):
    bg_color = "#D9D9D9"

    def __init__(self, parent, event: Event, on_remove, on_check, on_show_info):
        self.var = tk.BooleanVar()
        self.var.set(False)
        self.event = event
        tk.Frame.__init__(self, parent, bg=self.bg_color, padx=10, pady=8)

        tk.Label(self, text=event.date, bg=self.bg_color).pack(anchor="w")
        ttk.Separator(self, orient="horizontal").pack(expand=True, fill="both")

        content = tk.Frame(self, bg=self.bg_color)
        delete_icon = tk.PhotoImage(file=r"./delete.png")
        icon = delete_icon.subsample(3, 3)
        tk.Checkbutton(content, variable=self.var, onvalue=True, offvalue=False, bg=self.bg_color,
                       command=on_check).pack(
            side="left")
        tk.Label(content, text=event.name, anchor="s", bg=self.bg_color).pack(side="left", fill="x", expand=True,
                                                                              anchor="nw")
        ttk.Button(content, text="Информация", style="TButton", command=lambda: on_show_info(event)).pack(side="left",
                                                                                                          padx=10)

        delete_btn = tk.Button(content, text="Remove", image=icon, command=lambda: on_remove(event.uuid), padx=6,
                               pady=4,
                               relief="flat",
                               borderwidth=0)
        delete_btn.image = icon
        delete_btn.pack(side="left")

        content.pack(expand=True, fill="x", pady=(1, 0))


class EventInfo(tk.Frame):
    bg_color = "#D9D9D9"

    def __init__(self, parent, controller: Application):
        tk.Frame.__init__(self, parent, background=self.bg_color)
        self.controller = controller
        tk.Label(self, text="Сведения о мероприятии:", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).pack(
            fill="x")
        ttk.Separator(self, orient="horizontal").pack(fill="x")

        tk.Label(self, text="Название:", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).pack(fill="x")
        self.name = tk.Label(self, anchor="w", bg=self.bg_color)
        self.name.pack(fill="x")

        row_frame = tk.Frame(self, bg=self.bg_color)
        tk.Label(row_frame, text="Дата:", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).grid(column=1,
                                                                                                           row=1)
        self.date = tk.Label(row_frame, anchor="w", bg=self.bg_color)
        self.date.grid(column=1, row=2)

        tk.Label(row_frame, text="Время: ", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).grid(column=2,
                                                                                                             row=1)
        self.time = tk.Label(row_frame, anchor="w", bg=self.bg_color)
        self.time.grid(column=2, row=2)
        row_frame.pack(anchor="w")

        tk.Label(self, text="Адрес:", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).pack(fill="x")
        self.address = tk.Label(self, anchor="w", bg=self.bg_color)
        self.address.pack(fill="x")

        tk.Label(self, text="Кол-во гостей:", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).pack(fill="x")
        self.guests = tk.Label(self, anchor="w", bg=self.bg_color)
        self.guests.pack(fill="x")

        tk.Label(self, text="ФИО спикера", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).pack(fill="x")
        self.spiker_name = tk.Label(self, anchor="w", bg=self.bg_color)
        self.spiker_name.pack(fill="x")

        tk.Label(self, text="Телефон спикера", anchor="w", bg=self.bg_color, font=('calibri', 10, 'bold')).pack(
            fill="x")
        self.spiker_phone = tk.Label(self, anchor="w", bg=self.bg_color)
        self.spiker_phone.pack(fill="x")
        self.initUI()

    def initUI(self):
        self.config(padx=50, pady=10)

        tk.Button(self, text="Закрыть", command=lambda: self.controller.show_frame(StartPage)).pack(side="right",
                                                                                                    padx=10)


class CreateEvent(tk.Frame):
    bg_color = "#D9D9D9"

    def __init__(self, parent, controller: Application):
        tk.Frame.__init__(self, parent, background=self.bg_color)
        self.controller = controller
        tk.Label(self, text="Сведения о мероприятии:", anchor="w", bg=self.bg_color).pack(fill="x")
        ttk.Separator(self, orient="horizontal").pack(expand=True, fill="x")

        self.name = tk.Entry(self)
        self.date = tk.Entry()
        self.time = tk.Entry()
        self.address = tk.Entry(self)
        self.guests = tk.Entry(self, width=6, )
        self.spiker_name = tk.Entry(self)
        self.spiker_phone = tk.Entry(self, width=15)
        self.initUI()

    def initUI(self):
        tk.Label(self, text="Название мероприятия:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.config(padx=50, pady=10)
        self.name.pack(anchor="w")

        row_frame = tk.Frame(self, bg=self.bg_color)
        tk.Label(row_frame, text="Дата проведения:*", anchor="w", bg=self.bg_color).grid(column=1, row=1)
        self.date = tk.Entry(row_frame, width=10)
        self.date.grid(column=1, row=2, sticky='w')
        tk.Label(row_frame, text="Время проведения:*", anchor="w", bg=self.bg_color).grid(column=2, row=1)
        self.time = tk.Entry(row_frame, width=5)
        self.time.grid(column=2, row=2, sticky='w')
        row_frame.pack(anchor="w")

        tk.Label(self, text="Адрес:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.address.pack(anchor="w")

        tk.Label(self, text="Кол-во гостей:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.guests.pack(anchor="w")

        tk.Label(self, text="ФИО спикера:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.spiker_name.pack(anchor="w")

        tk.Label(self, text="Контактный номер телефона спикера:*", anchor="w", bg=self.bg_color).pack(fill="x")
        self.spiker_phone.pack(anchor="w")
        tk.Button(self, text="Сохранить", command=lambda: self.controller.add_event()).pack(side="right",
                                                                                            padx=10)
        tk.Button(self, text="Закрыть", command=lambda: self.controller.show_frame(StartPage)).pack(side="right",
                                                                                                    padx=10)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
