package com.example.scan_test;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.List;

public class WiFiScan extends AppCompatActivity {
    private static final String TAG = "Main Activity";
    private WifiManager wifiManager;
    private BroadcastReceiver wifiReceiver;

    TextView textWifi;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button buttonScan = findViewById(R.id.scan_btn);
        Button buttonGotoBLE = findViewById(R.id.gotoble_btn);
        textWifi = findViewById(R.id.wifi_txt);


         buttonGotoBLE.setOnClickListener(new View.OnClickListener() {
             @Override
             public void onClick(View view) {
                 Intent gotoBLE_intent = new Intent(WiFiScan.this, BLEScan.class);
                 startActivity(gotoBLE_intent);
             }
         });

        wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
        wifiReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                List<ScanResult> results = wifiManager.getScanResults();
                unregisterReceiver(this);

                String display = "";
                for (ScanResult sr: results) {
                    display = display.concat("SSID: "+sr.SSID+", RSSI: "+sr.level+"\n");
                    Log.i(TAG, "SSID: "+sr.SSID+", Level: "+sr.level);
                }
                textWifi.setText(display);
            }
        };

        if (!wifiManager.isWifiEnabled()) {
            Toast.makeText(this, "WiFi needs to be enabled", Toast.LENGTH_SHORT).show();
            wifiManager.setWifiEnabled(true);
        }

        buttonScan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                scanWifi();
            }
        });
    }

    private void scanWifi() {
        registerReceiver(wifiReceiver, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
        boolean success = wifiManager.startScan();
        if (!success){ scanFailed(); }
        Toast.makeText(this, "Scanning...", Toast.LENGTH_SHORT).show();
    }

    private void scanFailed(){
        Toast.makeText(this, "Scan failed", Toast.LENGTH_SHORT).show();
    }
}
