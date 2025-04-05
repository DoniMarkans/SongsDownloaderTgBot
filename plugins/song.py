import os
import time
import requests
from yt_dlp import YoutubeDL
from pyrogram import filters, Client, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Путь к файлу cookies
COOKIES_FILE = "cookies.txt"

## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply(
        "𝐈'𝐦 𝐡𝐞𝐥𝐩𝐢𝐧𝐠 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐲𝐨𝐮𝐫 𝐥𝐨𝐯𝐞𝐥𝐲 𝐬𝐨𝐧𝐠𝐬 𝐨𝐧 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦🎸🎸🎸.\n"
        "𝐒𝐞𝐧𝐝 𝐦𝐞 𝐚 𝐘𝐨𝐮𝐭𝐮𝐛𝐞 𝐥𝐢𝐧𝐤 𝐭𝐨 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐭𝐡𝐞 𝐚𝐮𝐝𝐢𝐨 𝐢𝐧 𝐭𝐡𝐞 𝐛𝐞𝐬𝐭 𝐪𝐮𝐚𝐥𝐢𝐭𝐲!",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝐔𝐩𝐝𝐚𝐭𝐞𝐬 𝐂𝐡𝐚𝐧𝐧𝐞𝐥🔔', url='https://t.me/Updates_of_ElizaBot'),
                    InlineKeyboardButton('𝐒𝐮𝐩𝐩𝐨𝐫𝐭', url='https://t.me/ElizaSupporters')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['help']))
async def help(client, message):
    await message.reply(
        "<b>𝐇𝐨𝐰 𝐭𝐨 𝐮𝐬𝐞 𝐦𝐞:</b>\n"
        "1. 𝐒𝐞𝐧𝐝 𝐚 𝐘𝐨𝐮𝐭𝐮𝐛𝐞 𝐥𝐢𝐧𝐤 (e.g., <code>https://www.youtube.com/watch?v=dQw4w9WgXcQ</code>).\n"
        "2. 𝐈'𝐥𝐥 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐚𝐧𝐝 𝐬𝐞𝐧𝐝 𝐭𝐡𝐞 𝐚𝐮𝐝𝐢𝐨 𝐢𝐧 𝐭𝐡𝐞 𝐛𝐞𝐬𝐭 𝐪𝐮𝐚𝐥𝐢𝐭𝐲!",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Developer', url='https://t.me/SehathSanvidu')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['about']))
async def about(client, message):
    await message.reply(
        "➪<b>Name</b> : ✫<i>Song Downloader</i>\n"
        "➪<b>Developer</b> : ✫[SehathPerera](https://t.me/SehathSanvidu)\n"
        "➪<b>Language</b> : ✫<i>Python3</i>\n"
        "➪<b>Server</b> : ✫[𝘏𝘦𝘳𝘰𝘬𝘶](https://heroku.com/)\n"
        "➪<b>Source Code</b> : ✫[𝘊𝘭𝘪𝘤𝘬 𝘏𝘦𝘳𝘦](https://github.com/PereraSehath)",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Support', url='https://t.me/ElizaSupporters')
                ]
            ]
        )
    )

@Client.on_message(filters.regex(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'))
async def download_audio(client, message):
    url = message.text.strip()
    m = await message.reply('🔎 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐘𝐨𝐮𝐭𝐮𝐛𝐞 𝐥𝐢𝐧𝐤...')

    # Настройки для yt_dlp: лучшее качество аудио с cookies
    ydl_opts = {
        'format': 'bestaudio/best',  # Скачиваем лучшее доступное аудио
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Извлекаем аудио с помощью FFmpeg
            'preferredcodec': 'mp3',      # Конвертируем в mp3
            'preferredquality': '192',    # Качество 192 kbps (можно настроить)
        }],
        'outtmpl': 'audio_%(id)s.%(ext)s',  # Имя файла
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,  # Используем cookies, если файл существует
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Извлекаем информацию о видео
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            duration = info_dict.get('duration', 0)  # В секундах
            views = info_dict.get('view_count', 0)
            thumbnail = info_dict.get('thumbnail', None)
            audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')  # Учитываем конвертацию

            # Скачиваем аудио
            await m.edit("`𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐮𝐝𝐢𝐨...`")
            ydl.process_info(info_dict)

        # Скачиваем миниатюру, если есть
        thumb_name = f'thumb{message.message_id}.jpg'
        if thumbnail:
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
        else:
            thumb_name = None

        # Формируем подпись
        rep = (
            f'🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({url})\n'
            f'⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : `{time.strftime("%M:%S", time.gmtime(duration))}`\n'
            f'👀 𝐕𝐢𝐞𝐰𝐬 : `{views:,}`\n\n'
            f'📮 𝗕𝘆: {message.from_user.mention()}\n'
            f'📤 𝗕𝘆 : @AnnieElizaSongDT_Bot'
        )

        # Отправляем аудио
        await m.edit("`𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐭𝐨 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦...`")
        await message.reply_audio(
            audio_file,
            caption=rep,
            parse_mode='HTML',
            quote=False,
            title=title,
            duration=duration,
            performer="Downloaded by bot",
            thumb=thumb_name
        )
        await m.delete()

    except Exception as e:
        await m.edit(f'𝐅𝐚𝐢𝐥𝐞𝐝: `{str(e)}`\n\n`𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐡𝐞𝐜𝐤 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤 𝐚𝐧𝐝 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧.`')
        print(e)

    # Очистка временных файлов
    try:
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if thumb_name and os.path.exists(thumb_name):
            os.remove(thumb_name)
    except Exception as e:
        print(f"Error cleaning up: {e}")
