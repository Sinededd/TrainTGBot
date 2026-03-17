package Handlers;

import Client.Client;
import Client.ClientManager;
import Client.ClientState;
import Client.ClientPermissions;
import Client.NotificationSession;
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
import java.util.Map;
import java.util.Set;

public class MessageHandler {
    private final ClientManager clientManager;
    private final MessageSender messageSender;

    public MessageHandler(ClientManager clientManager, TelegramClient telegramClient)
    {
        this.messageSender = new MessageSender(telegramClient);
        this.clientManager = clientManager;
    }

    public void inputHandle(Message message)
    {
        long chat_id = message.getChatId();
        String msg = message.getText();

        Client client = clientManager.getOrAddClient(chat_id, message.getFrom());  // Client.Client who sent the message
        ClientState inputState = client.getClientState();
        IO.println(client.getId() + ":" + message.getFrom().getUserName() + "(" + client.getClientState() + "):\t\t" + msg);

        if(inputCommand(client, message))
            return;

        switch (inputState)
        {
            case DEFAULT:
                break;
            case WAITING_FROM_STATION:
                client.setFromStation(msg);
                MessageSender.sendMessage(client,"Введите город прибытия: ");
                client.setClientState(ClientState.WAITING_TO_STATION);
                break;
            case WAITING_TO_STATION:
                client.setToStation(msg);
                MessageSender.sendMessage(client,"Введите дату оправления (2026-01-22): ");
                client.setClientState(ClientState.WAITING_DATE);
                break;
            case WAITING_DATE:
                try {
                    client.setDate(LocalDate.parse(msg));
                } catch (DateTimeParseException e) {
                    MessageSender.sendMessage(client, "Неверный формат даты. Попробуйте ещё раз");
                    break;
                }
                requestToSite(client);
                client.setClientState(ClientState.DEFAULT);
                break;
        }
    }

    private boolean inputCommand(Client client, Message message)
    {
        String msg = message.getText();
        switch (msg) {
            case "/start" -> {
                client.setClientState(ClientState.DEFAULT);
                return true;
            }
            case "/schedule" -> {
                if (MessageSender.sendMessage(client, "Введите город отправления: ")) {
                    client.setClientState(ClientState.WAITING_FROM_STATION);
                    return true;
                } else {
                    return false;
                }
            }
            case "/subscriptions" -> {
                client.setClientState(ClientState.DEFAULT);
                MessageSender.sendMessageTrains(client, client.getSubscribedTrains());
                return true;
            }
//            case "/test" -> {
//                SendMessage message = SendMessage
//                        .builder()
//                        .chatId(client.getId())
//                        .text("Тест кнопки")
//                        .replyMarkup(InlineKeyboardMarkup
//                                .builder()
//                                .keyboardRow(new InlineKeyboardRow(InlineKeyboardButton
//                                        .builder()
//                                        .text("Нажми")
//                                        .callbackData("test_button")
//                                        .build())).build())
//                        .build();
//                try {
//                    messageSender.getTelegramClient().execute(message);
//                } catch (TelegramApiException e) {
//                    System.err.println("Ошибка сообщения с кнопкий!!\n" + e.getMessage());
//                    return false;
//                }
//                return true;
//            }
            case "/admin" -> {
                client.setClientState(ClientState.DEFAULT);
                if(client.getClientPermissions() == ClientPermissions.USER){
                    MessageSender.sendMessage(client,"У вас нет прав адмистратора");
                    IO.println("Пользователь " + client.getId() + "не имеет прав админа");
                }
                else if(client.getClientPermissions() == ClientPermissions.ADMIN)
                {
                    MessageSender.sendMessage(client,"Команды администратора:\n" +
                            "/users - показывает список пользователей");
                    IO.println("Пользователь " + client.getId() + "является админом");
                }
                return true;
            }
            case "/users" -> {
                client.setClientState(ClientState.DEFAULT);
                StringBuilder outText = new StringBuilder("Пользователи:\n");
                if(client.getClientPermissions() == ClientPermissions.ADMIN) {
                    Map<Long, Client> clients = clientManager.getAllClients();
                    for (Client cl : clients.values()) {
                        outText.append("`").append(cl.getId()).append("`: @").append(cl.getClientUserName()).append("\n");
                        Set<NotificationSession> sessionSet = cl.getSessions();
                        for(NotificationSession s: sessionSet)
                        {
                            outText.append("`   ").append(s.getTrain().getId()).append("\n`");
                        }
                    }
                }
                String outTextStr = outText.toString()
                        .replace("*", "\\*")
                        .replace("_", "\\_")
                        .replace("[", "\\[")
                        .replace("]", "\\]")
                        .replace("(", "\\(")
                        .replace(")", "\\)");
                MessageSender.sendMessageMarkdown(client, outTextStr);
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
            MessageSender.sendMessageTrains(client, trains);
        } catch (NoTrainsFoundException e) {
            System.err.println(e.getMessage());
            MessageSender.sendMessage(client, e.getMessage());
        }
    }
}
