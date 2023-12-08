from User import User

class Driver(User):    
    def createProfile(self, FirstName, LastName, Phone, Role):
        super().createProfile(FirstName, LastName, Phone, Role)
    
    def currentLocation(self, Location):
        super().currentLocation(Location)
    
    def set_avialability(self, avialable, current_ride):
        self.avialable = avialable
        self.current_ride = current_ride