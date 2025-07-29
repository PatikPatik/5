import logging
from datetime import time
from gettext import translation

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters, ContextTypes
)

import config
import models
import services.payments
import services.mining
import services.support
from utils import get_translator

ASK_QUESTION = 1

def main_menu_kb(_):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(_("Balance"), callback_data="BALANCE")],
        [InlineKeyboardButton(_("Buy Hashpower"), callback_data="BUY")],
        [InlineKeyboardButton(_("Refer a Friend"), callback_data="REFER")],
        [InlineKeyboardButton(_("Withdraw"), callback_data="WITHDRAW")],
    ])

def language_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    _ = get_translator(u.language or 'en')
    text = _(
        "☁️ Cloud Mining Bot\n\n"
        "Пополните баланс через @CryptoBot и приобретайте мощности.\n"
        "Зарабатывайте 20% в месяц, выплаты ежедневно.\n\n"
        "1 TH/s = 17 USDT\n"
        "Реферал: 1% от прибыли приглашённого"
    )
    await update.message.reply_markdown(text, reply_markup=main_menu_kb(_))

async def language_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Select language / Выберите язык:", reply_markup=language_kb()
    )

async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.callback_query.data.split('_')[1]
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    u.language = code
    u.save()
    _ = get_translator(code)
    await update.callback_query.edit_message_text(_("Language set."))

async def support_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    _ = get_translator(u.language)
    await update.message.reply_text(
        _("Опишите проблему:"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(_('Отмена'), callback_data='CANCEL')]
        ])
    )
    return ASK_QUESTION

async def support_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    req = services.support.create_request(user.id, text)
    await context.bot.send_message(
        chat_id=config.SUPPORT_CHAT_ID,
        text=f"#{req.id} {user.full_name}: {text}"
    )
    _ = get_translator(models.User[user.id].language)
    await update.message.reply_text(_("Спасибо, заявка принята."))
    return ConversationHandler.END

async def set_report_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    _ = get_translator(u.language)
    if not context.args or ':' not in context.args[0]:
        return await update.message.reply_text(_("Использование: /setreport HH:MM"))
    hh, mm = map(int, context.args[0].split(':'))
    u.report_time = (hh, mm); u.save()
    context.job_queue.run_daily(
        daily_report, time(hour=hh, minute=mm),
        context=user.id, name=str(user.id)
    )
    await update.message.reply_text(
        _("Отчёт будет приходить каждый день в {:02d}:{:02d}").format(hh, mm)
    )

async def daily_report(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.context
    u = models.User[user_id]
    _ = get_translator(u.language)
    report = services.mining.get_daily_report(u)
    await context.bot.send_message(chat_id=user_id, text=_("Ваш отчёт:
") + report)

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(config.TG_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language_cmd))
    app.add_handler(CallbackQueryHandler(lang_callback, pattern="^lang_"))

    conv = ConversationHandler(
        entry_points=[CommandHandler('support', support_start)],
        states={ASK_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, support_receive)]},
        fallbacks=[CallbackQueryHandler(lambda u,c: c.end(), pattern="^CANCEL$")]
    )
    app.add_handler(conv)

    app.add_handler(CommandHandler("setreport", set_report_time))

    for u in models.User.with_report_time():
        hh, mm = u.report_time
        app.job_queue.run_daily(daily_report, time(hour=hh, minute=mm),
                                context=u.id, name=str(u.id))

    app.run_polling()

if __name__ == "__main__":
    main()
