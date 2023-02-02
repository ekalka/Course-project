from uuid import uuid4


class Event:
    name = ""
    date = ""
    time = ""
    address = ""
    guests = 0
    spiker_name = ""
    spiker_phone = ""

    def __init__(self, uuid, name, date, time, address, guests, spiker_name, spiker_phone):
        super().__init__()
        if uuid is not None:
            self.uuid = uuid
        else:
            self.uuid = uuid4()

        self.spiker_name = spiker_name
        self.guests = guests
        self.address = address
        self.time = time
        self.spiker_phone = spiker_phone
        self.date = date
        self.name = name
