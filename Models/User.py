class User:
    def createProfile(self, id, username, FirstName, LastName, Phone):
        self.id = id
        self.username = username
        self.firstName = FirstName
        self.lastName = LastName
        self.phone = Phone
        self.rides_requested = []
        self.rides_completed = []

        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "phone": self.phone,
            "rides_requested": self.rides_requested,
            "rides_completed": self.rides_completed,
        }

    def currentLocation(self, Location):
        self.location = Location
        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "phone": self.phone,
            "location": self.location,
            "rides_requested": self.rides_requested,
            "rides_completed": self.rides_completed,
        }

    def set_user_role(self, role):
        self.role = role
        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "phone": self.phone,
            "role": self.role,
            "rides_requested": self.rides_requested,
            "rides_completed": self.rides_completed,
        }

    def update_profile(self, id, username, firstName, lastName, phone, role, rides_requested, rides_completed, current_location=None):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.role = role
        self.current_location = current_location
        self.rides_requested = rides_requested
        self.rides_completed = rides_completed
        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "phone": self.phone,
            "role": self.role,
            "current_location": self.current_location,
            "rides_requested": self.rides_requested,
            "rides_completed": self.rides_completed,
        }

    def ride_history(self, passenger_id, driver_id, date, destination):
        self.passenger_id = passenger_id
        self.driver_id = driver_id
        self.date = date
        self.destination = destination
        return {
            "passenger_id": self.passenger_id,
            "driver_id": self.driver_id,
            "date": self.date,
            "destination": self.destination
        }
