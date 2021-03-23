package com.example.scan_test;

import android.net.wifi.ScanResult;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class FloorplanScanner{
    private List<ScanPoint> allScanResults;

    public static FloorplanScanner getInstance() {
        return new FloorplanScanner();
    }

    public void mapPoint(double x, double y, List<ScanResult> scanResultList){
        ScanPoint point = new ScanPoint(x, y);
        Map<String, ArrayList<Integer>> SSIDList = new HashMap<>();
        for(ScanResult scanResult: scanResultList){
            String id = scanResult.SSID;
            Integer value = scanResult.level;
            ArrayList<Integer> value_list = new ArrayList<>();
            if (SSIDList.containsKey(id))
                value_list = SSIDList.get(id);

            if (value_list != null) {
                value_list.add(value);
            }
            SSIDList.put(id, value_list);
        }

        point.addAllAPs(SSIDList);
        allScanResults.add(point);
    }

    public void sendResults() throws JSONException {
        JSONArray allJSONresults = new JSONArray();
        for(ScanPoint point: allScanResults){
            JSONObject obj = new JSONObject();
            obj.put("point", point.getPoint());
            obj.put("vector", point.getVector());
            allJSONresults.put(obj);
        }
    }
}

class ScanPoint {
    private double x;
    private double y;
    private ArrayList<ScanAP> vector;

    ScanPoint(double x, double y){
        this.x = x;
        this.y = y;
        vector = new ArrayList<>();
    }

    void addAllAPs(Map<String, ArrayList<Integer>> SSIDList){
        for(String id: SSIDList.keySet()){
            ScanAP ap = new ScanAP(id, SSIDList.get(id));
            vector.add(ap);
        }
    }

    double[] getPoint(){
        return new double[]{x, y};
    }

    ArrayList<ScanAP> getVector(){
        return vector;
    }
}

class ScanAP{
    private String SSID;
    private int avgRSSI;

    ScanAP(String id, ArrayList<Integer> value_list){
        SSID = id;
        avgRSSI = calculateAvgRSSI(value_list);
    }

    private int calculateAvgRSSI(ArrayList<Integer> value_list){
        int avg = 0;
        if(value_list.isEmpty()) { return avg; }
        for(Integer value: value_list){
            avg +=value;
        }
        avg = avg/value_list.size();
        return avg;
    }

    public HashMap<String, Integer> toHashMap(){
        HashMap<String, Integer> result = new HashMap<>();
        result.put(SSID, avgRSSI);
        return result;
    }
}
