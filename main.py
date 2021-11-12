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

@dp.message_handler(commands='start')
async def test_msg(message: types.Message):
    data = Director(message).create_answer_to_start_msg()
    await bot.send_message(data._id.chat_id, data._quest.question)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
