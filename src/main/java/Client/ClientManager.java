package Client;

import Bot.Serializer;
import org.telegram.telegrambots.meta.api.objects.User;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class ClientManager implements Serializable {
    private final Map<Long, Client> clients; // <chat id, client>
    private final NotificationManager notificationManager;

    public ClientManager() {
        Map<Long, Client> tempClients = new HashMap<>();

        ClientManager loaded = Serializer.loadClientManager();
        if (loaded != null && loaded.clients != null) {
            tempClients.putAll(loaded.clients);
        }

        this.clients = tempClients;
        this.notificationManager = NotificationManager.getInstance();
        if(loaded != null && loaded.notificationManager != null)
        {
            this.notificationManager.setSessions(loaded.notificationManager.getSessions());
        }
    }

    public Client getClient(long chatId)
    {
        return clients.get(chatId);
    }

    public Client getOrAddClient(long chatId, User user)
    {
        if(!clients.containsKey(chatId))
        {
            System.out.println("Создан новый клиент: " + chatId);
            Client newClient = new Client(chatId, user, this);
            clients.put(chatId, newClient);
           save();
            return newClient;
        }
        return clients.get(chatId);
    }

    public Map<Long, Client> getAllClients() {
        return new HashMap<>(clients);
    }

    public void save()
    {
        Serializer.saveClientManager(this);
    }
}
