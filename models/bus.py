class Bus:
    def __init__(self, bus_id, bus_name, origin, destination, journey_date, departure_time, total_seats, available_seats, operator_id, ticket_price):
        self.__id = bus_id
        self.__bus_name = bus_name
        self.__origin = origin
        self.__destination = destination
        self.__journey_date = journey_date
        self.__departure_time = departure_time
        self.__total_seats = total_seats
        self.__available_seats = available_seats
        self.__operator_id = operator_id
        self.__ticket_price = float(ticket_price) 

    
    @property
    def id(self): 
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def bus_name(self): 
        return self.__bus_name

    @bus_name.setter
    def bus_name(self, value):
        self.__bus_name = value

    @property
    def origin(self): 
        return self.__origin

    @origin.setter
    def origin(self, value):
        self.__origin = value

    @property
    def destination(self): 
        return self.__destination

    @destination.setter
    def destination(self, value):
        self.__destination = value

    @property
    def journey_date(self): 
        return self.__journey_date

    @journey_date.setter
    def journey_date(self, value):
        self.__journey_date = value

    @property
    def departure_time(self): 
        return self.__departure_time

    @departure_time.setter
    def departure_time(self, value):
        self.__departure_time = value

    @property
    def total_seats(self): 
        return self.__total_seats

    @total_seats.setter
    def total_seats(self, value):
        self.__total_seats = value

    @property
    def available_seats(self): 
        return self.__available_seats

    @available_seats.setter
    def available_seats(self, value):
        self.__available_seats = value

    @property
    def operator_id(self): 
        return self.__operator_id

    @operator_id.setter
    def operator_id(self, value):
        self.__operator_id = value

    @property
    def ticket_price(self): 
        return self.__ticket_price

    @ticket_price.setter
    def ticket_price(self, value): 
        if float(value) < 0: 
            raise ValueError("Price cannot be negative.")
        self.__ticket_price = float(value)

    def allocate_seats(self, count):
        if count > self.__available_seats:
            raise ValueError("Not enough available seats.")
        self.__available_seats -= count

    def release_seats(self, count):
        if self.__available_seats + count > self.__total_seats:
            raise ValueError("Exceeds bus capacity.")
        self.__available_seats += count