# TrainTGBot

A Telegram bot for searching and tracking train schedules in Belarus. Search for available trains, check seat availability, and view pricing from [pass.rw.by](https://pass.rw.by/ru/route).

## Features

- Train search between any two stations on a specific date
- Seat availability for different cabin classes
- Real-time ticket prices
- Multi-user support with persistent session storage
- Train notifications

## Quick Start

### Prerequisites
- Java 25+
- Maven 3.6+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Installation

1. Clone and build:
   ```bash
   git clone <repository-url>
   cd TrainTGBot
   mvn clean install
   ```

2. Create `.env` file:
   ```
   BOT_TOKEN=your_telegram_bot_token
   ```

3. Run:
   ```bash
   mvn exec:java
   ```

## Usage

1. Send `/start` to the bot
2. Enter departure and arrival stations
3. Choose travel date
4. Select a train to view details and availability

## Key Components

| Component | Purpose |
|-----------|---------|
| `MyBot` | Main bot class handling messages and callbacks |
| `ClientManager` | Manages all connected users |
| `Parser` | Scrapes train data using JSoup |
| `Train` | Train data model with builder pattern |
| `NotificationManager` | Handles user subscriptions |

## Tech Stack

- **Java 25** with Maven
- **telegrambots** 9.2.1 (Telegram Bot API)
- **jsoup** 1.22.1 (Web scraping)
- **dotenv-java** 3.0.0 (Configuration)

## Persistence

- Client sessions and subscriptions are serialized to disk
- Automatically loaded on bot startup

**Note**: Designed for the Belarusian railway system. Modifications needed for other services.

