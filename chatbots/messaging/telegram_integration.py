from emoji import emojize

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


class TelegramIntegration:
    bot_token: str

    def __init__(self, bot_token: str) -> None:

        # Create the Application and pass it your bot's token.
        self.application = Application.builder().token(bot_token).build()

        # on different commands - answer in Telegram
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

    def add_handler(self, handler) -> None:
        """ Add a custom handler to the application """
        self.application.add_handler(handler)

    def loop(self) -> None:
        # Run the bot until the user presses Ctrl-C
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! I'm your favorite assistant "
            rf"{emojize(':grinning_face_with_big_eyes:')}, how can I help you?"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message."""
        await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    telegram_int = TelegramIntegration(bot_token=TOKEN)
    telegram_int.add_handler(CommandHandler("start", telegram_int.start_command))
    telegram_int.loop()


if __name__ == "__main__":
    main()
