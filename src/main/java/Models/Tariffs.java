package Models;

import java.util.ArrayList;
import java.util.List;

public class Tariffs {
    private final List<Tariff> tariffList;

    public Tariffs()
    {
        this.tariffList = new ArrayList<>();
    }

    public Tariffs(ArrayList<Tariff> tariffs)
    {
        this.tariffList = tariffs;
    }

    public void addTariff(Tariff tariff)
    {
        tariffList.add(tariff);
    }

    public void addTariff(String type, String countPlace, String price)
    {
        tariffList.add(new Tariff(type, countPlace, price));
    }

    public boolean removeTariff(Tariff tariff) {
        return tariffList.remove(tariff);
    }

    public boolean removeTariff(int index) {
        if (index >= 0 && index < tariffList.size()) {
            tariffList.remove(index);
            return true;
        }
        return false;
    }

    public Tariff getTariff(int index) {
        if (index >= 0 && index < tariffList.size()) {
            return tariffList.get(index);
        }
        return null;
    }

    public List<Tariff> getAllTariffs() {
        return new ArrayList<>(tariffList);
    }

    public int size() {
        return tariffList.size();
    }

    public boolean isEmpty() {
        return tariffList.isEmpty();
    }

    public void clear() {
        tariffList.clear();
    }

    @Override
    public String toString() {
        int typeWidth = "Тип".length();
        int placesWidth = "Мест: 0".length();
        int priceWidth = "Цена: 0".length();
        for(Tariff tariff : tariffList)
        {
            typeWidth = Math.max(typeWidth, tariff.getType().length());
            placesWidth = Math.max(placesWidth, ("Мест: " + tariff.getCountPlace()).length());
            priceWidth = Math.max(priceWidth, ("Цена: " + tariff.getPrice()).length());
        }

        StringBuilder strBuilder = new StringBuilder();
        for(Tariff tariff : tariffList)
        {
            strBuilder.append(String.format("`%-" + (typeWidth) + "s | %-" + (placesWidth) + "s | %-" + priceWidth + "s`\n",
                    tariff.getType(),
                    "мест: " + tariff.getCountPlace(),
                    "цена: " + tariff.getPrice()));
        }
        return strBuilder.toString();
    }
}
