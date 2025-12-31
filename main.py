import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

# Вставь свой токен здесь
API_TOKEN = '8258664382:AAFjkg6U-TInnaXEtpfXaiqcgZ0zS0nlYQs'
# Ссылка на твой Mini App (которую ты получишь от Vercel)
APP_URL = 'https://vibeid-project.vercel.app'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 1. Приветствие и кнопка открытия приложения
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    kb = [
        [types.InlineKeyboardButton(text="🚀 Открыть VibeID", web_app=types.WebAppInfo(url=APP_URL))],
        [types.InlineKeyboardButton(text="💎 Купить Premium (50 ⭐)", callback_data="buy_premium")]
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в **VibeID** — сервис для создания твоих уникальных виджетов.\n\n"
        "Нажми кнопку ниже, чтобы начать!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# 2. Выставление счета на "Звезды"
@dp.callback_query(lambda c: c.data == 'buy_premium')
async def process_buy_premium(callback_query: types.CallbackQuery):
    await bot.send_invoice(
        chat_id=callback_query.from_user.id,
        title="VibeID Premium",
        description="Разблокируй все неоновые темы и убери водяной знак!",
        payload="premium_payload",
        currency="XTR",  # Код для Telegram Stars
        prices=[LabeledPrice(label="Premium", amount=50)], # 50 звезд
        start_parameter="premium_upgrade"
    )

# 3. Подтверждение готовности к оплате
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 4. Успешная оплата
@dp.message(lambda message: message.successful_payment is not None)
async def successful_payment(message: types.Message):
    await message.answer("🎉 Ура! Оплата прошла успешно. Твой Premium активирован!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())

