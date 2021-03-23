package com.example.scan_test;

import android.app.ProgressDialog;
import android.content.Context;
import android.net.wifi.ScanResult;
import android.util.Log;
import android.widget.ListAdapter;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.StringRequest;
import com.google.api.gax.httpjson.HttpJsonCallOptions;

import org.json.JSONArray;
import java.util.HashMap;

public class APIRequests {
    public static Request<JSONArray> getAllPlans(Context ctx, String base_url, HashMap<String, String> allPlans){
        ProgressDialog progressDialog = new ProgressDialog(ctx);
        progressDialog.setMessage("Loading...");
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        progressDialog.setCancelable(true);

        String url = base_url+"/api";
        String bucket_url = "https://storage.googleapis.com/floorplan-images/";
        JsonArrayRequest getRequest = new JsonArrayRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressDialog.dismiss();
                        Log.i("JSON RESPONSE", "--->" + response);

                        for(int i=0; i<response.length(); i++) {
                            try{
                                String title = response.getJSONObject(i).getString("title");
                                String img = response.getJSONObject(i).getString("plan");
                                allPlans.put(title, bucket_url+img);
                            } catch (Exception e){
                                Log.d("Error.Response", e.getMessage());
                            }
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("RESPONSE ERROR", error.toString());
                    }
                });

        return getRequest;
    }

    public static StringRequest login(Context ctx, String base_url, String username, String password){
        ProgressDialog progressDialog = new ProgressDialog(ctx);
        progressDialog.setMessage("Loading...");
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        progressDialog.setCancelable(true);

        String url = base_url+"/login";
        StringRequest postRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        progressDialog.dismiss();
                        Log.i("STRING RESPONSE", "--->" + response);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("RESPONSE ERROR", error.toString());
                    }
                }
                ) {
                    @Override
                    protected HashMap<String, String> getParams() {
                        HashMap<String, String> params = new HashMap<String, String>();
                        params.put("username", username);
                        params.put("password", password);
                        return params;
                    }
        };

        return postRequest;
    }

    public static Request<JSONArray> sendMapping(Context ctx, String base_url){
        ProgressDialog progressDialog = new ProgressDialog(ctx);
        progressDialog.setMessage("Loading...");
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        progressDialog.setCancelable(true);

        JSONArray mapped_data = null;

        String url = base_url+"/api";
        JsonArrayRequest postRequest = new JsonArrayRequest(Request.Method.POST, url, mapped_data,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        progressDialog.dismiss();
                        Log.i("STRING RESPONSE", "--->" + response);
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
