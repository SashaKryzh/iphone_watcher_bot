# iPhone Watcher Bot

A simple Telegram bot that checks iPhone availability in stores every 30 mins and sends a notification.

Run locally: `uvicorn app:app`

Deploy to Fly.io: `fly deploy --ha=false`. The first time, you might need to kill the second machine, because there is no reason for this bot to run on more than 1 machine.
