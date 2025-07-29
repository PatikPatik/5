from telegram import Update
from telegram.ext import ContextTypes
import models
from utils import get_translator

async def balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    _ = get_translator(u.language)
    text = _("Your balance: {balance} USDT\nYour hashpower: {hashpower} TH/s").format(
        balance=u.balance, hashpower=u.hashpower
    )
    await update.message.reply_text(text)
