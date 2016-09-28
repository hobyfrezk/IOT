import os,datetime,time
import json

#if error in updating database file, can be initilzed by running this script


rawdata = {}
data= {}

rawdata["time"]= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for key in ["user", "light", "mode","led"]:
    rawdata[key] = "==="

data[0] = rawdata

with open("database.txt", "w") as f:
     json.dump(data, f)
