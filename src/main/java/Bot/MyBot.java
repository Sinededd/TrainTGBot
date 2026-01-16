package Bot;

import Client.ClientManager;
import Handlers.CallbackHandler;
import Handlers.MessageHandler;
import org.telegram.telegrambots.client.okhttp.OkHttpTelegramClient;
import org.telegram.telegrambots.longpolling.util.LongPollingSingleThreadUpdateConsumer;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.methods.updatingmessages.EditMessageText;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

import static java.lang.Math.toIntExact;


public class MyBot implements LongPollingSingleThreadUpdateConsumer {
    private final ClientManager clientManager;
    private final TelegramClient telegramClient;
    private final MessageHandler messageHandler;
    private final CallbackHandler callbackHandler;


    public MyBot(String botToken)
    {
        super();
        telegramClient = new OkHttpTelegramClient(botToken);
        clientManager = new ClientManager();
        messageHandler = new MessageHandler(clientManager, telegramClient);
        callbackHandler = new CallbackHandler(clientManager, telegramClient);
    }



    @Override
    public void consume(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            String message_text = update.getMessage().getText();
            long chat_id = update.getMessage().getChatId();
            messageHandler.inputHandle(chat_id, message_text);
        }
        else if (update.hasCallbackQuery()) {
//            update.getCallbackQuery().getMessage()
//            String call_data = update.getCallbackQuery().getData();
//            long message_id = update.getCallbackQuery().getMessage().getMessageId();
//            long chat_id = update.getCallbackQuery().getMessage().getChatId();
            callbackHandler.inputHandle(update.getCallbackQuery());

        }
    }
}