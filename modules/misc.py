from telegram import *
from telegram.ext import *
from functools import wraps
import config
import constants
from random import choice


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.message.chat_id
        print(f"user: {user_id}   chat: {chat_id}")
        if user_id not in config.LIST_OF_USERS and chat_id not in config.LIST_OF_CHATS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.START_TEXT)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.HELP_TEXT)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Comando não encontrado")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    res = ''.join(choice((str.upper, str.lower))(char) for char in message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=res)