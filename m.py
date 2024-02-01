from aiogram.utils.exceptions import ChatNotFound, MessageNotModified
from pyrogram import Client
from pyrogram import types
from aiogram import Bot
import os
import time
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import MessageEntityType
import asyncio

# Ключ - откуда копируем, значение - куда копируем.
CHANNELS = {
    '@AsirusChogobot': [6606885505],
    6694332070: [6606885505],
    # -1001254732707: [-1001625830919],  # prod
    # -1002117444687: [-1002037983867],  # test
    # -1002090503185: [-1002129378949]
    # -1001967661898: [-1002119649818] # test_parser
    # -1002146801058: [-1002045657627]
}

api_id = 11325071
api_hash = '8b7bd8121748973fcc1341afb5935b3b'
app = Client('anon', api_id=api_id, api_hash=api_hash)
TOKEN = '6840007780:AAEwr5_CXjhGAOT0Svu7wsbHOcr5BFXSF2Y'
bot = Bot(token=TOKEN)
DOWNLOADS = {}


async def edit_keyboard(msg, kb):
    await bot.edit_message_reply_markup(msg.chat.id, msg.id, reply_markup=kb)


def replace_sender(txt):
    if txt:
        return txt.replace(
            'X5GT',
            'X5PRO'
        ).replace(
            'AshokGold',
            'Ashok_help'
        ).replace(
            'X5CODER',
            'X5AR'
        ).replace(
            'TextMessageAidarbot',
            'AidarTextMebot'
        ).replace('https://1winis.click/XLK8xy', 'https://1winis.click/ashok')
    return txt


def replace_entities(ent):
    if not ent:
        return

    for i in ent:
        if i.type == MessageEntityType.TEXT_LINK:
            i.url = replace_sender(i.url)


def get_edit_copy_keyboard(keyboard):
    kb = InlineKeyboardMarkup()
    if keyboard:
        reply_markup = keyboard.inline_keyboard
        for i in reply_markup:
            button = i[0]
            kb.add(InlineKeyboardButton(text=button.text, url=replace_sender(button.url)))
    return kb


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.text)
async def post_text_handler(client: Client, message: types.Message):
    replace_entities(message.entities)
    kb = get_edit_copy_keyboard(message.reply_markup)
    await send_in_groups(client.send_message, message.chat.id, text=replace_sender(message.text),
                         entities=message.entities, kb=kb)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.media_group)
async def post_media_handler(client: Client, message: types.Message):
    length = len((await message.get_media_group()))
    res = await client.download_media(message)
    prev_res = DOWNLOADS.get(message.media_group_id, {}).get('res', [])
    prev_res.append([res, message.caption])
    DOWNLOADS[message.media_group_id] = {'length': length, 'res': prev_res}

    if DOWNLOADS[message.media_group_id]['length'] == len(prev_res):
        groups = []
        for i in DOWNLOADS[message.media_group_id]['res']:
            frmt = i[0][::-1].split('.')[0][::-1].lower()
            replace_entities(message.caption_entities)

            if frmt in ('jpg', 'png'):
                groups.append(types.InputMediaPhoto(i[0], caption=replace_sender(i[1]),
                                                    caption_entities=message.caption_entities))

            if frmt in ('mp4', 'avi', 'mov'):
                groups.append(types.InputMediaVideo(i[0], caption=replace_sender(i[1]),
                                                    caption_entities=message.caption_entities))

        await send_in_groups(client.send_media_group, message.chat.id, kb=False, media=groups)

        for i in DOWNLOADS[message.media_group_id]['res']:
            os.remove(i[0])

        del DOWNLOADS[message.media_group_id]


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.photo)
async def post_photo_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    kb = get_edit_copy_keyboard(message.reply_markup)
    replace_entities(message.caption_entities)
    with open(res, 'rb') as f:
        await send_in_groups(client.send_photo, message.chat.id, photo=f, caption=replace_sender(message.caption),
                             caption_entities=message.caption_entities, kb=kb)

    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.video)
