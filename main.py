import logging
from aiogram import Bot, Dispatcher, executor, types

from Database.config import ConfigTelebot
from message_builder import Director

bot = Bot(token=ConfigTelebot().api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='test')
async def test_msg(message: types.Message):
    await message.answer('Test message')

@dp.callback_query_handler(text='add')
async def add_new_person(call: types.CallbackQuery):
    data = Director(call.message).create_answer_to_add_commands(call)
    await bot.send_message(data._id.chat_id, data._quest.question)

@dp.message_handler(commands='start')
async def asnwer_to_start_command(message: types.Message):
    data = Director(message).create_answer_to_start_msg()
    await bot.send_message(data._id.chat_id, data._quest.question)

@dp.message_handler(content_types=['text'])
async def answer_to_text_message(message: types.Message):
    try:
        data = Director(message).choice_answer_to_text_message()
        keyboard = types.InlineKeyboardMarkup()
        KeyboardExtender(keyboard, data._dia.dialogs_list)
        await bot.send_message(data._id.chat_id, data._quest.question, reply_markup=keyboard)
    except ValueError:
        await message.answer('Введены неверные данные')

@dp.callback_query_handler()
async def answer_to_inline_btn_command(call: types.CallbackQuery):
    data = Director(call.message).choice_answer_to_not_named_inline_command(call)
    keyboard = types.InlineKeyboardMarkup()
    KeyboardExtender(keyboard, data._dia.dialogs_list)
    await bot.send_message(data._id.chat_id, data._quest.question, reply_markup=keyboard)


class KeyboardExtender:
    def __init__(self, keyboard, dialog_obj_list: list) -> None:
        self.keyboard = keyboard
        self.dialog_obj_list = dialog_obj_list
        self.extend_keyboard()

    def extend_keyboard(self) -> None:
        if self.dialog_obj_list:
            for dialog in self.dialog_obj_list:
                if dialog.emoji:
                    self.keyboard.add(types.InlineKeyboardButton(text=dialog.dialog + '  ' + dialog.emoji,
                                                                 callback_data=dialog.commands))
                else:
                    self.keyboard.add(types.InlineKeyboardButton(text=dialog.dialog,
                                                                 callback_data=dialog.commands))
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
