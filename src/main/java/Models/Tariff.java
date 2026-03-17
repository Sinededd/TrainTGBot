package Models;

import java.io.Serializable;

public class Tariff implements Serializable {
    private String type;
    private String countPlace;
    private String price;

    Tariff(String type, String countPlace, String price)
    {
        this.type = type;
        this.countPlace = countPlace;
        this.price = price;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getCountPlace() {
        return countPlace;
    }

    public void setCountPlace(String countPlace) {
        this.countPlace = countPlace;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }
}
