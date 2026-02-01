package Bot;

import Client.ClientManager;

import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

public class Serializer {
    public static void saveClientManager(ClientManager clientManager)
    {
        try(ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("saving.dat")))
        {
            oos.writeObject(clientManager);
        }
        catch(Exception ex){

            System.out.println(ex.getMessage());
        }
    }
}
