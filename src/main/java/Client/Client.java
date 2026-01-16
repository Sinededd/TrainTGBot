package Client;

import Models.Train;

import java.time.LocalDate;
import java.util.*;

public class Client {
    private final Long id;
    private ClientState clientState;
    private String fromStation = "";
    private String toStation = "";
    private LocalDate date = LocalDate.now();
    private Map<Integer, Train> savedTrains = new HashMap<>();
    private final List<NotificationSession> sessionList;

    public Client(long id)
    {
        this.id = id;
        clientState = ClientState.DEFAULT;
        sessionList = new ArrayList<>();
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
        ArrayList<Train> trains = new ArrayList<>(sessionList.size());
        for(NotificationSession session : sessionList)
        {
            trains.add(session.getTrain());
        }
        return trains;
    }

    public NotificationSession addSession(Train train)
    {
        NotificationSession newSession = new NotificationSession(this, train);
        sessionList.add(newSession);
        return newSession;
    }

    public void stopSession(NotificationSession session) {
        session.stop();
        sessionList.remove(session);
    }

    public void stopSession(Train train)
    {
        for(NotificationSession session : sessionList)
        {
            if(Objects.equals(session.getTrain().getId(), train.getId()))
            {
                session.stop();
                sessionList.remove(session);
                return;
            }
        }
    }

    public boolean checkSession(String trainId)
    {
        for(NotificationSession session : sessionList)
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
    }

    public Train getTrainByMessageId(int message_id)
    {
        return savedTrains.get(message_id);
    }

}
