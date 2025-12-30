import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

API_TOKEN = os.getenv("8520007457:AAH7IOdl9obVeZbDU5vdH0Hd2AXXAYqOQ-U")  # توکن از محیط می‌خونه

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

waiting_users = set()
connections = {}

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🔗 چت ناشناس با یکی!", callback_data="find_partner")],
        [InlineKeyboardButton("❓ راهنما", callback_data="help")]
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "😈 سلام ای موجود ناشناس!\n\n"
        "اینجا می‌تونی با یکی چت کنی بدون اینکه بدونه تو کی هستی... و اونم نمی‌دونه تو کی هستی!\n"
        "فقط یادت باشه، اینجا فقط حال کنیم، کسی رو ناراحت نکن وگرنه خودم میام سراغت 😉\n\n"
        "دکمه زیر رو بزن تا یکی پیدا کنیم برات!",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data == "help")
async def help_callback(call: types.CallbackQuery):
    await call.message.edit_text(
        "📌 راهنما:\n\n"
        "🔗 چت ناشناس با یکی! → یه نفر تصادفی پیدا می‌کنم برات\n"
        "هر چی بنویسی، ناشناس براش می‌ره\n"
        "اونم هر چی جواب بده، برات میاد\n"
        "هر وقت خواستی بزن /stop\n\n"
        "⚠️ فقط حال کن، فوش سنگین نده، تهدید نکن، آزار نده... وگرنه خودم بلاکت می‌کنم 😏",
        reply_markup=get_main_keyboard()
    )
    await call.answer()

@dp.callback_query(F.data == "find_partner")
async def find_partner(call: types.CallbackQuery):
    user_id = call.from_user.id
    if user_id in connections:
        await call.answer("تو همین الان داری با یکی چت می‌کنی پدرسگ 😏", show_alert=True)
        return
    if user_id in waiting_users:
        await call.answer("داریم دنبال یکی می‌گردیم برات، صبور باش لعنتی!", show_alert=True)
        return
    waiting_users.add(user_id)
    await call.message.edit_text("🔍 دارم دنبال یه آدم باحال می‌گردم برات...\nیه لحظه صبر کن ای جوون!")
    partner = next((w for w in list(waiting_users) if w != user_id), None)
    if partner:
        connections[user_id] = partner
        connections[partner] = user_id
        waiting_users.remove(user_id)
        waiting_users.remove(partner)
        await bot.send_message(user_id, "😈 پیدات کرد یه آدم مرموز! حالا هر چی بنویسی، ناشناس براش می‌ره...\nبرو حالشو ببر، فقط زیادی شیطونی نکن ها 😉")
        await bot.send_message(partner, "😈 یه آدم ناشناس پیدات کرد! داره باهات چت می‌کنه...\nهر چی جواب بدی، براش می‌ره. حال بده ولی زیادی گند نزن 😏")
        await call.answer("اتصال برقرار شد! 🔥")
    else:
        await call.answer("در انتظار یه آدم باحال... صبر کن!")

@dp.message(Command("stop"))
async def stop(message: types.Message):
    user_id = message.from_user.id
    if user_id in connections:
        partner = connections[user_id]
        del connections[user_id]
        if partner in connections:
            del connections[partner]
        await bot.send_message(partner, "💔 اوه... طرف مقابلت ترسید و در رفت 😭\nشاید دفعه بعد شجاع‌تر باشی!")
        await message.answer("🔌 چت قطع شد! امیدوارم حالشو برده باشی ای شیطون 😈")
    else:
        await message.answer("هیچ چتی نداری که قطع کنی ای خالی‌بند 😏")

@dp.message()
async def relay_message(message: types.Message):
    user_id = message.from_user.id
    if user_id in connections:
        target_id = connections[user_id]
        try:
            await message.send_copy(chat_id=target_id)
        except:
            await message.answer("❌ طرف بلاکت کرده یا مشکلی پیش اومد. چت تموم شد.")
            if target_id in connections:
                del connections[target_id]
            del connections[user_id]
    else:
        await message.answer("اول دکمه 🔗 چت ناشناس رو بزن تا یکی پیدا کنیم برات!", reply_markup=get_main_keyboard())

async def main():
    print("بات ناشناس شیطون داره استارت می‌خوره 😈")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
