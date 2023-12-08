from Controllers.BaseController import BaseController
from Repositories.UserRepository import UserRepository
from Models.User import User
from Models.Role import Role
import random
import json


class UserController(BaseController):
    def __init__(self, html) -> None:
        super().__init__(html)
        self.user = User()

    async def start_handler(self, message) -> None:
        await message.answer(
            "🚗 Greetings, Traveler! 🌟 \nI am Ride Hailing Bot, at your service for a seamless ride. Kindly provide your contact details to embark on this journey. Your adventure awaits! ",
            reply_markup=self.ReplyKeyboardMarkup(
                resize_keyboard=True,
                keyboard=[
                    [
                        self.KeyboardButton(
                            text="Share Contact", request_contact=True, is_persistant=True)
                    ]
                ],
            ),
        )

    async def handle_contact_message(self, message) -> None:
        contact = message.contact
        self.userJson = self.user.createProfile(
            message.from_user.id, message.from_user.username, contact.first_name, contact.last_name, contact.phone_number)
        await message.answer(
            "Are you a driver or a passenger?",
            reply_markup=self.ReplyKeyboardMarkup(
                resize_keyboard=True,
                keyboard=[
                    [
                        self.KeyboardButton(text="Driver"),
                        self.KeyboardButton(text="Passenger"),
                    ]
                ],
            ),
        )

    async def role_handler(self, message) -> None:
        self.userJson = self.user.set_user_role(message.text)
        UserRepository().set(self.user.id, self.userJson)
        await message.answer("Thank you for registration")

    async def update_profile_handler(self, message, data):
        if UserRepository().exists(message.from_user.id):
            self.userJson = UserRepository().get(message.from_user.id)
            id = self.userJson["id"]
            username = self.userJson["username"]
            firstName = data["firstName"]
            lastName = data["lastName"]
            phone = data["phone"]
            role = data["role"]
            rides_requested = self.userJson["rides_requested"]
            rides_completed = self.userJson["rides_completed"]

            self.userJson = self.user.update_profile(
                id, username, firstName, lastName, phone, role, rides_requested, rides_completed)

            UserRepository().set(self.user.id, self.userJson)
            user = UserRepository().get(self.user.id)
            if role == "Driver" or role == "Passenger":
                await message.answer("Your profile was updated")
                text = (
                    "Profile: \n"+f"First Name: {user['firstName']}\nLast Name: {user['lastName']}\nPhone: {user['phone']}\nRole: {user['role']}\n")
                await message.answer(text=text)
            else:
                await message.answer(f"{data['role']} cannot be a role. Please write either Passenger or Driver")
        else:
            await message.answer("You don't have a profile, please register first")

    async def get_profile_handler(self, message):
        if UserRepository().exists(message.from_user.id):
            user = UserRepository().get(message.from_user.id)
            text = (
                "Profile: \n"+f"First Name: {user['firstName']}\nLast Name: {user['lastName']}\nPhone: {user['phone']}\nRole: {user['role']}\n")
            return text
            await message.answer(text=text)
        else:
            await message.answer("You don't have a profile, please register first")

    async def share_location_handler(self, message):
        if UserRepository().exists(message.from_user.id):
            self.userJson = UserRepository().get(message.from_user.id)
            id = self.userJson["id"]
            username = self.userJson["username"]
            firstName = self.userJson["firstName"]
            lastName = self.userJson["lastName"]
            phone = self.userJson["phone"]
            role = self.userJson["role"]
            rides_requested = self.userJson["rides_requested"]
            rides_completed = self.userJson["rides_completed"]
            current_location = str(message.location)
            self.userJson = self.user.update_profile(
                id, username, firstName, lastName, phone, role, rides_requested, rides_completed, current_location)
            UserRepository().set(self.user.id, self.userJson)
            self.time = random.randint(5, 200)
            self.fee = random.randint(self.time, 500)
            await message.answer(f"Estimated time: {self.time} \n Estimated Fee: {self.fee} \n Finding your driver... ⌛️🚗 \nYou will be notified when we get a driver")
        else:
            await message.answer("You don't have a profile, please register first")

    async def save_ride_history(self, passenger_id, driver_id, current_time):
        if UserRepository().exists(driver_id):
            self.userJson = UserRepository().get(driver_id)
            id = self.userJson["id"]
            Driverusername = self.userJson["username"]
            DriverfirstName = self.userJson["firstName"]
            lastName = self.userJson["lastName"]
        if UserRepository().exists(passenger_id):
            self.userJson = UserRepository().get(passenger_id)
            print(self.userJson)
            id = self.userJson["id"]
            username = self.userJson["username"]
            firstName = self.userJson["firstName"]
            lastName = self.userJson["lastName"]
            phone = self.userJson["phone"]
            role = self.userJson["role"]
            rides_requested = self.userJson["rides_requested"]
            rides_completed = self.userJson["rides_completed"]
            current_location = None
            if "current_location" in self.userJson:
                current_location = self.userJson["current_location"]
            self.infoJson = User.ride_history(
                User, passenger_id, Driverusername, current_time, current_location)
            rides_completed.append(json.dumps(self.infoJson))
            self.userJson = self.user.update_profile(
                id, username, firstName, lastName, phone, role, rides_requested, rides_completed, current_location)
            UserRepository().set(self.user.id, self.userJson)

    async def show_history(self, message):
        if UserRepository().exists(message.from_user.id):
            self.userJson = UserRepository().get(message.from_user.id)
            id = self.userJson["id"]
            username = self.userJson["username"]
            firstName = self.userJson["firstName"]
            lastName = self.userJson["lastName"]
            phone = self.userJson["phone"]
            role = self.userJson["role"]
            rides_requested = self.userJson["rides_requested"]
            rides_completed = self.userJson["rides_completed"]
            return rides_completed