async def post_video_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    kb = get_edit_copy_keyboard(message.reply_markup)
    dst = await client.download_media(message.video.thumbs[-1].file_id)
    replace_entities(message.caption_entities)
    await send_in_groups(client.send_video, message.chat.id, kb=kb,
                         video=res, caption=replace_sender(message.caption), width=message.video.width,
                         height=message.video.height, supports_streaming=message.video.supports_streaming,
                         thumb=dst, caption_entities=message.caption_entities)
    os.remove(dst)
    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.video_note)
async def post_video_note_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    kb = get_edit_copy_keyboard(message.reply_markup)
    await send_in_groups(client.send_video_note, message.chat.id, kb=kb, video_note=res)

    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.document)
async def post_document_handler(client: Client, message: types.Message):
    replace_entities(message.caption_entities)
    res = await client.download_media(message)
    kb = get_edit_copy_keyboard(message.reply_markup)
    await send_in_groups(client.send_document, message.chat.id, document=res, kb=kb,
                         caption=replace_sender(message.caption), caption_entities=message.caption_entities)
    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.animation)
async def post_animation_handler(client: Client, message: types.Message):
    replace_entities(message.caption_entities)
    res = await client.download_media(message)
    kb = get_edit_copy_keyboard(message.reply_markup)

    await send_in_groups(client.send_animation, message.chat.id, animation=res, kb=kb,
                         caption=replace_sender(message.caption), caption_entities=message.caption_entities)
    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.voice)
async def post_voice_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    kb = get_edit_copy_keyboard(message.reply_markup)
    await send_in_groups(client.send_voice, message.chat.id, voice=res, kb=kb,
                         caption=replace_sender(message.caption))
    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.sticker)
async def post_sticker_handler(client: Client, message: types.Message):
    kb = get_edit_copy_keyboard(message.reply_markup)
    await send_in_groups(client.send_sticker, message.chat.id, sticker=message.sticker.file_id, kb=kb)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.audio)
async def post_audio_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    replace_entities(message.caption_entities)
    kb = get_edit_copy_keyboard(message.reply_markup)
    await send_in_groups(client.send_audio, message.chat.id, kb=kb, audio=res, caption=replace_sender(message.caption),
                         caption_entities=message.caption_entities)
    os.remove(res)


# @app.on_message(filters=filters.chat(list(CHANNELS.keys())))
async def f(client: Client, message: types.Message):
    await client.send_message('@DenisErmoshin', 'что-то пошло по пизде :(')


async def send_in_groups(func, chat_copy_id, kb=True, **kwargs):
    for i in CHANNELS[chat_copy_id]:
        msg = await func(
            i,
            **kwargs
        )
        if kb:
            try:
                await edit_keyboard(msg, kb)
            except ChatNotFound:
                print("Добавьте бота в канал")
            except MessageNotModified:
                pass


async def get_last_post_id(chat_id):
    async for i in app.get_chat_history(chat_id, limit=1):
        return i.id


async def run():
    await app.start()
    print("Бот запущен")
    last_post_id_channels = {

    }

    for i in CHANNELS:
        last_post_id_channels[i] = await get_last_post_id(i)
        time.sleep(3)

    while True:
        for i in last_post_id_channels:
            time.sleep(3)

            current_last_post_id = await get_last_post_id(i)
            last_post_id = last_post_id_channels[i]

            if last_post_id != current_last_post_id:
                for msg_id in range(last_post_id + 1, current_last_post_id + 1):
                    try:
                        await post_message_to_channel(await app.get_messages(i, msg_id))

                    except Exception as e:
                        print(f"Ошибка в канале {i} сообщение {msg_id}: {str(e)}")

                    last_post_id_channels[i] = msg_id


async def post_message_to_channel(message: types.Message):
    if message.text:
        return await post_text_handler(app, message)

    if message.media:
        try:
            return await post_media_handler(app, message)
        except ValueError:
            pass

    if message.photo:
        return await post_photo_handler(app, message)

    if message.video:
        return await post_video_handler(app, message)

    if message.video_note:
        return await post_video_note_handler(app, message)

    if message.document:
        return await post_document_handler(app, message)

    if message.sticker:
        return await post_sticker_handler(app, message)

    if message.animation:
        return await post_animation_handler(app, message)

    if message.voice:
        return await post_voice_handler(app, message)


loop = asyncio.get_event_loop()
tasks = [loop.create_task(run())]
loop.run_until_complete(asyncio.wait(tasks))
# asyncio.run(run())
