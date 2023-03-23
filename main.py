import logging
from telegram import *
from telegram.ext import *
import config
import commands.misc as miscCommands
import commands.roll as rollCommands   

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

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(roll_handler)

    application.add_handler(unknown_handler) #added last

    application.run_polling()