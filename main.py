from urllib import request
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import configparser
import requests
from datetime import datetime, timezone, time, timedelta, date
import time
import string

# Define config

config = configparser.ConfigParser()
config.read('config.ini')

bucket = config['INFLUX']['bucket']
org = config['INFLUX']['org']
token = config['INFLUX']['token']
url = config['INFLUX']['url']


# calcul to define week report
today = date.today()
valueDate = today.weekday() + 3
lastThursday = (today - timedelta(valueDate))
plusSeven = lastThursday + timedelta(7)

lt = int(time.mktime(lastThursday.timetuple()))
p7 = int(time.mktime(plusSeven.timetuple()))

# Influx connection

client = InfluxDBClient(url=url,token=token,org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Fonction to get value on serenicity api (get flux)

def reqCount(p_user):
    var_user = p_user
    r = requests.get(config['LASTFM_API']['url'], params={ "user": var_user, "api_key": config["LASTFM_API"]["access_token"], "method": "user.getWeeklyTrackChart","format": "json","from": lt, "to": p7 })
    return r


# Fonction to write into bucket a value

def writeIntoBucket(p_count, p_tag):
    var_count = p_count
    var_tag = p_tag
    r = Point("ScrobblesTotal").tag("user", var_tag).field("value", var_count)
    write_api.write(bucket, org, r)


# Request Serenicity API



user = config['LASTFM_API']['user'].split()
# Write into bucket (fiest value json count string transform into int, second it's just a tag)


for i in user:
    getUserScrobbles = reqCount(i)  
    ScrobblesData = getUserScrobbles.json() 
    var_result = 0
    for k in ScrobblesData['weeklytrackchart']['track']:
        var_result = var_result + int(k['playcount'])
    writeIntoBucket(int(var_result), i)






