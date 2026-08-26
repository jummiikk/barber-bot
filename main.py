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

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✂️ Услуги", callback_data="services")
    builder.button(text="📅 Записаться", callback_data="start_booking")
    builder.button(text="📍 Контакты", callback_data="contacts")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в наш барбершоп!", reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "services")
async def show_services(callback: types.CallbackQuery):
    await callback.message.edit_text("✂️ Наши услуги и цены...", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "contacts")
async def show_contacts(callback: types.CallbackQuery):
    await callback.message.edit_text("📍 Мы находимся в г. Майлуу-Суу...", reply_markup=get_main_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "start_booking")
async def start_booking(callback: types.CallbackQuery):
    await callback.message.edit_text("📅 Онлайн-запись в разработке.", reply_markup=get_main_keyboard())
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