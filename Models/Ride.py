class Ride:
    def __init__(self, ride_id, user, driver, current_location, destination, status, arrival_time, fare) -> None:
        self.ride_id = ride_id
        self.user = user
        self.driver = driver
        self.current_location = current_location
        self.destination = destination
        self.status = status
        self.arrival_time = arrival_time
        self.fare = fare