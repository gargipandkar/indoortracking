package com.example.scan_test;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.nfc.Tag;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import org.w3c.dom.Text;

import java.util.List;

public class BLEScan extends AppCompatActivity {
    private static String TAG = "BLEScan";
    BluetoothManager bluetoothManager;
    BluetoothAdapter bluetoothAdapter;

    String display;
    Button buttonScan;
    TextView textBLE;

    BluetoothAdapter.LeScanCallback bleCallback = new BluetoothAdapter.LeScanCallback() {
        @Override
        public void onLeScan(BluetoothDevice bluetoothDevice, int i, byte[] bytes) {
            display = display.concat("Device: "+bluetoothDevice.toString()+", RSSI: "+i+"\n");
            textBLE.setText(display);
            Log.i(TAG, bluetoothDevice.toString()+", "+i+", "+bytes);
            bluetoothAdapter.stopLeScan(bleCallback);
        }
    };

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ble);

        buttonScan = findViewById(R.id.ble_btn);
        display = "";
        textBLE = findViewById(R.id.ble_txt);

        boolean setup = setupBLE();

        buttonScan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (setup){ scanBLE(); }
            }
        });

    }

    void scanBLE(){
//            registerReceiver(bleReceiver, new IntentFilter(BluetoothDevice.ACTION_FOUND));
//            bluetoothAdapter.startDiscovery();

            bluetoothAdapter.startLeScan(bleCallback);

    }

    private final BroadcastReceiver bleReceiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (BluetoothDevice.ACTION_FOUND.equals(action)){
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                Log.i(TAG, "Bluetooth device: "+device.toString());
            }
            unregisterReceiver(bleReceiver);
            bluetoothAdapter.cancelDiscovery();
        }
    };


    boolean setupBLE(){
        bluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        bluetoothAdapter = bluetoothManager.getAdapter();
        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled()) {
            Log.i(TAG, "Device does not support Bluetooth or Bluetooth is not enabled");
            return false;
        }
        return true;
    }
}
