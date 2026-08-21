import requests
import sqlite3
from bs4 import BeautifulSoup


def get_current_coins():
    url = "https://coins.bank.gov.ua/pam-atni-moneti/c-422.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Помилка підключення до сайту: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    product_cards = soup.select("div.col_product_bank")
    coins_list = []

    for card in product_cards:
        title_tag = card.find("a", class_="model_product")
        price_tag = card.find("span", class_="new_price")

        if title_tag:
            title = title_tag.text.strip()
            link = title_tag.get("href", "")
            price = price_tag.text.strip() if price_tag else "Ціна не вказана"

            full_link = "https://coins.bank.gov.ua" + link if link.startswith("/") else link
            coin_id = link.split("/")[-1].replace(".html", "")

            coins_list.append({
                "id": coin_id,
                "title": title,
                "price": price,
                "link": full_link
            })

    return coins_list


def check_and_save_coins():
    db_name = "coin.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS coin (id TEXT PRIMARY KEY, title TEXT, price TEXT, link TEXT)')
    connection.commit()

    current_coins = get_current_coins()
    new_coins = []

    for coin in current_coins:
        coin_id = coin['id']
        coin_title = coin['title']
        coin_price = coin['price']
        coin_link = coin['link']

        cursor.execute("SELECT id FROM coin WHERE id = ?", (coin_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO coin (id, title, price, link) VALUES (?, ?, ?, ?)",
                           (coin_id, coin_title, coin_price, coin_link))
            new_coins.append(coin)
    connection.commit()
    connection.close()
    return new_coins


def add_user(chat_id):
    db_name = "coin.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY)')
    cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    connection.commit()
    connection.close()


def get_all_users():
    db_name = "coin.db"
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY)')

    cursor.execute("SELECT chat_id FROM users")
    results = cursor.fetchall()

    connection.close()

    return [row[0] for row in results]

if __name__ == "__main__":
    print("Тестування файлу db.py...")
    fresh_coins = check_and_save_coins()

    if fresh_coins:
        print(f"Знайдено нових монет: {len(fresh_coins)}!\n")
        for coin in fresh_coins:
            print(f"- {coin['title']} | {coin['price']}")
    else:
        print("Нових монет не знайдено. База даних актуальна.")