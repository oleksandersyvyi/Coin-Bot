import requests
from bs4 import BeautifulSoup

def parse_nbu_coins():
    url = "https://coins.bank.gov.ua/pam-atni-moneti/c-422.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Помилка підключення до сайту:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Використовуємо select для надійного пошуку за класом
    product_cards = soup.select("div[class*='product_bank']")
    print(f"Знайдено потенційних блоків: {len(product_cards)}")
    coins_list = []  # Обов'язково на новому рядку!

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


if __name__ == "__main__":
    print("Збираємо дані з сайту НБУ...")
    coins = parse_nbu_coins()
    print(f"Успішно знайдено монет: {len(coins)}\n")

    for coin in coins[:3]:
        print(f"ID: {coin['id']}")
        print(f"Назва: {coin['title']}")
        print(f"Ціна: {coin['price']}")
        print(f"Посилання: {coin['link']}")
        print("-" * 40)