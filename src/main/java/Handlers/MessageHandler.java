package Handlers;

import Client.Client;
import Client.ClientManager;
import Client.ClientState;
import Models.Train;
import Web.NoTrainsFoundException;
import Web.Parser;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.message.Message;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.InlineKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardButton;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.InlineKeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import org.telegram.telegrambots.meta.generics.TelegramClient;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class MessageHandler {
    private final ClientManager clientManager;
    private final TelegramClient telegramClient;

    public MessageHandler(ClientManager clientManager, TelegramClient telegramClient)
    {
        this.clientManager = clientManager;
        this.telegramClient = telegramClient;
    }

    public void inputHandle(long chat_id, String msg)
    {
        Client client = clientManager.getOrAddClient(chat_id);  // Client.Client who sent the message
        ClientState inputState = client.getClientState();
        IO.println(client.getId() + "(" + client.getClientState() + "):\t\t" + msg);

        if(inputCommand(client, msg))
            return;

        switch (inputState)
        {
            case DEFAULT:
                break;
            case WAITING_FROM_STATION:
                client.setFromStation(msg);
                sendMessage(chat_id,"Введите город прибытия: ");
                client.setClientState(ClientState.WAITING_TO_STATION);
                break;
            case WAITING_TO_STATION:
                client.setToStation(msg);
                sendMessage(chat_id,"Введите дату оправления (2026-01-22): ");
                client.setClientState(ClientState.WAITING_DATE);
                break;
            case WAITING_DATE:
                try {
                    client.setDate(LocalDate.parse(msg));
                } catch (DateTimeParseException e) {
                    sendMessage(chat_id, "Неверный формат даты. Попробуйте ещё раз");
                    break;
                }
                requestToSite(client);
                client.setClientState(ClientState.DEFAULT);
                break;
        }
    }

    private boolean inputCommand(Client client, String msg)
    {
        switch (msg) {
            case "/start" -> {
                client.setClientState(ClientState.DEFAULT);
                return true;
            }
            case "/schedule" -> {
                if (sendMessage(client.getId(), "Введите город отправления: ")) {
                    client.setClientState(ClientState.WAITING_FROM_STATION);
                    return true;
                } else {
                    return false;
                }
            }
            case "/subscriptions" -> {
                client.setClientState(ClientState.DEFAULT);
                sendMessageTrains(client, client.getSubscribedTrains());
                return true;
//                if (sendMessage(client.getId(), "Введите город отправления: ")) {
//                    client.setClientState(ClientState.WAITING_FROM_STATION);
//                    return true;
//                } else {
//                    return false;
//                }
            }
            case "/test" -> {
                SendMessage message = SendMessage
                        .builder()
                        .chatId(client.getId())
                        .text("Тест кнопки")
                        .replyMarkup(InlineKeyboardMarkup
                                .builder()
                                .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
                                        .builder()
                                        .text("Нажми")
                                        .callbackData("test_button")
                                        .build())).build())
                        .build();
                try {
                    telegramClient.execute(message); // Sending our message object to user
                } catch (TelegramApiException e) {
                    System.err.println("Ошибка сообщения с кнопкий!!\n" + e.getMessage());
                    return false;
                }
                return true;
            }
        }
        return false;
    }

    private void requestToSite(Client client)
    {
        try {
            ArrayList<Train> trains = Parser.getTrains(client.getFromStation(),
                    client.getToStation(), client.getDate());
            sendMessageTrains(client, trains);
        } catch (NoTrainsFoundException e) {
            System.err.println(e.getMessage());
            sendMessage(client.getId(), e.getMessage());
        }
    }

    private void sendMessageTrains(Client client, ArrayList<Train> trains)
    {
        if(trains.isEmpty())
        {
            sendMessage(client.getId(), "Поездов нет");
            return;
        }

        Map<Integer, Train> savedTrains = new HashMap<>();
        for(Train train : trains)
        {
            IO.println("---------------------------");
            IO.println("ID: " + train.getId());
            IO.println(train.toString());

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

    public boolean sendMessage(long chat_id, String msg)
    {
        try {
            telegramClient.execute(new SendMessage(String.valueOf(chat_id), msg));
            return true;
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
            return false;
        }
    }

    public void sendMessageMarkdown(long chat_id, String msg)
    {
        SendMessage message = new SendMessage(String.valueOf(chat_id), msg);
        message.setParseMode("MarkdownV2");
        try {
            telegramClient.execute(message);
        } catch (TelegramApiException e) {
            System.err.println("\nОшибка отправки сообщения!!!\n" + e.getMessage());
        }
    }

}
