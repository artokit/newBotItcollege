from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

created_program = InlineKeyboardBuilder()
created_program.row(InlineKeyboardButton(text='✅Text me📲', url='https://t.me/rufus_money'))
created_program.row(InlineKeyboardButton(text='✅Reviews🤑', callback_data='reviews'))
created_program.row(InlineKeyboardButton(text='💸Get money now💸', url='https://t.me/rufus_money'))
