# 🪙 NBU Commemorative Coins Scraper & Bot

An automated web scraping tool and Telegram bot built to extract, track, and store information about commemorative coin releases from the official National Bank of Ukraine (NBU) website.

## 📌 Project Overview
Monitoring new coin releases manually can be time-consuming. This project automates the data extraction process (ETL logic) by parsing HTML pages, cleaning the data, and storing it in a structured relational database for easy access and querying.

## ⚙️ Features
* **Web Scraping:** Extracts real-time data on commemorative coins directly from the NBU portal.
* **Data Transformation:** Cleans and structures raw HTML elements into readable text/metrics.
* **Database Storage:** Automatically loads the parsed data into a local SQLite database, preventing duplicates.
* **Notifications (Optional):** Can notify users via Telegram when new entries are added.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Data Extraction:** requests, BeautifulSoup4
* **Database:** SQLite (built-in)
* **Bot Framework:** [aiogram / pyTelegramBotAPI - *remove if it's just a scraper without a bot*]

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/nbu-coins-scraper.git](https://github.com/your-username/nbu-coins-scraper.git)
   cd nbu-coins-scraper
