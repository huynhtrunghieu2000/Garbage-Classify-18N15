from datetime import datetime
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAjsg2_QADPDyj5AuHt_N3ox5lJJzQcpRk",
    "authDomain": "garbage-app-eed2c.firebaseapp.com",
    "databaseURL": "https://garbage-app-eed2c-default-rtdb.firebaseio.com",
    "projectId": "garbage-app-eed2c",
    "storageBucket": "garbage-app-eed2c.appspot.com",
    "messagingSenderId": "60234969577",
    "appId": "1:60234969577:web:13a61b29de05ea14191b78",
    "measurementId": "G-8S9QM8LB7R"
}

config = {
  "apiKey": "0Vb5hYTFaPwqhP8Hmusbzc69kglwOctMONHuh5Kp",
  "authDomain": "realtime-pi-1.firebaseapp.com",
  "databaseURL": "https://realtime-pi-1-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "realtime-pi-1.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

print("Send Data to Firebase Using Raspberry Pi")
print("—————————————-")

def updateTrashPercent(type,percent):
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
  db.child("trash").child(type).update({"dated": "{}".format(str(dt_string)), "percent": "{}".format(str(percent))})

# db.child("trash").child("inorganic").update({"dated": "10.5.2021", "percent": "59"})
# db.child("trash").child("organic").update({"dated": "10.5.2021", "percent": "59"})
# db.child("mlx90614").child("2-push").push(data)

# time.sleep(2)