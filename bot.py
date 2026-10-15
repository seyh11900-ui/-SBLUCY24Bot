import os
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Replace with your token from @BotFather

BOT_DESCRIPTION = (
    "Welcome to My Helper Bot! 👋\n\n"
    "I am here to assist you with automated answers, commands, and tasks. "
    "Click 'Start' below to begin exploring!"
)

BOT_ABOUT_TEXT = "A fast and reliable automated assistant for Telegram."

# Enable logging to inspect API events in terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# BOT HANDLERS
# -------------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user_name}! Your bot is active and ready. 🎉\n\n"
        "Send me any text message and I will echo it back to you!"
    )


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes user messages back."""
    await update.message.reply_text(f"You said: {update.message.text}")


# -------------------------------------------------------------------
# PROFILE INITIALIZATION
# -------------------------------------------------------------------
async def setup_bot_profile(app) -> None:
    """Configures the Bot Username, Description, and About text on startup."""
    bot = app.bot

    # Fetch and print Bot Username
    me = await bot.get_me()
    print("=" * 45)
    print(f"Bot Name:     {me.first_name}")
    print(f"Bot Username: @{me.username}")
    print("=" * 45)

    # Set Description (shown on the empty chat screen before clicking Start)
    await bot.set_my_description(description=BOT_DESCRIPTION)

    # Set Short Description / About text (shown on profile page & share links)
    await bot.set_my_short_description(short_description=BOT_ABOUT_TEXT)

    logger.info("Bot Description and About text updated successfully.")


# -------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------
def main():
    # 1. Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 2. Configure Bot Profile (Description / About) during initialization
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_bot_profile(app))

    # 3. Register command & message handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))

    # 4. Start polling for updates
    print("Starting bot polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
