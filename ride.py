import asyncio
import logging
import sys
from typing import Any, Dict
import datetime
import json

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, F, Router, html, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from os import getenv

from dotenv import load_dotenv


from Controllers.BaseController import BaseController
from Controllers.UserController import UserController
from Repositories.UserRepository import UserRepository
from Repositories.BaseRepository import BaseRepository


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

router = Router()
baseController = BaseController(html)
userController = UserController(html)


class Contact(StatesGroup):
    contact = State()
    role = State()


class Profile(StatesGroup):
    update = State()
    updateFirstName = State()
    updateLastName = State()
    updatePhone = State()
    updateRole = State()


class Options(StatesGroup):
    option = State()
    mainMenu = State()
    mainMenuDriver = State()
    UpdateProfile = State()


class Location(StatesGroup):
    currentLocation = State()
    destination = State()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await userController.start_handler(message)
    await state.set_state(Contact.contact)


@router.message(Contact.contact)
async def handle_contact_message(message: Message, state: FSMContext):
    await state.set_state(Contact.role)
    await userController.handle_contact_message(message)


@router.message(Contact.role)
async def role_handler(message: Message, state: FSMContext):
    data = await state.update_data(role=message.text)
    await state.set_state(Options.option)
    await userController.role_handler(message)
    if data['role'] == 'Passenger':
        await main_menu_handler(message, state)
    else:
        await main_menu_handler_driver(message, state)


@router.message(Options.mainMenu)
async def main_menu_handler(message: Message, state: FSMContext):
    await message.answer("Welcome to the main menu!",
                         reply_markup=ReplyKeyboardMarkup(
                             resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton(
                                         text="Profile", callback_data="profile"),
                                     KeyboardButton(text=" Order Ride",
                                                    callback_data="order_ride"),
                                     KeyboardButton(text="Ride History",
                                                    callback_data="ride_history"),
                                 ]
                             ],
                         ),
                         )


@router.message(Options.mainMenuDriver)
async def main_menu_handler_driver(message: Message, state: FSMContext):
    await message.answer("Welcome to the main menu!",
                         reply_markup=ReplyKeyboardMarkup(
                             resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton(
                                         text="Profile", callback_data="profile"),
                                     KeyboardButton(text="Ride History",
                                                    callback_data="ride_history"),
                                 ]
                             ],
                         ),
                         )


@router.message(Profile.update)
async def update_firstName(message: Message, state: FSMContext):
    await state.set_state(Profile.updateFirstName)
    await message.reply("Please enter your first name",  reply_markup=ReplyKeyboardRemove())


@router.message(Profile.updateFirstName)
async def update_lastName(message: Message, state: FSMContext):
    await state.update_data(firstName=message.text)
    await state.set_state(Profile.updateLastName)
    await message.answer("Please enter your last name")


@router.message(Profile.updateLastName)
async def update_phone(message: Message, state: FSMContext):
    await state.update_data(lastName=message.text)
    await state.set_state(Profile.updatePhone)
    await message.answer("Please enter your phone number")


@router.message(Profile.updatePhone)
async def update_role(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Profile.updateRole)
    await message.answer("Please enter your role",
                         reply_markup=ReplyKeyboardMarkup(
                             resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton(text="Driver"),
                                     KeyboardButton(text="Passenger"),
                                 ]
                             ],
                         ),
                         )


@router.message(Profile.updateRole)
async def update_profile(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    data = await state.get_data()
    await userController.update_profile_handler(message, data)
    if data['role'] == "Driver":
        await main_menu_handler_driver(message, state)
        await state.set_state(Options.option)
    elif data['role'] == "Passenger":
        await main_menu_handler(message, state)
        await state.set_state(Options.option)
    else:
        message.text = data['phone']
        await update_role(message, state)
        # await update_firstName(message, state)


@router.message(Options.option)
async def option_handler(message: Message, state: FSMContext):
    if message.text == "Profile":
        await state.set_state(Options.UpdateProfile)
        data = await userController.get_profile_handler(message)
        await message.answer(text=data, reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text="Update Profile"),
                    KeyboardButton(text="Back to main menu"),
                ]
            ]
        ))
    elif message.text == "Order Ride":
        await state.set_state(Location.currentLocation)
        await message.answer("Share your location",
                             reply_markup=ReplyKeyboardMarkup(
                                 resize_keyboard=True,
                                 keyboard=[
                                     [
                                         KeyboardButton(text="Share Location",
                                                        request_location=True),
                                     ]
                                 ],
                             ),
                             )
        # return

    elif message.text == "Ride History":
        infoJson = await userController.show_history(message)
        text = ""
        for info in infoJson:
            changed = json.loads(info)
            text += f"Driver/Passenger: {changed['driver_id']}\nDate: {changed['date']}\nDestination: {changed['destination']}\n\n"

        await message.answer(text=text)


@router.message(Options.UpdateProfile)
async def update_profile_menu(message: Message, state: FSMContext):
    the_id = message.from_user.id
    info = BaseRepository().get(the_id)
    if message.text == "Update Profile":
        await state.set_state(Profile.update)
    else:
        if info['role'] == "Driver":
            await main_menu_handler_driver(message, state)
            await state.set_state(Options.option)
        else:
            await main_menu_handler(message, state)
            await state.set_state(Options.option)


@router.message(Location.currentLocation)
async def handle_location(message: Message, state: FSMContext):
    await state.set_state(Location.destination)
    await message.answer("Please enter your destination")

global found
found = False
lucky_drivers = set()


@router.message(Location.destination)
async def handle_location(message: Message, state: FSMContext):
    global user_id
    global user_info
    global found
    user_id = message.from_user.id
    user_info = message.from_user
    await state.set_state(Options.option)
    await userController.share_location_handler(message)
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Accept", callback_data="accept")
    keyboard.button(text="Reject", callback_data="reject")
    for driver in UserRepository().get_drivers():
        await bot.send_message(chat_id=driver['id'], text="There's a passenger waiting for a ride. Are you available to be their driver?", reply_markup=keyboard.as_markup())
        if found:
            break

    await main_menu_handler(message, state)


@router.callback_query(lambda c: c.data in ["accept", "reject"])
async def accepted_ride(callback_query: types.CallbackQuery):
    global found
    global user_id
    global user_info
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    lucky_drivers.add(callback_query.from_user.id)
    if "accept" == callback_query.data and not found:
        found = True
        for driver in UserRepository().get_drivers():
            if driver['id'] not in lucky_drivers:
                await bot.send_message(chat_id=driver['id'], text="Apologies, but the passenger has been matched with another driver. Thanks for your response, and we appreciate your willingness to help. Feel free to stay tuned for future ride opportunities. Drive safely!")
            else:
                phone_no = driver['phone']
                await bot.send_message(chat_id=driver['id'], text=f"Your passenger is {user_info.first_name} He/She will contact you shortly")
                current_time = datetime.datetime.now()
                await userController.save_ride_history(user_id, driver['id'], str(current_time))
                await userController.save_ride_history(driver['id'], user_id, str(current_time))
        await bot.send_message(chat_id=user_id, text=f"🌟 Your ride request has been accepted by a driver. Here are their contact details: \nDriver's Name: {callback_query.from_user.first_name} \nContact Number:{phone_no} \nFeel free to reach out to coordinate your ride. Safe travels!")
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Your decision to decline is noted. Thank you for your response! If you change your mind or have any questions, feel free to reach out. Drive safe!")


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
