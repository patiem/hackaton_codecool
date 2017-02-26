package mmaciega.pl.beacontestapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import com.estimote.sdk.Beacon;
import com.estimote.sdk.BeaconManager;
import com.estimote.sdk.Region;
import com.estimote.sdk.SystemRequirementsChecker;
import com.koushikdutta.async.ByteBufferList;
import com.koushikdutta.async.DataEmitter;
import com.koushikdutta.async.callback.DataCallback;
import com.koushikdutta.async.future.Future;
import com.koushikdutta.async.http.AsyncHttpClient;
import com.koushikdutta.async.http.WebSocket;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import static mmaciega.pl.beacontestapp.MainActivity.WEBSOCKET;

public class LoggedActivity extends AppCompatActivity {
    private static final UUID ESTIMOTE_PROXIMITY_UUID = UUID.fromString("B9407F30-F5F8-466E-AFF9-25556B57FE6D");
    private static final Region ALL_ESTIMOTE_BEACONS = new Region("rid", ESTIMOTE_PROXIMITY_UUID, null, null);
    private BeaconManager beaconManager = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged);
        beaconManager = new BeaconManager(getApplicationContext());

        beaconManager.setRangingListener(new BeaconManager.RangingListener() {
            @Override public void onBeaconsDiscovered(Region region, final List<Beacon> beacons) {
                for(final Beacon one_beacon:beacons) {
                    List <Integer> majorsAnswers = Arrays.asList(11593, 23453);
                    int majorReset = 25152;
                    if (majorsAnswers.contains(one_beacon.getMajor())) {

                        AsyncHttpClient.getDefaultInstance().websocket("http://192.170.20.100:8888/ws", null, new AsyncHttpClient.WebSocketConnectCallback() {

                            @Override
                            public void onCompleted(Exception ex, WebSocket webSocket) {
                                if (ex != null) {
//                    Toast.makeText(MainActivity.this, "WYSTAPIL BLAD", Toast.LENGTH_LONG).show();
                                    ex.printStackTrace();
                                    return;
                                }

                                Log.d("All Beacons", "Ranged beacons: " + one_beacon.getMajor());
                                JSONObject jsonObject = new JSONObject();
                                try {
                                    jsonObject.put("username", MainActivity.LOGIN);
                                    jsonObject.put("beaconId", one_beacon.getMajor());
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
//                  Toast.makeText(MainActivity.this, "JEST WEBSOCKET", Toast.LENGTH_LONG).show();
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



                    }
                    else if(majorReset == one_beacon.getMajor()){

                    }
                }

            }

        });

        beaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override public void onServiceReady() {

                // Beacons ranging.
                beaconManager.startRanging(ALL_ESTIMOTE_BEACONS);

                // Nearable discovery.
                beaconManager.startNearableDiscovery();

                // Eddystone scanning.
                beaconManager.startEddystoneScanning();
            }
        });
    }
    @Override
    protected void onResume() {
        super.onResume();

        SystemRequirementsChecker.checkWithDefaultDialogs(this);
    }

    public void logout(View view) {
        WEBSOCKET.tryGet().end();
        onBackPressed();
        beaconManager.disconnect();
    }
}
