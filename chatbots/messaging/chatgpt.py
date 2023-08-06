import os
from dotenv import load_dotenv

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from telegram_integration import TelegramIntegration


class LLMBot:
    def setup_llm(self):
        # LLM
        llm = ChatOpenAI()

        # Prompt
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a nice chatbot having a conversation with a human. You can add emojis to your answers. Limit your answers to 1000 characters. "
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )

        # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
        # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.conversation = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = await self.conversation.arun(update.message.text)
        await update.message.reply_text(message)


def main() -> None:

    # Firstly load all the environment variables
    load_dotenv()

    """Start the bot."""
    bot = LLMBot()
    bot.setup_llm()

    telegram_int = TelegramIntegration(bot_token=os.environ.get("TELEGRAM_TOKEN"))
    telegram_int.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    telegram_int.loop()


if __name__ == "__main__":
    main()
