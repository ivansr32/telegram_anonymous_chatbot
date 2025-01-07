from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from database import Database

db = Database("chats.db")  # Inicializa la base de datos.

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "¡Hola! Soy un chatbot anónimo. Escribe tu pregunta y un agente te responderá pronto."
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    message = update.message.text

    # Almacena el mensaje en la base de datos.
    db.save_message(user_id, "user", message)

    # Notifica a los agentes.
    agents = db.get_agents()
    for agent_id in agents:
        context.bot.send_message(
            chat_id=agent_id,
            text=f"Nuevo mensaje de usuario {user_id}:\n\n{message}"
        )

def agent_reply(update: Update, context: CallbackContext) -> None:
    agent_id = update.message.chat_id
    reply_to = db.get_user_for_agent(agent_id)
    if reply_to:
        response = update.message.text
        context.bot.send_message(chat_id=reply_to, text=response)
        db.save_message(reply_to, "agent", response)
    else:
        update.message.reply_text("No hay chats asignados en este momento.")

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.reply, agent_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
