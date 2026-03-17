package Bot;

import Client.ClientManager;
import Handlers.CallbackHandler;
import Handlers.MessageHandler;
import org.telegram.telegrambots.client.okhttp.OkHttpTelegramClient;
import org.telegram.telegrambots.longpolling.util.LongPollingSingleThreadUpdateConsumer;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.generics.TelegramClient;


public class MyBot implements LongPollingSingleThreadUpdateConsumer {
    private final MessageHandler messageHandler;
    private final CallbackHandler callbackHandler;


    public MyBot(String botToken)
    {
        super();
        TelegramClient telegramClient = new OkHttpTelegramClient(botToken);
        ClientManager clientManager = new ClientManager();
        messageHandler = new MessageHandler(clientManager, telegramClient);
        callbackHandler = new CallbackHandler(clientManager, telegramClient);
    }

    @Override
    public void consume(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            messageHandler.inputHandle(update.getMessage());
        }
        else if (update.hasCallbackQuery()) {
            callbackHandler.inputHandle(update.getCallbackQuery());

        }
    }
}