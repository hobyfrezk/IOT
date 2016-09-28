import httplib, urllib
import os
import datetime
import json
import time

# field1: user attendence, field2: light sensor, field3: led working state
def update(field, data):
    #update user's behavior
    if field == "user":
        params1 = urllib.urlencode({'field1':data, 'key':'NXCLG7W3AQVRDBL1'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params1, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
    #update lightsensor's data
    if field == "light":
        params2 = urllib.urlencode({'field2':data, 'key':'NXCLG7W3AQVRDBL1'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params2, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
    #update led working state
    if field == "led":
        params3 = urllib.urlencode({'field3':data, 'key':'NXCLG7W3AQVRDBL1'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        conn.request("POST", "/update", params3, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
    



def mkjsondata():
    os.chdir("/home/pi/IOT/temp")
    rawdata = {}
    data= {}

    rawdata["time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for filename in ["userlog.txt", "lightlog.txt", "modelog.txt","ledlog.txt"]:
        rawdata[filename[0:-7]] = file(filename, "r").readlines()[-1][27:]

    with open("database.txt", "r") as f:
        data = json.load(f)
        data[int(max(data.keys(), key = int))+1] = rawdata
       
    with open("database.txt", "w") as f:
        json.dump(data,f)

    print "done"
    time.sleep(5)


def update2thgspk():
        os.chdir("/home/pi/IOT/temp")
        with open("database.txt", "r") as f:
           data = json.load(f)
        #only update newest state
        rdytoupdate = data[max(data.keys(), key = int)]
        update("user", str(rdytoupdate["user"]))
        time.sleep(2)
        update("light", str(rdytoupdate["light"]))
        time.sleep(2)
        update("led", str(rdytoupdate["led"]))
        time.sleep(2)


while True:
    mkjsondata()
    update2thgspk()


