package Bot;

import io.github.cdimascio.dotenv.Dotenv;

public class Config {
    private static final Dotenv dotenv = Dotenv.configure()
            .directory("./")
            .ignoreIfMissing()
            .load();

    public static String getBotToken() {
        return dotenv.get("TELEGRAM_BOT_TOKEN");
    }
}