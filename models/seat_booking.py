class SeatBooking:
    def __init__(self, seat_booking_id, booking_id, bus_id, seat_number):
        self.__id = seat_booking_id
        self.__booking_id = booking_id
        self.__bus_id = bus_id
        self.__seat_number = int(seat_number)

    @property
    def id(self): 
        return self.__id
    
    @property
    def booking_id(self): 
        return self.__booking_id
    
    @property
    def bus_id(self): 
        return self.__bus_id
    
    @property
    def seat_number(self): 
        return self.__seat_number