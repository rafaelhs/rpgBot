from telegram import *
from telegram.ext import *
from modules.roll import diceRoll
import modules.bot_db as bot_db

async def newCharacter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.message.from_user['id']
    name = update.message.from_user['first_name']
    character = bot_db.get_coc_character(id)
    if(character != None):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f"{name} já tem um personagem")
    else:
        character = rollCharacter(id, name)
        bot_db.create_coc_character(character)
        formatedCharacter = formatCharacter(character)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=formatedCharacter, parse_mode='HTML')

async def get_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    character = bot_db.get_coc_character(update.message.from_user['id'])
    if character == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Nenhum personagem encontrado")

    else:  
        formated_character = formatCharacter(character)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=formated_character, parse_mode='HTML')

def rollCharacter(id, name):
    character = {
        "ID": id,
        "NOME": name,
        "FOR": diceRoll(3, 6) * 5,
        "CON": diceRoll(3, 6) * 5,
        "TAM": (diceRoll(2, 6) + 6) * 5,
        "DES": diceRoll(3, 6) * 5,
        "APA": diceRoll(3, 6) * 5,
        "INT": (diceRoll(2, 6) + 6) * 5,
        "POD": diceRoll(3, 6) * 5,
        "EDU": (diceRoll(2, 6) + 6) * 5,
        "SOR": diceRoll(3, 6) * 5
    }
    character['SAN'] = character["POD"]
    character['HP'] = (character["CON"] + character["TAM"]) // 10
    character["MP"] = character["POD"] // 5
    return character

def formatCharacter(character):
    line1 = f"{character['NOME']}\n"
    line2 = f"FOR: {character['FOR']} DES: {character['DES']} CON: {character['CON']} TAM: {character['TAM']}\n"
    line3 = f"INT: {character['INT']} EDU: {character['EDU']} APA: {character['APA']} POD: {character['POD']}\n" 
    line4 = f"SAN: {character['SAN']} SOR: {character['SOR']} HP: {character['HP']}"
    return "<pre>" + line1 + line2 + line3 + line4 + "</pre>"