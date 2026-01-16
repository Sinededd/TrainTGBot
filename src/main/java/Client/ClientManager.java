package Client;

import java.util.HashMap;
import java.util.Map;

public class ClientManager {
    private final Map<Long, Client> clients;

    public ClientManager()
    {
        clients = new HashMap<>();
    }

    public Client getClient(long chatId)
    {
        return clients.get(chatId);
    }

    public Client getOrAddClient(long chatId)
    {
        return clients.computeIfAbsent(chatId, _ -> {
            System.out.println("Создан новый клиент: " + chatId);
            return new Client(chatId);
        });
    }

    public Map<Long, Client> getAllClients() {
        return new HashMap<>(clients);
    }
}
