#!/usr/bin/env sh
python bot.py &
BOT_PID=$!
uvicorn health:app --host 0.0.0.0 --port ${PORT:-8000} &
UVICORN_PID=$!
wait $BOT_PID $UVICORN_PID
