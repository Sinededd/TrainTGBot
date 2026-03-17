package Client;

import Handlers.MessageHandler;
import Handlers.MessageSender;
import Models.Tariff;
import Models.Train;
import Web.Parser;

import java.io.Serializable;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Objects;

public class NotificationSession implements Serializable {
    private final Client client;
    private Train train;

    public NotificationSession(Client client, Train train)
    {
        this.client = client;
        this.train = train;
        start();
    }

    public void start()
    {
        IO.println("Начата сессия: " + client.getId() + " -> " + train.getId() );
        NotificationManager.getInstance().addSession(this);
    }

    public void stop()
    {
        IO.println("Завершена сессия: " + client.getId() + "->" + train.getId() );
        NotificationManager.getInstance().removeSession(this);
    }

    public Train getTrain() {
        return train;
    }

    public Client getClient() {
        return client;
    }

    public void sendSignal() {
        ArrayList<Train> trains = Parser.getTrains(train.getDepStation(), train.getArrStation(), train.getLocalDate());
        Train curTrain = null;
        for(Train train : trains)
        {
            if(Objects.equals(train.getId(), this.train.getId()))
            {
                curTrain = train;
                break;
            }
        }
        if(curTrain == null)
        {
            return;
        }

        int countPlaceOfCurTrain = 0;
        int countPlaceOfTrain = 0;
        for(Tariff tariff: curTrain.getTariffs().getAllTariffs())
        {
            countPlaceOfCurTrain += Integer.parseInt(tariff.getCountPlace());
        }
        for(Tariff tariff: this.train.getTariffs().getAllTariffs())
        {
            countPlaceOfTrain += Integer.parseInt(tariff.getCountPlace());
        }

        IO.println("Сигнал: " +
                client.getId() + " -> " +
                train.getId() + "\t\t" +
                LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss")));
        if(countPlaceOfTrain != countPlaceOfCurTrain)
        {
            MessageSender.sendMessage(client, "Обновился поезд:");
            MessageSender.sendMessageTrain(client, curTrain);
            IO.println("Было: " + countPlaceOfTrain);
            IO.println("Стало: " + countPlaceOfCurTrain);
            this.train = curTrain;
        }




    }
}
