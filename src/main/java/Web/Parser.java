package Web;

import Models.Tariffs;
import Models.Train;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.util.ArrayList;

public class Parser {
    public static ArrayList<Train> getTrains(String stationFrom, String stationTo, LocalDate date) throws NoTrainsFoundException
    {
        ArrayList<Train> trainList = new ArrayList<>();
        try {
            Document doc = Jsoup.connect("https://pass.rw.by/ru/route")
                    .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/143.0.0.0")
                    .referrer("https://www.google.com")
                    .data("from", stationFrom)
                    .data("from_exp", "")
                    .data("from_esr", "")
                    .data("to", stationTo)
                    .data("to_exp", "")
                    .data("to_esr", "")
                    .data("front_date", "")
                    .data("date", date.toString())
                    .get();
//            File input = new File("page.html");
//            Document doc = Jsoup.parse(input, "UTF-8");


            //Get data of trains
            Elements trains = doc.select("div.sch-table__row-wrap.js-row");
            if(trains.isEmpty())
            {
                String errStr = doc.select(".h3").text();
                IO.println("Ошибка: " + errStr);
                if(errStr.contains("Пожалуйста, укажите пункт отправления / прибытия"))
                {
                    throw new NoTrainsFoundException("Неверно указаны пункты отправления / прибытия");
                }
                errStr = doc.select(".error_title").text();
                IO.println("Ошибка: " + errStr);
                if(errStr.contains("Информация о расписании движения поездов и стоимости проезда на указанную дату недоступна"))
                {
                    throw new NoTrainsFoundException("Информация о расписании движения поездов и стоимости проезда на указанную дату недоступна");
                }
            }

            for (Element train : trains) {
                Element element = train.selectFirst(".train-number");
                String trainNumber = element != null ? element.text() : "";

                element = train.selectFirst(".train-route");
                String route = element != null ? element.text() : "";

                element = train.selectFirst(".train-from-time");
                String depTime = element != null ? element.text() : "";

                element = train.selectFirst(".train-from-name");
                String depStation = element != null ? element.text() : "";

                element = train.selectFirst(".train-to-time");
                String arrTime = element != null ? element.text() : "";

                element = train.selectFirst(".train-to-name");
                String arrStation = element != null ? element.text() : "";

                element = train.selectFirst(".train-duration-time");
                String duration = element != null ? element.text() : "";

                element = train.selectFirst(".sch-table__row");
                String trainId = element != null ? element.attr("data-train-id") : "";



                //Getting tariffs
                Tariffs tariffs = new Tariffs();
                Elements tickets = train.select(".sch-table__t-item");

                for (Element ticket : tickets) {
                    Element typeElement = ticket.selectFirst(".sch-table__t-name");
                    String type = "";
                    if (typeElement != null && !typeElement.text().isEmpty()) {
                        type = typeElement.text();
                    } else if (ticket.selectFirst("i.svg-tag-bicycle--quantity") != null) {
                        type = "Вело";
                    }
                    type = type.length() > 8 ? type.substring(0, 8) : type;

                    element = ticket.selectFirst(".sch-table__t-quant span");
                    String places =  element != null ? element.text() : "";

                    element = ticket.selectFirst(".ticket-cost");
                    String price = element != null ? element.text() : "";

                    tariffs.addTariff(type, places, price);
                }

                trainList.add(new Train.Builder()
                        .trainNumber(trainNumber)
                        .date(date)
                        .route(route)
                        .depTime(depTime)
                        .depStation(depStation)
                        .arrTime(arrTime)
                        .arrStation(arrStation)
                        .duration(duration)
                        .id(trainId)
                        .tariffs(tariffs)
                        .build());
            }

//            FileWriter writer = new FileWriter("page.html");
//            writer.write(doc.html());
//            writer.close();
//
//            FileWriter writerTrains = new FileWriter("trains.html");
//            writerTrains.write(trains.html());
//            writerTrains.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
        return trainList;
    }
}
