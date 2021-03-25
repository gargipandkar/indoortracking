package com.example.scan_test;

import android.app.ProgressDialog;
import android.content.Context;
import android.net.wifi.ScanResult;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class FloorplanScanner{
    private List<ScanPoint> allScanResults;
    private List<Double> predictedLocation;

    public FloorplanScanner() {
        allScanResults = new ArrayList<>();
        predictedLocation = new ArrayList<>();
    }

    public static FloorplanScanner getInstance() {
        return new FloorplanScanner();
    }

    public void findPoint(List<ScanResult> scanResultList){
        ScanPoint point = new ScanPoint(0, 0); // placeholder coordinates
        Map<String, ArrayList<Integer>> SSIDList = new HashMap<>();
        for(ScanResult scanResult: scanResultList){
            String id = scanResult.SSID;
            if (id.equals("")){ continue; } // skip hidden or unknown network names
            id = id+"/"+scanResult.BSSID;
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

    }

    public void mapPoint(double x, double y, List<ScanResult> scanResultList){
        ScanPoint point = new ScanPoint(x, y);
        Map<String, ArrayList<Integer>> SSIDList = new HashMap<>();
        for(ScanResult scanResult: scanResultList){
            String id = scanResult.SSID;
            if (id.equals("")){ continue; } // skip hidden or unknown network names
            id = id+"/"+scanResult.BSSID;
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

    public JSONArray sendResults() throws JSONException {
        JSONArray allJSONresults = new JSONArray();
        for(ScanPoint point: allScanResults){
            JSONObject obj = new JSONObject();
            obj.put("point", point.getPoint());
            obj.put("vector", point.getVector());
            allJSONresults.put(obj);
        }

        return allJSONresults;
    }

    public Request<JSONArray> getLocation(Context ctx, String base_url){
        JSONArray mapped_data;
        try {
            mapped_data = sendResults();
            Log.i("REQUEST DATA", mapped_data.toString());
        } catch (JSONException e){
            Log.i("JSON EXCEPTION", e.toString());
            return null;
        }

        ProgressDialog progressDialog = new ProgressDialog(ctx);
        progressDialog.setMessage("Loading...");
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        progressDialog.setCancelable(true);

        String url = base_url+"getlocation/";
        JsonArrayRequest postRequest = new JsonArrayRequest(Request.Method.POST, url, mapped_data,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressDialog.dismiss();
//                        Log.i("JSON RESPONSE", "--->" + response);
                        try {
                            predictedLocation.add(response.getDouble(0));
                            predictedLocation.add(response.getDouble(1));
                            Log.i("PREDICTED LOCATION", predictedLocation.toString());
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("RESPONSE ERROR", error.toString());
                    }
                }
        );

        return postRequest;
    }

    public Request<JSONArray> sendMapping(Context ctx, String base_url){
        JSONArray mapped_data;
        try {
            mapped_data = sendResults();
            Log.i("REQUEST DATA", mapped_data.toString());
        } catch (JSONException e){
            Log.i("JSON EXCEPTION", e.toString());
            return null;
        }

        ProgressDialog progressDialog = new ProgressDialog(ctx);
        progressDialog.setMessage("Loading...");
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        progressDialog.setCancelable(true);

        String url = base_url+"savemapping/";
        JsonArrayRequest postRequest = new JsonArrayRequest(Request.Method.POST, url, mapped_data,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressDialog.dismiss();
                        Log.i("JSON RESPONSE", "--->" + response);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("RESPONSE ERROR", error.toString());
                    }
                }
        );

        return postRequest;
    }
}

class ScanPoint {
    private double x;
    private double y;
    private ArrayList<Object> vector;

    ScanPoint(double x, double y){
        this.x = x;
        this.y = y;
        vector = new ArrayList<>();
    }

    void addAllAPs(Map<String, ArrayList<Integer>> SSIDList){
        for(String id: SSIDList.keySet()){
            if(!id.equals("")) {
                ScanAP ap = new ScanAP(id, SSIDList.get(id));
                vector.add(ap.getSSID());
                vector.add(ap.getAvgRSSI());
            }
        }
    }

    String getPoint(){ return x+","+y; }

    ArrayList<Object> getVector(){ return vector; }
}

class ScanAP{
    private String id;
    private int avgRSSI;

    ScanAP(String id, ArrayList<Integer> value_list){
        this.id = id;
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

    public int getAvgRSSI() {
        return avgRSSI;
    }

    public String getSSID() {
        return id;
    }

    public HashMap<String, Integer> toHashMap(){
        HashMap<String, Integer> result = new HashMap<>();
        result.put(id, avgRSSI);
        return result;
    }
}

