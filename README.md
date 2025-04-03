# РІЄЛТОР - ЗЛО! Бот

A Python bot that monitors OLX listings and sends notifications to multiple Telegram chats.

## Features

- Monitors OLX listings in real-time using GraphQL API
- Detects realtor listings using multiple methods:
  - Business account verification
  - Keyword analysis in descriptions
  - Number of listings per user (2+ listings)
  - User profile analysis
- Sends notifications to multiple Telegram chats
- Stores processed listings in SQLite database
- Supports Ukrainian language listings
- Real-time price monitoring
- Detailed listing information including:
  - Location details (district, city, region)
  - Contact information
  - User profile data
  - Photos and promotion status
  - Price history and currency conversion

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_IDS=chat_id1,chat_id2,chat_id3
   ```
   - Replace `your_bot_token_here` with your Telegram bot token
   - Replace `chat_id1,chat_id2,chat_id3` with your chat IDs, separated by commas

## Project Structure

- `main.py` - Main script that runs the bot and handles GraphQL API requests
- `parser.py` - Handles OLX data parsing and message formatting
- `realtor_detector.py` - Contains logic for detecting realtor listings
- `database.py` - Manages SQLite database operations
- `bot.py` - Handles Telegram bot functionality
- `message_formatter.py` - Formats messages for Telegram
- `.env` - Configuration file for tokens and chat IDs
- `requirements.txt` - Python dependencies

## Message Format

The bot sends messages in the following format:

```
🏠 ВСТВАВАЙ НОВА ХАТА

[Realtor Status]
📌 [Title]
💰 Ціна: [Price] UAH
📍 Район: [District]
👤 Власник: [Owner Name]
📱 Телефон: [Phone Status]
📊 Кількість оголошень: [Listings Count]
📅 Дата створення: [Created Time]
🔄 Дата останнього оновлення: [Last Update Time]
🔗 URL: [Listing URL]
```

Realtor status indicators:
- 🔴 Рієлтор - Confirmed realtor (business account or keywords)
- 🟡 МОЖЛИВО НЕ РІЄЛТОР - User has 2+ listings
- 🟢 МОЖЛИВО Без рієлтора - User has fewer than 5 listings

## Usage

1. Configure your `.env` file with your bot token and chat IDs
2. Run the script:
   ```bash
   python main.py
   ```

The bot will:
- Check for new listings every 5 minutes
- Process and analyze each listing
- Send notifications to configured Telegram chats
- Store processed listings in the database

## Dependencies

- python-telegram-bot
- requests
- python-dotenv
- schedule
- sqlite3 (built-in)

## License

MIT License 