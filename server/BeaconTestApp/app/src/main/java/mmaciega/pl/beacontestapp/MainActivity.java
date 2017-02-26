package mmaciega.pl.beacontestapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import com.koushikdutta.async.ByteBufferList;
import com.koushikdutta.async.DataEmitter;
import com.koushikdutta.async.callback.DataCallback;
import com.koushikdutta.async.future.Future;
import com.koushikdutta.async.http.AsyncHttpClient;
import com.koushikdutta.async.http.WebSocket;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;

public class MainActivity extends AppCompatActivity {

    public static Future<WebSocket> WEBSOCKET;
    public static String LOGIN;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

    }

    public void loginToGame(View v) {
        EditText viewById = (EditText) this.findViewById(R.id.loginEditText);

        LOGIN = viewById.getText().toString();

        if (LOGIN != null && !LOGIN.isEmpty()) {
            WEBSOCKET = AsyncHttpClient.getDefaultInstance().websocket("http://192.170.20.100:8888/ws", null, new AsyncHttpClient.WebSocketConnectCallback() {

                @Override
                public void onCompleted(Exception ex, WebSocket webSocket) {
                    if (ex != null) {
//                    Toast.makeText(MainActivity.this, "WYSTAPIL BLAD", Toast.LENGTH_LONG).show();
                        ex.printStackTrace();
                        return;
                    }

                    JSONObject jsonObject = new JSONObject();
                    try {
                        jsonObject.put("username", LOGIN);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
//                Toast.makeText(MainActivity.this, "JEST WEBSOCKET", Toast.LENGTH_LONG).show();
                    webSocket.send(jsonObject.toString());

                    webSocket.setStringCallback(new WebSocket.StringCallback() {
                        public void onStringAvailable(String s) {
//                        Toast.makeText(MainActivity.this, "I got a string: " + s, Toast.LENGTH_LONG).show();
                            System.out.println("I got a string: " + s);
                        }
                    });
                    webSocket.setDataCallback(new DataCallback() {
                        public void onDataAvailable(DataEmitter emitter, ByteBufferList byteBufferList) {
//                        Toast.makeText(MainActivity.this, "I got some bytes!", Toast.LENGTH_LONG).show();

                            System.out.println("I got some bytes!");
                            // note that this data has been read
                            byteBufferList.recycle();
                        }
                    });
                }
            });

            try {
                if (WEBSOCKET.get() != null) {
                    Intent intent = new Intent(getApplicationContext(), LoggedActivity.class);
                    startActivity(intent);

                }
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }
    }
}