package com.example.scan_test;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Response;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class MyRequest extends com.android.volley.toolbox.StringRequest {

    private final Map<String, String> _params = null;

    /**
     * @param method
     * @param url
     * @param listener
     * @param errorListener
     */
    public MyRequest(int method, String url, Response.Listener<String> listener,
                         Response.ErrorListener errorListener) {
        super(method, url, listener, errorListener);


    }


    @Override
    protected Map<String, String> getParams() {
        return _params;
    }

    /* (non-Javadoc)
     * @see com.android.volley.toolbox.StringRequest#parseNetworkResponse(com.android.volley.NetworkResponse)
     */
    @Override
    protected Response<String> parseNetworkResponse(NetworkResponse response) {
        // since we don't know which of the two underlying network vehicles
        // will Volley use, we have to handle and store session cookies manually
        MyApp.get().checkSessionCookie(response.headers);

        return super.parseNetworkResponse(response);
    }

    /* (non-Javadoc)
     * @see com.android.volley.Request#getHeaders()
     */
    @Override
    public Map<String, String> getHeaders() throws AuthFailureError {
        Map<String, String> headers = super.getHeaders();

        if (headers == null
                || headers.equals(Collections.emptyMap())) {
            headers = new HashMap<String, String>();
        }

        MyApp.get().addSessionCookie(headers);

        return headers;
    }
}