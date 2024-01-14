import logging
from telegram import *
from telegram.ext import *
import config
import modules.misc as miscCommands
import modules.roll as rollCommands   
import modules.coc as cocCommands
import modules.ose as oseCommands

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(config.API_KEY).build()
    
    start_handler = CommandHandler('start', miscCommands.start)
    unknown_handler = MessageHandler(filters.COMMAND, miscCommands.unknown)
    help_handler = CommandHandler('help', miscCommands.help)
    roll_handler = CommandHandler('roll', rollCommands.roll)
    test_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), miscCommands.test)
    coc_character_handler = CommandHandler('newcharacter', cocCommands.newCharacter)
    coc_get_character_handler = CommandHandler('getcharacter', cocCommands.get_character)
    coc_san_handler = CommandHandler('san', cocCommands.san_test)
    ose_new_char_handler = CommandHandler('oseChar', oseCommands.newCharacter)


    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(roll_handler)
    application.add_handler(coc_character_handler)
    application.add_handler(coc_get_character_handler)
    application.add_handler(coc_san_handler)
    application.add_handler(ose_new_char_handler)


    application.add_handler(test_handler)
    application.add_handler(unknown_handler) #added last

    #bot_db.start_database()    


    application.run_polling()