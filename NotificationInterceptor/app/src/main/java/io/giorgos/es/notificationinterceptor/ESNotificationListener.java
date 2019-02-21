package io.giorgos.es.notificationinterceptor;

import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class ESNotificationListener extends NotificationListenerService {

    @Override
    public void onNotificationPosted(StatusBarNotification notification) {
        try {
            Log.d("ESNL", "Sending...");
            URL url = new URL("http://es.giorgos.io:8080/api/notifications");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            String body = "1";
            byte[] bodyBytes = body.getBytes(StandardCharsets.UTF_8);
            OutputStream os = con.getOutputStream();
            os.write(bodyBytes);
            os.close();

            int resp = con.getResponseCode();
            Log.d("ESNL", "Response Code: " + resp);
            con.disconnect();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

