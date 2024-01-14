from telegram import *
from telegram.ext import *
from modules.roll import diceRoll

CLASSES = ["Guerreiro", "Clérigo", "Ladrão", "Usuário de Magia", "Anão", "Elfo", "Halfling"]
HD = [8, 6, 4, 4, 8, 6, 6]
MIN_HP = [6, 4, 2, 2, 6, 4, 4]
ALIGNMENT = ["Ordeiro", "Neutro", "Caótico"]

async def newCharacter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    classId = diceRoll(1, 7) - 1
    character = {
        "STR": diceRoll(3, 6),
        "DEX": diceRoll(3, 6),
        "CON": diceRoll(3, 6),
        "INT": diceRoll(3, 6),
        "WIS": diceRoll(3, 6),
        "CHA": diceRoll(3, 6), 
        "CLASS": CLASSES[classId],
        "HP": max(diceRoll(1, HD[classId]), MIN_HP[classId]),
        "ALIGNMENT": ALIGNMENT[diceRoll(1, 3)-1]
    }
    line1 = f"{character['CLASS']}\n"
    line2 = f"FOR:{character['STR']} DES:{character['DEX']} CON:{character['CON']}\n"
    line2 += f"INT:{character['INT']} SAB:{character['WIS']} CAR:{character['CHA']}\n"
    line3 = f"PV:{character['HP']}\n"
    line4 = f"Alinhamento: {character['ALIGNMENT']}\n"
    response =  "<pre>" + line1 + line4 + line3 + line2 + "</pre>"


    await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='HTML')