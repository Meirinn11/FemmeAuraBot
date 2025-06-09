import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import BOT_TOKEN
from database import Database

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database('femmeaura.db')

# Handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🌸 **Hai! Aku FemmeAura, asisten haid & mood-mu.**\n"
        "Gunakan command:\n"
        "/start - Mulai bot\n"
        "/trackperiod - Catat haid terakhir\n"
        "/trackmood - Catat mood\n"
        "/tips - Dapatkan rekomendasi",
        parse_mode="Markdown"
    )

def track_period(update: Update, context: CallbackContext):
    update.message.reply_text("📅 **Kapan terakhir haid?** (Contoh: 01/06/2024)", parse_mode="Markdown")

def save_period(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    last_period = update.message.text
    db.save_period(user_id, last_period)
    update.message.reply_text("✅ Data haid tersimpan!")

def track_mood(update: Update, context: CallbackContext):
    mood_keyboard = [["😊 Senang", "😢 Sedih"], ["😠 Marah", "🥱 Lelah"]]
    reply_markup = ReplyKeyboardMarkup(mood_keyboard, one_time_keyboard=True)
    update.message.reply_text("💭 **Bagaimana moodmu hari ini?**", reply_markup=reply_markup, parse_mode="Markdown")

def save_mood(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    mood = update.message.text
    db.save_mood(user_id, mood)
    update.message.reply_text(f"📝 Mood tersimpan: {mood}")

def tips(update: Update, context: CallbackContext):
    update.message.reply_text("💡 **Tips Hari Ini:** Minum air jahe hangat jika kram!", parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trackperiod", track_period))
    dp.add_handler(CommandHandler("trackmood", track_mood))
    dp.add_handler(CommandHandler("tips", tips))

    # Message handlers
    dp.add_handler(MessageHandler(Filters.regex(r'^\d{2}/\d{2}/\d{4}$'), save_period))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, save_mood))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()