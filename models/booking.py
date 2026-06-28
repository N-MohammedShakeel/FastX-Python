class Booking:
    def __init__(self, booking_id, passenger_id, bus_id, seat_count, booking_date, status='BOOKED', total_price=0.00):
        self.__id = booking_id
        self.__passenger_id = passenger_id
        self.__bus_id = bus_id
        self.__seat_count = seat_count
        self.__booking_date = booking_date
        self.__status = status
        self.__total_price = float(total_price)

    @property
    def id(self): 
        return self.__id
    @property
    def passenger_id(self): 
        return self.__passenger_id
    @property
    def bus_id(self): 
        return self.__bus_id
    @property
    def seat_count(self): 
        return self.__seat_count
    @property
    def booking_date(self): 
        return self.__booking_date
    @property
    def status(self): 
        return self.__status
    @property
    def total_price(self): 
        return self.__total_price

    def cancel(self):
        if self.__status == 'CANCELLED':
            raise ValueError("Booking is already marked as cancelled.")
        self.__status = 'CANCELLED'