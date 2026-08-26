import os
import asyncio
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
import uvicorn
import threading

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

# Главное меню с категориями
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✂️ Стрижки и укладка", callback_data="haircuts")
    builder.button(text="🧔 Борода и бритье", callback_data="beard")
    builder.button(text="💆‍♂️ Доп. услуги и уход", callback_data="additional")
    builder.button(text="🔥 Комбо-наборы", callback_data="combos")
    builder.button(text="📍 Контакты и адрес", callback_data="contacts")
    builder.button(text="📅 Записаться", callback_data="start_booking")
    builder.adjust(1)
    return builder.as_markup()

# Кнопка возврата в меню
def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад в меню", callback_data="back_to_menu")
    return builder.as_markup()

# Тексты разделов
HAIRCUTS_TEXT = (
    "✂️ Мужские стрижки и уход:\n\n"
    "• Мужская стрижка — от 2500\n"
    "• Стрижка машинкой — 2000\n"
    "• Стрижка машинкой (1-2 насадки) — от 1400\n"
    "• Детская стрижка — 2000\n"
    "• Укладка — 600\n"
    "• Окантовка — 700\n"
    "• Тонирование головы — от 1200\n"
    "• Моделирование головы — от 1500\n"
    "• Бритье головы — 1100"
)

BEARD_TEXT = (
    "🧔 Борода и бритье:\n\n"
    "• Стрижка бороды и усов (до 6мм) — 2000\n"
    "• Окантовка бороды — 700\n"
    "• Моделирование бороды + окантовка — 3500\n"
    "• Камуфляж бороды — от 1000\n"
    "• Бритье начисто шейвером — 2000\n"
    "• Бритье лица или головы — 3500\n"
    "• Бритье шейвером лица и головы — 2500"
)

ADDITIONAL_TEXT = (
    "💆‍♂️ Дополнительные услуги и уход:\n\n"
    "• Массаж головы\n"
    "• Детокс кожи головы — 1500\n"
    "• Удаление нежелательных волос — от 500\n"
    "• Уход за лицом DEPOT — 3500\n"
    "• Уход за лицом Volcano — 1500"
)

COMBO_TEXT = (
    "🔥 Выгодные комплексы:\n\n"
    "• Стрижка + уход за лицом Volcano — 3500\n"
    "• Стрижки + detox для кожи головы — 3500\n"
    "• Стрижка головы + бороды + Volcano — 4700\n"
    "• Мужская стрижка + моделирование бороды — 5400\n"
    "• Моделирование бороды + окантовка — 3500"
)

CONTACTS_TEXT = (
    "📍 «Je ton Barber shop» 💈\n\n"
    "▫️ Адрес: Нахимовский проспект, 50\n"
    "▫️ График работы: Ежедневно с 10:00 до 22:00\n"
    "▫️ Телефон: +7 929 963-3487"
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в Je ton Barber shop! 💈\nВыберите интересующий раздел:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "haircuts")
async def show_haircuts(callback: types.CallbackQuery):
    await callback.message.edit_text(HAIRCUTS_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "beard")
async def show_beard(callback: types.CallbackQuery):
    await callback.message.edit_text(BEARD_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "additional")
async def show_additional(callback: types.CallbackQuery):
    await callback.message.edit_text(ADDITIONAL_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "combos")
async def show_combos(callback: types.CallbackQuery):
    await callback.message.edit_text(COMBO_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "contacts")
async def show_contacts(callback: types.CallbackQuery):
    await callback.message.edit_text(CONTACTS_TEXT, reply_markup=get_back_keyboard(), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "start_booking")
async def start_booking(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📅 Онлайн-запись:\n\nДля записи позвоните нам по номеру:\n📞 +7 929 963-3487\n\nИли приходите по адресу: Нахимовский проспект, 50",
        reply_markup=get_back_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Главное меню Je ton Barber shop 💈\nВыберите интересующий раздел:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    
    server_thread = threading.Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=port),
        daemon=True
    )
    server_thread.start()
    
    asyncio.run(main())