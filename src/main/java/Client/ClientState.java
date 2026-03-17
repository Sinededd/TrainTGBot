package Client;

import java.io.Serializable;

public enum ClientState implements Serializable {
    DEFAULT, WAITING_FROM_STATION, WAITING_TO_STATION, WAITING_DATE
}
