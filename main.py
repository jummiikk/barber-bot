import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

# Загружаем токен
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Функция создания главного меню с кнопками
def get_main_keyboard():
  builder = InlineKeyboardBuilder()
  builder.button(text="✂️ Наши услуги и цены", callback_data="services")
  builder.button(text="📅 Записаться онлайн", callback_data="booking")
  builder.button(text="📍 О нас и контакты", callback_data="contacts")
  builder.adjust(1)  
  return builder.as_markup()


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  welcome_text = (
      "👋 Добро пожаловать в наш барбершоп!\n\nЗдесь вы можете узнать цены,"
      " записаться к мастеру или посмотреть контакты.\nВыберите нужный пункт"
      " меню ниже:"
  )
  await message.answer(welcome_text, reply_markup=get_main_keyboard())


# Обработка нажатия на кнопки меню
@dp.callback_query(F.data == "services")
async def show_services(callback: types.CallbackQuery):
  services_text = (
      "✂️ Наши услуги:\n\n1. Мужская стрижка — 1000 сом\n2. Стрижка бороды —"
      " 600 сом\n3. Комплекс (стрижка + борода) — 1500 сом\n4. Детская стрижка"
      " — 800 сом"
  )
  await callback.message.edit_text(
      services_text, reply_markup=get_main_keyboard(), parse_mode="Markdown"
  )
  await callback.answer()


@dp.callback_query(F.data == "contacts")
async def show_contacts(callback: types.CallbackQuery):
  contacts_text = (
      "📍 Мы находимся:\nг. Майлуу-Суу, ул. Центральная, 15\n\n⏰"
      " Режим работы:\nЕжедневно с 10:00 до 20:00\n\n📞 Телефон для связи:"
      " +996 (...)"
  )
  await callback.message.edit_text(
      contacts_text, reply_markup=get_main_keyboard(), parse_mode="Markdown"
  )
  await callback.answer()


@dp.callback_query(F.data == "booking")
async def start_booking(callback: types.CallbackQuery):
  await callback.message.edit_text(
      "📅 Функция онлайн-записи в разработке!\nСкоро здесь можно будет выбрать"
      " мастера и время.",
      reply_markup=get_main_keyboard(),
  )
  await callback.answer()


# Главная функция запуска
async def main():
  print("Бот барбершопа запущен...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())