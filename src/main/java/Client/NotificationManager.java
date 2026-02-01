package Client;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class NotificationManager {

    private static final int PERIOD_SECONDS = 300;

    private static final NotificationManager INSTANCE = new NotificationManager();
    private final Set<NotificationSession> sessions = ConcurrentHashMap.newKeySet();
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();

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
}
