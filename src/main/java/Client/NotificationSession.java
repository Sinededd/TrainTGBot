package Client;

import Models.Train;

public class NotificationSession {
    private final Client client;
    private final Train train;
    private boolean isOpen = false;

    NotificationSession(Client client, Train train)
    {
        this.client = client;
        this.train = train;
        start();
    }

    public void start()
    {
        isOpen = true;
        IO.println("Начата сессия: " + client.getId() + " -> " + train.getId() );
    }

    public void stop()
    {
        IO.println("Завершена сессия: " + client.getId() + "->" + train.getId() );
        isOpen = false;
    }

    public Train getTrain() {
        return train;
    }
}
