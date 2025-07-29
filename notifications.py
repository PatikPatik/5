from datetime import time
from telegram.ext import ContextTypes, CommandHandler
import models, services.mining
from utils import get_translator

async def set_report_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    _ = get_translator(u.language)
    if len(context.args) != 1 or ':' not in context.args[0]:
        return await update.message.reply_text(_("Использование: /setreport HH:MM"))
    hh, mm = map(int, context.args[0].split(':'))
    u.report_time = (hh, mm)
    u.save()
    context.job_queue.run_daily(
        daily_report, time(hour=hh, minute=mm),
        context=user.id, name=str(user.id)
    )
    await update.message.reply_text(_("Ежедневный отчёт на {}:{} установлен").format(hh, mm))

async def daily_report(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.context
    u = models.User[user_id]
    _ = get_translator(u.language)
    text = services.mining.get_daily_report(u)
    await context.bot.send_message(chat_id=user_id, text=_("Ваш ежедневный отчёт:
") + text)
