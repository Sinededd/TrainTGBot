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
    private final MessageSender messageSender;

    public MessageHandler(ClientManager clientManager, TelegramClient telegramClient)
    {
        this.clientManager = clientManager;
        messageSender = new MessageSender(telegramClient);
    }

    public void inputHandle(Message message)
    {
        long chat_id = message.getChatId();
        String msg = message.getText();
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
                messageSender.sendMessage(client,"Введите город прибытия: ");
                client.setClientState(ClientState.WAITING_TO_STATION);
                break;
            case WAITING_TO_STATION:
                client.setToStation(msg);
                messageSender.sendMessage(client,"Введите дату оправления (2026-01-22): ");
                client.setClientState(ClientState.WAITING_DATE);
                break;
            case WAITING_DATE:
                try {
                    client.setDate(LocalDate.parse(msg));
                } catch (DateTimeParseException e) {
                    messageSender.sendMessage(client, "Неверный формат даты. Попробуйте ещё раз");
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
                if (messageSender.sendMessage(client, "Введите город отправления: ")) {
                    client.setClientState(ClientState.WAITING_FROM_STATION);
                    return true;
                } else {
                    return false;
                }
            }
            case "/subscriptions" -> {
                client.setClientState(ClientState.DEFAULT);
                messageSender.sendMessageTrains(client, client.getSubscribedTrains());
                return true;
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
                    messageSender.getTelegramClient().execute(message);
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
            messageSender.sendMessageTrains(client, trains);
        } catch (NoTrainsFoundException e) {
            System.err.println(e.getMessage());
            messageSender.sendMessage(client, e.getMessage());
        }
    }
}
