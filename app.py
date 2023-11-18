import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from telegram import Bot

from main import RTVWatcher, iSpotWatcher

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
chat_id = '386062027' # You should first send a message to your bot and record your chat_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_availability()
    yield


app = FastAPI(lifespan=lifespan)


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

    is_available = any(result[0] for result in results[:2])

    message = f"{'✅ AVAILABLE' if is_available else '❌ NOT AVAILABLE'}\n\n"
    for index, result in enumerate(results):
        if index == 2:
            message += '\n---\n\n'
        message += f"{'✅' if result[0] else '❌'} {result[1].url}\n"

    await bot.send_message(chat_id, message, disable_notification=not is_available)
