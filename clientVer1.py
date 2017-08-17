import serial
import time
import sys
import pymongo
import datetime
import arrow
import requests
import json

def try_float(s):
        try:
                return float(s)
        except:
                return int(s)

ser = serial.Serial("/dev/ttyACM0",9600)
ser.flushInput()

print("sensor")
temperature = 0
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

url = "http://192.168.0.2:30004/deviceinfo/" + "20"
url2 = "http://192.168.0.2:30004/session_number/" + "20"

while True:
        i=0
        values = [ ]
        now = datetime.datetime.now()
        D = arrow.now().format('YYYY-MM-DD')
        T = arrow.now().format('HH:mm:ss')

        response = requests.get(url).json()
        NSamplingTrial = response['NSamplingTrial']
        SamplingInterval = response['SamplingInterval']
        Evaluation = response['Evaluation']
        print Evaluation
        Evaluation = str(Evaluation)
        print type(Evaluation)
        while True:
                vals = ser.readline()
                #vals = try_float(vals)
                print vals
                print type(vals)
                '''
                temp = vals*5.0/1024.0
                cel = (temp-0.5)*100
                '''
                vals = str(vals)
                vals = vals.rstrip()
                cel = eval(vals + Evaluation)
                print 'cel = ' + str(cel)

                values.insert(i, cel)
                print values
                i += 1

                NSamplingTrial -= 1
                if NSamplingTrial == 0:
                        break

        print values

        print "end"

        res = requests.post(url2, data=json.dumps(values))

        try:
                time.sleep(0.5)
        except:
                print("insert failed")
