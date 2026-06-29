class SeatBooking:
    def __init__(self, seat_booking_id, booking_id, bus_id, seat_number):
        self.__id = seat_booking_id
        self.__booking_id = booking_id
        self.__bus_id = bus_id
        self.__seat_number = int(seat_number)

    @property
    def id(self): 
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value
    
    @property
    def booking_id(self): 
        return self.__booking_id

    @booking_id.setter
    def booking_id(self, value):
        self.__booking_id = value
    
    @property
    def bus_id(self): 
        return self.__bus_id

    @bus_id.setter
    def bus_id(self, value):
        self.__bus_id = value
    
    @property
    def seat_number(self): 
        return self.__seat_number

    @seat_number.setter
    def seat_number(self, value):
        self.__seat_number = value
