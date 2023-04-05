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

async def san_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    character = bot_db.get_coc_character(update.message.from_user['id'])
    if character == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Nenhum personagem encontrado")
    else: 
        id = character["ID"]
        name = character["NOME"]
        san = character["SAN"]
        sanLost = 0
        roll = diceRoll(1, 100)

        text =  f"A sanidade de <b>{name}</b> é testada..." 
        text += f"\n<b>{roll}</b> <i>vs</i> <b>{san}</b>"
        if roll <= character['SAN']:
            text += f"\n<b>Sucesso!</b>"
            sanLost = 1
        else:
            text += f"\n<b>Fracasso!</b>"
            sanLost = diceRoll(1, 6)
        text += f"\n<b>{name}</b> perde {sanLost} ponto(s) de sanidade"
        san -= sanLost
        if(san <= 0):
            bot_db.delete_coc_character(character['ID'])
            text += f"\ne fica permanentemente insano..."
        else:
            bot_db.update_coc_character_attr("SAN", san, id)
            
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=text, 
                                       parse_mode='HTML')


