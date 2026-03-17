package Handlers;

import Client.Client;
import Models.Train;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.message.Message;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MessageSender {
    private static TelegramClient telegramClient = null;

    public MessageSender(TelegramClient telegramClient)
    {
        MessageSender.telegramClient = telegramClient;
    }

    public TelegramClient getTelegramClient() {
        return telegramClient;
    }

    public static boolean sendMessage(Client client, String msg)
    {
        try {
            telegramClient.execute(new SendMessage(String.valueOf(client.getId()), msg));
            return true;
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
            return false;
        }
    }

    public static void sendMessageMarkdown(Client client, String msg)
    {
        SendMessage message = new SendMessage(String.valueOf(client.getId()), msg);
        message.setParseMode("MarkdownV2");
        try {
            telegramClient.execute(message);
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
        }
    }

    public static void sendMessageTrains(Client client, ArrayList<Train> trains)
    {
        if(trains.isEmpty())
        {
            sendMessage(client, "Поездов нет");
            return;
        }

        Map<Integer, Train> savedTrains = new HashMap<>();
        for(Train train : trains)
        {
            IO.println("---------------------------");
            IO.println("ID: " + train.getId());

            SendMessage message;
            if(client.checkSession(train.getId()))
            {
                message = SendMessage.builder()
                        .chatId(client.getId())
                        .text(train.toString())
                        .replyMarkup(InlineKeyboardMarkup.builder()
                                .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                        .builder()
                                        .text("Отписаться")
                                        .callbackData("unsubscribe_button")
                                        .build()))
                                .build())
                        .build();
            } else {
                message = SendMessage.builder()
                        .chatId(client.getId())
                        .text(train.toString())
                        .replyMarkup(InlineKeyboardMarkup.builder()
                                .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                        .builder()
                                        .text("Подписаться")
                                        .callbackData("subscribe_button")
                                        .build()))
                                .build())
                        .build();
            }

            message.setParseMode("MarkdownV2");
            try {
                Message msg = telegramClient.execute(message);
                savedTrains.put(msg.getMessageId(), train);
            } catch (TelegramApiException e) {
                System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
            }
        }
        client.setSavedTrains(savedTrains);
    }

    public static void sendMessageTrain(Client client, Train train)
    {
        IO.println("---------------------------");
        IO.println("ID: " + train.getId());

        SendMessage message;
        if(client.checkSession(train.getId()))
        {
            message = SendMessage.builder()
                    .chatId(client.getId())
                    .text(train.toString())
                    .replyMarkup(InlineKeyboardMarkup.builder()
                            .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                    .builder()
                                    .text("Отписаться")
                                    .callbackData("unsubscribe_button")
                                    .build()))
                            .build())
                    .build();
        } else {
            message = SendMessage.builder()
                    .chatId(client.getId())
                    .text(train.toString())
                    .replyMarkup(InlineKeyboardMarkup.builder()
                            .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                    .builder()
                                    .text("Подписаться")
                                    .callbackData("subscribe_button")
                                    .build()))
                            .build())
                    .build();
        }

        Map<Integer, Train> savedTrains = new HashMap<>();
        message.setParseMode("MarkdownV2");
        try {
            Message msg = telegramClient.execute(message);
            savedTrains.put(msg.getMessageId(), train);
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
        }
        client.setSavedTrains(savedTrains);
    }
}