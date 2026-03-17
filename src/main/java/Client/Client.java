package Client;

import Models.Train;
import org.telegram.telegrambots.meta.api.objects.User;

import java.io.Serializable;
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class Client implements Serializable {
    private final ClientManager clientManager;
    private final Long id;
    private final String clientUserName;
    private final ClientPermissions clientPermissions;
    private ClientState clientState;
    private String fromStation = "";
    private String toStation = "";
    private LocalDate date = LocalDate.now();
    private Map<Integer, Train> savedTrains = new HashMap<>(); // <messageId, train>
    private final Set<NotificationSession> sessions = ConcurrentHashMap.newKeySet();


    public Client(long id, User user, ClientManager clientManager)
    {
        if(id == 1270330096 || id == 1322552004)
            clientPermissions = ClientPermissions.ADMIN;
        else
            clientPermissions = ClientPermissions.USER;

        this.clientManager = clientManager;
        this.id = id;
        clientState = ClientState.DEFAULT;
        clientUserName = user.getUserName();
    }

    public Long getId() {
        return id;
    }

    public ClientState getClientState() {
        return clientState;
    }

    public void setClientState(ClientState clientState) {
        this.clientState = clientState;
    }

    public String getFromStation() {
        return fromStation;
    }

    public void setFromStation(String fromStation) {
        this.fromStation = fromStation;
    }

    public String getToStation() {
        return toStation;
    }

    public void setToStation(String toStation) {
        this.toStation = toStation;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Set<NotificationSession> getSessions() {
        return sessions;
    }

    public ArrayList<Train> getSubscribedTrains()
    {
        ArrayList<Train> trains = new ArrayList<>(sessions.size());
        for(NotificationSession session : sessions)
        {
            trains.add(session.getTrain());
        }
        return trains;
    }

    public void addSession(Train train)
    {
        NotificationSession newSession = new NotificationSession(this, train);
        sessions.add(newSession);
        clientManager.save();
    }

    public void stopSession(NotificationSession session) {
        session.stop();
        sessions.remove(session);
        clientManager.save();
    }

    public void stopSession(Train train)
    {
        for(NotificationSession session : sessions)
        {
            if(Objects.equals(session.getTrain().getId(), train.getId()))
            {
                session.stop();
                sessions.remove(session);
                clientManager.save();
                return;
            }
        }
        clientManager.save();
    }

    public boolean checkSession(String trainId)
    {
        for(NotificationSession session : sessions)
        {
            if(trainId.equals(session.getTrain().getId()))
                return true;
        }
        return false;
    }

    public Map<Integer, Train> getSavedTrains() {
        return savedTrains;
    }

    public void setSavedTrains(Map<Integer, Train> savedTrains) {
        this.savedTrains = savedTrains;
        clientManager.save();
    }

    public Train getTrainByMessageId(int message_id)
    {
        return savedTrains.get(message_id);
    }

    public ClientPermissions getClientPermissions() {
        return clientPermissions;
    }

    public String getClientUserName() {
        return clientUserName;
    }
}
