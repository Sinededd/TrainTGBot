import Bot.Config;
import Bot.MyBot;

import org.telegram.telegrambots.longpolling.TelegramBotsLongPollingApplication;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

void main() {
    try {
        String botToken = Config.getBotToken();
        TelegramBotsLongPollingApplication botsApplication = new TelegramBotsLongPollingApplication();
        botsApplication.registerBot(botToken, new MyBot(botToken));
    } catch (TelegramApiException e) {
        e.printStackTrace();
    }
}