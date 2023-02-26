import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint

bot = Bot(token="")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class CaptchaStates(StatesGroup):
    captcha = State()

async def send_captcha(message: types.Message, state: FSMContext):
    num1 = randint(1, 10)
    num2 = randint(1, 10)

    op = randint(1, 3)
    if op == 1:
        op_str = "+"
        result = num1 + num2
    elif op == 2:
        op_str = "-"
        result = num1 - num2
    else:
        op_str = "*"
        result = num1 * num2

    await message.answer(f"Решите пример: {num1} {op_str} {num2} = ?")

    await CaptchaStates.captcha.set()
    await state.update_data(result=result)

@dp.message_handler(state=CaptchaStates.captcha)
async def check_captcha(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    result = data.get("result")

    if answer.isdigit() and int(answer) == result:
        await state.finish()
        await message.answer("Проверка пройдена!")
    else:
        await send_captcha(message, state)

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет")
    await send_captcha(message, state)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
