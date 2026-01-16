package Models;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeFormatterBuilder;

public class Train {

    private final String trainNumber;
    private final LocalDate date;
    private final String route;
    private final String depTime;
    private final String depStation;
    private final String arrTime;
    private final String arrStation;
    private final String duration;
    private final String id;
    private final Tariffs tariffs;


    private Train(Builder builder) {
        this.trainNumber = builder.trainNumber;
        this.date = builder.date;
        this.route = builder.route;
        this.depTime = builder.depTime;
        this.depStation = builder.depStation;
        this.arrTime = builder.arrTime;
        this.arrStation = builder.arrStation;
        this.duration = builder.duration;
        this.id = builder.id;
        this.tariffs = builder.tariffs;
    }

    public String getTrainNumber() {
        return trainNumber;
    }

    public LocalDate getLocalDate() {
        return date;
    }

    public String getRoute() {
        return route;
    }

    public String getDepTime() {
        return depTime;
    }

    public String getDepStation() {
        return depStation;
    }

    public String getArrTime() {
        return arrTime;
    }

    public String getArrStation() {
        return arrStation;
    }

    public String getDuration() {
        return duration;
    }

    public String getId() {
        return id;
    }

    public Tariffs getTariffs() {
        return tariffs;
    }

    public String toString()
    {
        return ("Поезд: " + trainNumber +
                "\nДата: " + date.format(DateTimeFormatter.ofPattern("dd.MM.yyyy")) +
                "\nМаршрут: " + route +
                "\n" + depStation + " " + depTime + " → " + arrStation + " " + arrTime +
                "\nВ пути: " + duration +
                "\n`────────────────────────────`" +
                "\n" + (tariffs.isEmpty() ? "Билетов нет" : tariffs.toString()))
                .replace("-", "\\-")
                .replace(".", "\\.");
    }

    public static class Builder {
        private String trainNumber = "";
        private LocalDate date = LocalDate.EPOCH;
        private String route = "";
        private String depTime = "";
        private String depStation = "";
        private String arrTime = "";
        private String arrStation = "";
        private String duration = "";
        private String id = "";
        private Tariffs tariffs = new Tariffs();

        public Builder trainNumber(String trainNumber) {
            this.trainNumber = trainNumber;
            return this;
        }

        public Builder date(LocalDate date) {
            this.date = date;
            return this;
        }

        public Builder route(String route) {
            this.route = route;
            return this;
        }

        public Builder depTime(String depTime) {
            this.depTime = depTime;
            return this;
        }

        public Builder depStation(String depStation) {
            this.depStation = depStation;
            return this;
        }

        public Builder arrTime(String arrTime) {
            this.arrTime = arrTime;
            return this;
        }

        public Builder arrStation(String arrStation) {
            this.arrStation = arrStation;
            return this;
        }

        public Builder duration(String duration) {
            this.duration = duration;
            return this;
        }

        public Builder id(String id)
        {
            this.id = id;
            return this;
        }

        public Builder tariffs(Tariffs tariffs) {
            this.tariffs = tariffs;
            return this;
        }

        public Train build() {
            return new Train(this);
        }
    }
}

