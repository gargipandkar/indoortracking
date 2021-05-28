# indoortracking

### Package dependencies
django==3.0.3  
google-cloud-storage==1.10.0    
django-storages==1.7.1  
keras==2.3.1  
tensorflow==2.1.0^

^if you would like to use the DL models

### Credentials
Add Google Cloud service account key to *mysite* directory.  
Change GS_BUCKET_NAME and GS_CREDENTIALS accordingly.

### Run Django app locally
python manage.py runserver 0.0.0.0:8000  

To run associated [Android app](https://github.com/ohyamn/IndoorTracking), point *MyApp.DOMAIN* to IP address of device running this Django app.  
If unable to reach server, check that port is open or disable Firewall.
