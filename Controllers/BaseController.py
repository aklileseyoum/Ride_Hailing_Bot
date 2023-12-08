from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton
)

class BaseController:   

    def __init__(self, html) -> None:
        self.html = html
        self.ReplyKeyboardMarkup = ReplyKeyboardMarkup
        self.Message = Message
        self.KeyboardButton = KeyboardButton
        self.InlineKeyboardButton = InlineKeyboardButton