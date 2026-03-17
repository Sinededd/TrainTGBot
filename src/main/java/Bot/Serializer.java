package Bot;

import Client.ClientManager;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class Serializer {
    public static void saveClientManager(ClientManager clientManager)
    {
        IO.println("Сохранение...");
        try(ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("saving.dat")))
        {
            oos.writeObject(clientManager);
        }
        catch(Exception ex){

            System.out.println(ex.getMessage());
        }
    }

    public static ClientManager loadClientManager()
    {
        try(ObjectInputStream ois = new ObjectInputStream(new FileInputStream("saving.dat")))
        {
            ClientManager clientManager = (ClientManager) ois.readObject();
            IO.println("Загрузка...");
            return clientManager;
        }
        catch(Exception ex){

            System.out.println(ex.getMessage());
            return null;
        }
    }
}
