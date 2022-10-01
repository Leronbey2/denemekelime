from pyrogram import Client
from pyrogram import filters
from random import shuffle
from pyrogram.types import Message
from kelime_bot import oyun
from kelime_bot.helpers.kelimeler import *
from kelime_bot.helpers.keyboards import *
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("➕ Gruba Ekle", url=f"http://t.me/inek_kelime_bot?startgroup=new")
    ],
    [
        InlineKeyboardButton("👤 Sahip", url="t.me/uslanmazmurti"),
        InlineKeyboardButton("🐄 Grubumuz", url="t.me/inekobasiTR"),
    ]
])


START = """
**⚔️ Merhaba, İnek Türet Bot'a Hoşgeldiniz Bot'u Gruba Ekleyerek Kelimeyi Türet Oyunu veya Kelime Anlatmaca Oynayabilirsiniz..**

➤ Yardım için 👉 /help Kullanın. Komutlar Gayet Kolaydır. 
"""

HELP = """
**📗 Komut Menüsüne Hoşgeldiniz.**
/bulmaca - Kelime Anlatma Oyunu Başlatır.
/ogretmen - Kelime Anlatma Oyununda Öğretmen Olma.. 
/puan - Oyuncular Arasındaki Rekabet Bilgisi..


/game - Kelime Türet oyunu başlatır.. 
/pass - Kelimeyi Atlar/Pas Geçer.
/skor - Oyuncular arasındaki Rekabet Bilgisi..
/cancel Kelime Türet Oyununu Bitirir.
"""

# Komutlar. 
@Client.on_message(filters.command("start"))
async def start(bot, message):
  await message.reply_photo("https://telegra.ph/file/d515a91bead7784328772.jpg",caption=START,reply_markup=keyboard)

@Client.on_message(filters.command("help"))
async def help(bot, message):
  await message.reply_photo("https://telegra.ph/file/3a177f6d7b5b5a3d0548f.jpg",caption=HELP) 

# Oyunu başlat. 
@Client.on_message(filters.command("game")) 
async def kelimeoyun(c:Client, m:Message):
    global oyun
    aktif = False
    try:
        aktif = oyun[m.chat.id]["aktif"]
        aktif = True
    except:
        aktif = False

    if aktif:
        await m.reply("**❗ Oyun Zaten Devam Ediyor \nOyunu Durdurmak İçin "/cancel" Kullanın")
    else:
        await m.reply(f"**{m.from_user.mention}** Komutuyla! \nKelime Bulma Oyunu Başlatıldı.\n\nİyi Oyunlar Sahip: @uslanmazmurti!", reply_markup=kanal)
        
        oyun[m.chat.id] = {"kelime":kelime_sec()}
        oyun[m.chat.id]["aktif"] = True
        oyun[m.chat.id]["round"] = 1
        oyun[m.chat.id]["pass"] = 0
        oyun[m.chat.id]["oyuncular"] = {}
        
        kelime_list = ""
        kelime = list(oyun[m.chat.id]['kelime'])
        shuffle(kelime)
        
        for harf in kelime:
            kelime_list+= harf + " "
        
        text = f"""
🎯 Raund : {oyun[m.chat.id]['round']}/60 
📝 Söz :   <code>{kelime_list}</code>
💰 Puanınız: 1
🔎 İpucu: 1. {oyun[m.chat.id]["kelime"][0]}
✍🏻 Uzunluk : {int(len(kelime_list)/2)} 

✏️ Karışık harflerden doğru kelimeyi bulun
        """
        await c.send_message(m.chat.id, text)
        
