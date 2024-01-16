from telegram import *
from telegram.ext import *
from functools import wraps
import config
from random import choice

def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        if config.RESTRICTED:
            user_id = update.effective_user.id
            chat_id = update.message.chat_id
            if user_id not in config.LIST_OF_USERS and chat_id not in config.LIST_OF_CHATS:
                print(f"Unauthorized access denied for {user_id}.")
                return
            return await func(update, context, *args, **kwargs)
    return wrapped

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    str = '  🎲 RPG Bot 🎲\n ⚔️ 🛡️ 🗡️ 🏹 🪄'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str)

@restricted
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    str = ("  🎲 RPG Bot 🎲\n"
             "⚔️ 🛡️ 🗡️ 🏹 🪄\n\n"
             "/help - Informações sobre o bot\n"
             "/roll [dados] - Rolagem de dados (ex: 2d6-1d4+1)\n\n"
             "🦑Chamado de Cthulhu🦑\n"
             "/cocnewchar - Rola um novo personagem de COC\n"
             "/cocgetchar - Retorna informações do personagem\n"
             "/san - Faz um teste de sanidade\n"
             "\n"
             "🗡️Oldschool Essentials🛡️\n"
             "/osenewchar - Rola um novo personagem de OSE\n"
             "\n"
             "🎲Tabelas Aleatórias🎲\n"
             "/voxcast - Passagens sacras do Cultus Mechanicus\n"
             "/espname [genero] - Gerador de nomes espanhos (sec XVI)"
             )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str)

@restricted
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Comando não encontrado")

@restricted
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    res = ''.join(choice((str.upper, str.lower))(char) for char in message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=res)