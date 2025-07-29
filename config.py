import os
from dotenv import load_dotenv
load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
CRYPTOBOT_API_KEY = os.getenv('CRYPTOBOT_API_KEY')
SUPPORT_CHAT_ID = int(os.getenv('SUPPORT_CHAT_ID'))
SENTRY_DSN = os.getenv('SENTRY_DSN')
