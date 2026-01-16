package Web;

public class NoTrainsFoundException extends RuntimeException {
    public NoTrainsFoundException(String message) {
        super(message);
    }
}
