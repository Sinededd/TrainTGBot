package Client;

import Models.Train;

import java.io.Serializable;
import java.time.LocalDate;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class Client implements Serializable {
    private final Long id;
    private ClientState clientState;
    private String fromStation = "";
    private String toStation = "";
    private LocalDate date = LocalDate.now();
    private Map<Integer, Train> savedTrains = new HashMap<>(); // <messageId, train>
    private final Set<NotificationSession> sessions = ConcurrentHashMap.newKeySet();


    public Client(long id)
    {
        this.id = id;
        clientState = ClientState.DEFAULT;
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

    public ArrayList<Train> getSubscribedTrains()
    {
        ArrayList<Train> trains = new ArrayList<>(sessions.size());
        for(NotificationSession session : sessions)
        {
            trains.add(session.getTrain());
        }
        return trains;
    }
///// ///////////////////////////////////////
    public NotificationSession addSession(Train train)
    {
        NotificationSession newSession = new NotificationSession(this, train);
        sessions.add(newSession);
        return newSession;
    }

    public void stopSession(NotificationSession session) {
        session.stop();
        sessions.remove(session);
    }

    public void stopSession(Train train)
    {
        for(NotificationSession session : sessions)
        {
            if(Objects.equals(session.getTrain().getId(), train.getId()))
            {
                session.stop();
                sessions.remove(session);
                return;
            }
        }
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
///// /////////////////////////////////////

    public Map<Integer, Train> getSavedTrains() {
        return savedTrains;
    }

    public void setSavedTrains(Map<Integer, Train> savedTrains) {
        this.savedTrains = savedTrains;
    }

    public Train getTrainByMessageId(int message_id)
    {
        return savedTrains.get(message_id);
    }

}
