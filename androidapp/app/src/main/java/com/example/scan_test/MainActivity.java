package com.example.scan_test;

import android.app.ProgressDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.nfc.Tag;
import android.os.Bundle;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.util.JsonReader;
import android.util.Log;
import android.view.View;

import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import java.util.ArrayList;
import java.util.BitSet;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "Main Activity";
    private WifiManager wifiManager;
    private BroadcastReceiver wifiReceiver;

    TextView textWifi;
    ImageView imgPlan;

    MyApp myapp = MyApp.get();
    ProgressDialog progressDialog;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button buttonScan = findViewById(R.id.scan_btn);
        Button buttonGotoBLE = findViewById(R.id.gotoble_btn);
        textWifi = findViewById(R.id.wifi_txt);
        imgPlan = findViewById(R.id.plan_img);

        buttonScan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent gotoWifi_intent = new Intent(MainActivity.this, BLEScan.class);
                startActivity(gotoWifi_intent);
            }
        });

        // Trying Android-server API
        final RequestQueue queue = Volley.newRequestQueue(this);
        buttonGotoBLE.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String url = MyApp.Domain + "getplans/";

                progressDialog = new ProgressDialog(MainActivity.this);
                progressDialog.setMessage("Loading..."); // Setting Message
                progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER); // Progress Dialog Style Spinner
                progressDialog.show(); // Display Progress Dialog
                progressDialog.setCancelable(true);

                JsonArrayRequest postRequest = new JsonArrayRequest(Request.Method.POST, url, null,
                        new Response.Listener<JSONArray>() {
                            @Override
                            public void onResponse(JSONArray response) {
                                progressDialog.dismiss();
                                Log.i("JSON Response", "--->" + response);
                                displayResponse(response);
                            }
                        },
                        new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                Log.d("Error.Response", error.toString());
                            }
                        });
                queue.add(postRequest);
            }
        });
    }

    private void displayResponse(JSONArray response){
        ArrayList<String> display = new ArrayList<>();
        for(int i=0; i<response.length(); i++) {
            try{
                display.add(response.getJSONObject(i).getString("title"));
            }catch (Exception e){
                Log.d("Error.Response", e.getMessage());
            }
        }
        textWifi.setText(display.toString());
    }
}








