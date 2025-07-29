from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
import config, models, services.support
from utils import get_translator

ASK_QUESTION = 1

async def support_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    u, _ = models.User.get_or_create(user.id)
    _ = get_translator(u.language)
    await update.message.reply_text(
        _("Опишите вашу проблему, и мы свяжемся с вами."),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(_('Отмена'), callback_data='CANCEL')]])
    )
    return ASK_QUESTION

async def support_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    req = services.support.create_request(user.id, text)
    await context.bot.send_message(
        chat_id=config.SUPPORT_CHAT_ID,
        text=f"#{req.id} {user.full_name} (id={user.id}): {text}"
    )
    _ = get_translator(u.language)
    await update.message.reply_text(_("Спасибо, ваша заявка принята."))
    return ConversationHandler.END
