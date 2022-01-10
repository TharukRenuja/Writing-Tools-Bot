import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os
import requests
import requests as r
from htmlwebshot import WebShot
from PIL import Image, ImageDraw, ImageFont
from telegraph import upload_file as uf

Client = Client(
    "Writing-Tools",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
)

HELP_STRING = """
● Still Wonder How I Work ? 
● Use /write to Write on a paper
● Use /img2txt to Convert image to text
● Use /webshot to Create Webshot text
"""
ABOUT_STRING = """
● **BOT:** `Writing Tools Bot` 
● **CRETOR :** [Tharuk Renuja](https://t.me/TharukRenuja) 
● **SERVER :** `Azure` 
● **LIBRARY :** `Pyrogram` 
● **LANGUAGE :** `Python 3.9` 
● **Updates :** [SLBotsOfficial](https://t.me/SLBotsOfficial) 
"""
START_STRING = """ Hi {}, I'm Writing Tools Bot. 
 I Can Write Your Text on a Paper."""

START_BUTTON = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="Help❔",callback_data="cbhelp"),InlineKeyboardButton(text="About🤖",callback_data="cbabout")
                        ],
                        [
                            InlineKeyboardButton(text="Channel 📢",url="https://t.me/SLBotsofficial"),InlineKeyboardButton(text="Developer👦",url="https://t.me/TharukRenuja")
                        ]
                    ]
                )


@Client(pattern="write ?(/*)")
async def writer(e):
    if e.reply_to:
        reply = await e.get_reply_message()
        text = reply.message
    elif e.pattern_match.group(1):
        text = e.text.split(maxsplit=1)[1]
    else:
        return await eod(e, get_string("writer_1"))
    k = await eor(e, get_string("com_1"))
    img = Image.open("https://telegra.ph/file/6231b752af485850d80fb.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/assfont.ttf", 30)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getsize("hg")[1]
    for line in lines:
        draw.text((x, y), line, fill=(1, 22, 55), font=font)
        y = y + line_height - 5
    file = "ult.jpg"
    img.save(file)
    await e.reply(file=file)
    os.remove(file)
    await k.delete()
        
@Client.on_message(filters.command(["start"]) & filters.private)
async def start_private(bot, update):
    text = START_STRING.format(update.from_user.mention)
    reply_markup = START_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    
@Client.on_message(filters.command(["webshot"]) & filters.private)
async def f2i(e):
    txt = e.pattern_match.group(1)
    if txt:
        html = e.text.split(maxsplit=1)[1]
    elif e.reply_to:
        r = await e.get_reply_message()
        if r.media:
            html = await e.client.download_media(r.media)
        elif r.text:
            html = r.text
    else:
        return await eod(e, "`Either reply to any file or give any text`")
    html = html.replace("\n", "<br>")
    shot = WebShot(quality=85)
    css = "body {background: white;} p {color: red;}"
    pic = await shot.create_pic_async(html=html, css=css)
    try:
        await e.reply(file=pic)
    except BaseException:
        await e.reply(file=pic, force_document=True)
    os.remove(pic)
    if os.path.exists(html):
        os.remove(html)
        
@Client.on_message(filters.command(["img2txt"]) & filters.private)
async def ocrify(ult):
    if not ult.is_reply:
        return await eor(ult, "`Reply to Photo...`")
    msg = await eor(ult, "`Processing..`")
    OAPI = os.environ("OCR_API")
    if not OAPI:
        return await msg.edit(TE)
    pat = ult.pattern_match.group(1)
    repm = await ult.get_reply_message()
    if not (repm.media and repm.media.photo):
        return await msg.edit("`Not a Photo..`")
    dl = await repm.download_media()
    if pat:
        atr = f"&language={pat}&"
    else:
        atr = "&"
    tt = uf(dl)
    li = "https://telegra.ph" + tt[0]
    gr = r.get(
        f"https://api.ocr.space/parse/imageurl?apikey={OAPI}{atr}url={li}"
    ).json()
    trt = gr["ParsedResults"][0]["ParsedText"]
    await msg.edit(f"**🎉 IMG2TXT PORTAL\n\nRESULTS ~ ** `{trt}`")
    
@Client.on_message(filters.command(["help"]) & filters.private)
async def start_private(bot, update):
    text = HELP_STRING.format(update.from_user.mention)
    reply_markup = START_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )
    
@Client.on_message(filters.command(["about"]) & filters.private)
async def start_private(bot, update):
    text = ABOUT_STRING.format(update.from_user.mention)
    reply_markup = START_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )    
    
@Client.on_callback_query()
async def cb_data(bot, update):  
    if update.data == "cbhelp":
        await update.message.edit_text(
            text=HELP_STRING,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data == "cbabout":
        await update.message.edit_text(
            text=ABOUT_STRING,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    else:
        await update.message.edit_text(
            text=START_STRING.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTON
        )
        
Client.run()
