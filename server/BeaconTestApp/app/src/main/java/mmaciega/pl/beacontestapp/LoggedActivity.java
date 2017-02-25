package mmaciega.pl.beacontestapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class LoggedActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged);
    }

    public void logout(View view) {
        MainActivity.WEBSOCKET.tryGet().end();
        onBackPressed();
    }
}
