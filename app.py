from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from telegram import Bot
from main import RTVWatcher, iSpotWatcher
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
chat_id = '386062027'


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_availability()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
@repeat_every(seconds=60*30)  # 30 minutes
async def check_availability():
    websites = [
        RTVWatcher(
            'https://www.euro.com.pl/telefony-komorkowe/apple-iphone-15-pro-256gb-silver.bhtml'),
        RTVWatcher(
            'https://www.euro.com.pl/telefony-komorkowe/apple-iphone-15-pro-256gb-gold.bhtml'),
        iSpotWatcher(
            'https://ispot.pl/apple-iphone-15-pro-256gb-white-titanium'),
        iSpotWatcher(
            'https://ispot.pl/apple-iphone-15-pro-256gb-natural-titanium'),
    ]

    results = []
    for website in websites:
        print(f'Checking availability on {website.url}')

        try:
            is_available = website.is_available()
            results.append((is_available, website))

        except Exception as e:
            await bot.send_message(chat_id, f'Error checking availability on {website.url}')

    is_available = any(result[0] for result in results)

    message = f"{'AVAILABLE' if is_available else 'NOT AVAILABLE'}\n\n"
    for result in results:
        message += f"{'✅' if result[0] else '❌'} {result[1].url}\n"

    await bot.send_message(chat_id, message)
