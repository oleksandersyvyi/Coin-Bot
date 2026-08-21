import telebot
import time
import threading
from db import check_and_save_coins, add_user, get_all_users

TOKEN = "8543115817:AAH-7j15xuVxyqbwSpFxDhXQUqMWbbOLT5g"
bot = telebot.TeleBot(TOKEN)


def auto_check():
    while True:
        time.sleep(300)
        new_coins = check_and_save_coins()

        if new_coins:
            users = get_all_users()

            for chat_id in users:
                try:
                    bot.send_message(chat_id, f"🚨 **УВАГА! ЗНАЙДЕНО НОВІ МОНЕТИ: {len(new_coins)}** 🚨",
                                     parse_mode="Markdown")
                    for coin in new_coins:
                        msg_text = (
                            f"🪙 *{coin['title']}*\n"
                            f"💰 *Ціна:* {coin['price']}\n"
                            f"🔗 [Посилання на монету]({coin['link']})"
                        )
                        bot.send_message(chat_id, msg_text, parse_mode="Markdown")
                except Exception as e:
                    print(f"Не вдалося відправити повідомлення користувачу {chat_id}: {e}")


# --- 2. Обробники ручних команд ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    current_chat_id = message.chat.id
    first_name = message.from_user.first_name

    add_user(current_chat_id)

    welcome_text = (
        f"Привіт, {first_name}! 👋\n"
        f"Я успішно запам'ятав тебе. Тепер ти отримуватимеш автоматичні сповіщення "
        f"про нові монети НБУ кожні 5 хвилин!\n\n"
        f"Натисни /check, щоб перевірити наявність оновлень прямо зараз."
    )
    bot.send_message(current_chat_id, welcome_text)


@bot.message_handler(commands=['check'])
def check_coins_command(message):
    current_chat_id = message.chat.id
    bot.send_message(current_chat_id, "🔍 Перевіряю сайт НБУ...")

    new_coins = check_and_save_coins()

    if new_coins:
        bot.send_message(current_chat_id, f"🎉 Знайдено нових монет: {len(new_coins)}!")
        for coin in new_coins:
            msg_text = (
                f"🪙 *{coin['title']}*\n"
                f"💰 *Ціна:* {coin['price']}\n"
                f"🔗 [Посилання на монету]({coin['link']})"
            )
            bot.send_message(current_chat_id, msg_text, parse_mode="Markdown")
    else:
        bot.send_message(current_chat_id, "🕳️ Нових монет поки немає. База даних актуальна.")


if __name__ == "__main__":
    background_thread = threading.Thread(target=auto_check, daemon=True)
    background_thread.start()

    print("Бот запущений! База користувачів активна.")
    bot.polling(none_stop=True)