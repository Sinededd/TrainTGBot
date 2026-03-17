package Client;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class NotificationManager implements Serializable {

    private static final int PERIOD_SECONDS = 900;

    private static final NotificationManager INSTANCE = new NotificationManager();
    private Set<NotificationSession> sessions = ConcurrentHashMap.newKeySet();
    private transient final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();

    public static NotificationManager getInstance() {
        return INSTANCE;
    }

    private NotificationManager() {
        startScheduler();
    }

    private void startScheduler() {
        scheduler.scheduleAtFixedRate(
                this::processSessions,
                0,
                PERIOD_SECONDS,
                TimeUnit.SECONDS
        );
    }

    private void processSessions() {
        int size = sessions.size();
        if (size == 0) {
            return;
        }

        int stepSeconds = Math.max(1, PERIOD_SECONDS / size);
        int delaySeconds = 0;

        // делаем снапшот, чтобы избежать изменений во время итерации
        List<NotificationSession> snapshot =
                new ArrayList<>(sessions);

        for (NotificationSession session : snapshot) {
            scheduler.schedule(
                    session::sendSignal,
                    delaySeconds,
                    TimeUnit.SECONDS
            );
            delaySeconds += stepSeconds;
        }
    }

    public void addSession(NotificationSession session) {
        sessions.add(session);
    }

    public void removeSession(NotificationSession session) {
        sessions.remove(session);
    }

    public Set<NotificationSession> getSessions() {
        return sessions;
    }

    public void setSessions(Set<NotificationSession> sessions) {
        this.sessions = sessions;
    }
}
