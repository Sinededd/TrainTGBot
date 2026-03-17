package Handlers;

import Client.Client;
import Client.ClientManager;
import Models.Train;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.methods.updatingmessages.EditMessageText;
import org.telegram.telegrambots.meta.api.objects.CallbackQuery;
import org.telegram.telegrambots.meta.api.objects.message.MaybeInaccessibleMessage;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

import java.util.HashMap;
import java.util.Map;

import static java.lang.Math.toIntExact;

public class CallbackHandler {
    private final ClientManager clientManager;
    private final TelegramClient telegramClient;

    public CallbackHandler(ClientManager clientManager, TelegramClient telegramClient)
    {
        this.clientManager = clientManager;
        this.telegramClient = telegramClient;
    }

    public void inputHandle(CallbackQuery callbackQuery)
    {
        String call_data = callbackQuery.getData();
        long chat_id = callbackQuery.getMessage().getChatId();
        int message_id = callbackQuery.getMessage().getMessageId();

        Client client = clientManager.getOrAddClient(chat_id, callbackQuery.getFrom());
        IO.println(client.getId() + "(Button):\t\t" + call_data);
        switch (call_data) {
            case "test_button" -> testOnTrain(chat_id, message_id);
            case "subscribe_button" -> onSubscribeButton(callbackQuery);
            case "unsubscribe_button" -> onUnsubscribeButton(callbackQuery);
        }
    }

    private void testOnTrain(long chat_id, long message_id)
    {
        String answer = "Пошел нахуй";
//        String answer = "Люблю тебя💖";
        EditMessageText new_message = EditMessageText.builder()
                .chatId(chat_id)
                .messageId(toIntExact(message_id))
                .text(answer)
                .build();
        try {
            telegramClient.execute(new_message);
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка нажатия кнопки!!!\n" + e.getMessage());
        }
    }

    private void onSubscribeButton(CallbackQuery callbackQuery)
    {
        long chat_id = callbackQuery.getMessage().getChatId();
        int message_id = callbackQuery.getMessage().getMessageId();
        String msg = callbackQuery.getMessage().toString();

        Client client = clientManager.getOrAddClient(chat_id, callbackQuery.getFrom());
        Train train = client.getTrainByMessageId(message_id);
        if(train == null) {
            EditMessageText new_message = EditMessageText.builder()
                    .chatId(chat_id)
                    .messageId(message_id)
                    .text("Обновите расписание поездов")
                    .build();
            try {
                telegramClient.execute(new_message);
            } catch (TelegramApiException e) {
                System.err.println("\nОшибка нажатия кнопки!!!\n" + e.getMessage());
            }
        }
        else {
            client.addSession(train);
            EditMessageText message = EditMessageText.builder()
                .chatId(chat_id)
                .messageId(message_id)
                .text(train.toString())
                .replyMarkup(InlineKeyboardMarkup.builder()
                        .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                .builder()
                                .text("Отписаться")
                                .callbackData("unsubscribe_button")
                                .build()))
                        .build())
                .build();
        message.setParseMode("MarkdownV2");
        try {
            telegramClient.execute(message);
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
        }
        }
    }

    private void onUnsubscribeButton(CallbackQuery callbackQuery)
    {
        long chat_id = callbackQuery.getMessage().getChatId();
        int message_id = callbackQuery.getMessage().getMessageId();
        String msg = callbackQuery.getMessage().toString();

        Client client = clientManager.getOrAddClient(chat_id, callbackQuery.getFrom());
        Train train = client.getTrainByMessageId(message_id);
        if(train == null) {
            EditMessageText new_message = EditMessageText.builder()
                    .chatId(chat_id)
                    .messageId(message_id)
                    .text("Обновите расписание поездов")
                    .build();
            try {
                telegramClient.execute(new_message);
            } catch (TelegramApiException e) {
                System.err.println("\nОшибка нажатия кнопки!!!\n" + e.getMessage());
            }
        }
        else {
            client.stopSession(train);
            EditMessageText message = EditMessageText.builder()
                    .chatId(chat_id)
                    .messageId(message_id)
                    .text(train.toString())
                    .replyMarkup(InlineKeyboardMarkup.builder()
                            .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                    .builder()
                                    .text("Подписаться")
                                    .callbackData("subscribe_button")
                                    .build()))
                            .build())
                    .build();
            message.setParseMode("MarkdownV2");
            try {
                telegramClient.execute(message);
            } catch (TelegramApiException e) {
                System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
            }
        }
    }
}
