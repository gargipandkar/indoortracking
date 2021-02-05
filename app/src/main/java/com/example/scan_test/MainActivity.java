package com.example.scan_test;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.nfc.Tag;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.util.Log;
import android.view.View;

import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.Comparator;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "Main Activity";
//    private Context context;
//    WifiManager wifiManager;
//
//
//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        setContentView(R.layout.activity_main);
//
//        context = getApplicationContext();
//
//        Button scan_btn = findViewById(R.id.scan_btn);
//        wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
//
//        BroadcastReceiver wifiScanReceiver = new BroadcastReceiver() {
//            @Override
//            public void onReceive(Context c, Intent intent) {
//                boolean success = intent.getBooleanExtra(
//                        WifiManager.EXTRA_RESULTS_UPDATED, false);
//                if (success) {
//                    scanSuccess();
//                } else {
//                    // scan failure handling
//                    scanFailure();
//                }
//            }
//        };
//
//        IntentFilter intentFilter = new IntentFilter();
//        intentFilter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
//        context.registerReceiver(wifiScanReceiver, intentFilter);
//
//        scan_btn.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                boolean success = wifiManager.startScan();
//                if (!success) {
//                    // scan failure handling
//                    scanFailure();
//                }
//            }
//        });
//    }
//
//    private void scanSuccess() {
//        List<ScanResult> results = wifiManager.getScanResults();
//        Log.i(TAG, wifiManager.getConnectionInfo().toString());
//
//        //... use new scan results ...
//        Log.i(TAG, "Scan SUCCESS: "+results.toString());
//    }
//
//    private void scanFailure() {
//        // handle failure: new scan did NOT succeed
//        // consider using old scan results: these are the OLD results!
//        List<ScanResult> results = wifiManager.getScanResults();
//        //... potentially use older scan results ...
//        Log.i(TAG, "Scan FAILURE: "+results.toString());
//    }

    private WifiManager wifiManager;
    private BroadcastReceiver wifiReceiver;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button buttonScan = findViewById(R.id.scan_btn);
        Button buttonGotoBLE = findViewById(R.id.gotoble_btn);
        TextView textWifi = findViewById(R.id.wifi_txt);

        buttonGotoBLE.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent gotoBLE_intent = new Intent(MainActivity.this, BLEScan.class);
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








