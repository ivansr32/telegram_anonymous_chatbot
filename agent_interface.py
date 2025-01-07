from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from database import Database

db = Database("chats.db")

def register_agent(update: Update, context: CallbackContext) -> None:
    agent_id = update.message.chat_id
    db.register_agent(agent_id)
    update.message.reply_text("¡Te has registrado como agente!")

def handle_agent_reply(update: Update, context: CallbackContext) -> None:
    agent_id = update.message.chat_id
    user_id = db.get_assigned_user(agent_id)
    if user_id:
        context.bot.send_message(chat_id=user_id, text=update.message.text)
    else:
        update.message.reply_text("No tienes chats asignados en este momento.")

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("register", register_agent))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_agent_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
