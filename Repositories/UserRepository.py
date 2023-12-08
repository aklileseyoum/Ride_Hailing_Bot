from Repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super(UserRepository, self).__init__()

    def get_drivers(self):
        drivers = []
        for key in self.keys("*"):
            user = self.get(key)
            if user['role'] == 'Driver':
                drivers.append(user)

        return drivers
