package com.daandtu.smarthome;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.util.SparseArray;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.*;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity implements Sock.OnCreatedListener, Sock.OnMessageListener {

    Button verb;
    RelativeLayout control;
    TextView tvVerbindungen;

    Context context;
    Sock s;

    static SparseArray<String> ID_LIST = new SparseArray<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_INDETERMINATE_PROGRESS);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_main);
        context = this;

        verb = findViewById(R.id.verb);
        tvVerbindungen = findViewById(R.id.TVverbindungen);
        control = findViewById(R.id.controlView);
        findViewById(R.id.radio_volume_up).setOnLongClickListener(longClickListener);
        findViewById(R.id.radio_volume_down).setOnLongClickListener(longClickListener);

        ID_LIST.put(R.id.radio_onOff, "ro");
        ID_LIST.put(R.id.radio_volume_up, "ru");
        ID_LIST.put(R.id.radio_volume_down, "rd");
        ID_LIST.put(R.id.radio_portable, "rp");
        ID_LIST.put(R.id.radio_radio, "rr");
        ID_LIST.put(R.id.radio_left, "rl");
        ID_LIST.put(R.id.radio_right, "rh");
    }

    public void con (View v){
        setProgressBarIndeterminateVisibility(true);
        s = new Sock(context);
        s.setOnCreatedListener(this);
        s.setOnMessageListener(this);
        s.create();
    }

    public void radioButton(View view){
        s.write("su" + ID_LIST.get(view.getId()));
    }

    @Override
    public void created(final boolean success, final Exception e) {
        runOnUiThread(() -> {
            setProgressBarIndeterminateVisibility(false);
            if (success){
                verb.setVisibility(View.GONE);
                control.setVisibility(View.VISIBLE);
                // s.write("aPASSWORD"); // Send authentication
            }else{
                if (e.getMessage().contains("ECONNREFUSED")){
                    Toast.makeText(context, R.string.server_not_available, Toast.LENGTH_SHORT).show();
                }else if (e.getMessage().contains("ENETUNREACH")){
                    Toast.makeText(context, R.string.no_internet_connection, Toast.LENGTH_SHORT).show();
                }else {
                    Toast.makeText(context, R.string.verb_fehlgeschlagen, Toast.LENGTH_SHORT).show();
                }
                s = null;
                verb.setVisibility(View.VISIBLE);
            }
        });
    }

    View.OnLongClickListener longClickListener = new View.OnLongClickListener() {
        @Override
        public boolean onLongClick(View view) {
            s.write("su" + ID_LIST.get(view.getId()) + "l");
            return true;
        }
    };

    @Override
    public void onResume(){
        super.onResume();
        con(null);
    }
    @Override
    public void onPause(){
        s.close();
        s = null;
        control.setVisibility(View.GONE);
        super.onPause();
    }

    @Override
    public void gotMessage(String message) {
        Log.i("Logmsg", message);
        runOnUiThread(() -> {
            if (message.charAt(0) == 'a'){
                s.write("c");
                s.write("tm");
                s.write("tc");
            }else if (message.charAt(0) == 'c'){
                tvVerbindungen.setVisibility(View.VISIBLE);
                tvVerbindungen.setText(String.format("%s %s", message.replace("c", "").replace("+",""), getString(R.string.server_verbindungen)));
            }
        });
    }


}
