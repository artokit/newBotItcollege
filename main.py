import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import os
from aiogram.types.input_file import FSInputFile
from aiogram.utils import markdown
from aiogram.utils.media_group import MediaGroupBuilder

import db_api
import keyboards

MEDIA_PATH = os.path.join(os.path.dirname(__file__), 'media')
dp = Dispatcher()
bot = Bot('6826234001:AAH1m9pSIQMzzjsq_RJ5zztsK0XbsHCItxo')


@dp.message(Command('start'))
async def start(message: Message):
    db_api.add_sender(message.chat.id)

    await message.answer_photo(
        photo=FSInputFile(os.path.join(MEDIA_PATH, 'start.png')),
    )
    await message.answer(
        'Hello, my name is Rufus Chogo and I\'m a programmer.✌️\n\n'
        'My students have already been able to earn money to buy new cars😎'
    )
    await asyncio.sleep(5)

    await message.answer_video(FSInputFile(os.path.join(MEDIA_PATH, 'start.mp4')))
    await message.answer_video(FSInputFile(os.path.join(MEDIA_PATH, 'start2.mp4')))

    await message.answer(
        'I created a program in the Lucky Jet/Aviator game that predicts the next coefficient🛫.\n\n'

        'Using my program.\n'
        '1⃣thousand dollars you can win TODAY!\n\n'
        
        'But there\'s one condition!\n\n'
        
        'Text me and I\'ll give you the program for FREE.\n\n'

        '👉 https://t.me/rufus_money 👈',
        reply_markup=keyboards.created_program.as_markup()
    )

    await asyncio.sleep(5)
    link = markdown.hlink(message.chat.first_name, f'tg://resolve?domain={message.chat.username}')
    await message.answer(
        f'{link} your bot\'s ready, text me right now👇\n\n'
        'https://t.me/rufus_money',
        parse_mode='html'
    )


@dp.callback_query(F.data == 'reviews')
async def get_reviews(call: CallbackQuery):
    media_group = MediaGroupBuilder()

    for i in range(1, 6):
        media_group.add_photo(media=FSInputFile(os.path.join(MEDIA_PATH, f'comment{i}.png')))

    await call.message.answer_media_group(media=media_group.build())
    await call.message.answer(
        'text me "HELP" right now\n\n'
        '👇👇👇👇👇👇👇👇👇\n\n'
        'https://t.me/rufus_money'
    )


asyncio.run(dp.start_polling(bot))
