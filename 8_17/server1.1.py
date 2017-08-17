import psycopg2
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json

class LocalData(object):
	records= {}
class MyHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        try:
            self._set_headers()
		
	    #params = urllib.urlencode({'temperature':10})
            #self.wfile.write(params)
	    if None != re.search('/deviceinfo/*', self.path):
		deviceID = self.path.split('/')[-1]
		#if LocalData.records.has_key(deviceID):
		print deviceID
		#self.wfile.write(LocalData.records[deviceID])
		self.read_db(deviceID)

		try:
            	    conn = psycopg2.connect("host='localhost' dbname='postgres' user=postgres password='6105'")
            	    conn.autocommit = True
        	except:
        	    print "not connect"

        	cur=conn.cursor()
        	try:
		    params = []
		    i=0
        	    print deviceID
        	    cur.execute("SELECT * FROM Device_Profile WHERE id=%s",(deviceID,))
		    rows = cur.fetchall()
		    print rows
		    for row in rows:
			data = {'SamplingInterval':row[5],'NSamplingTrial':row[6], 'Evaluation':row[3]}		 
		    print data   
		    params = json.dumps(data)
		    self.wfile.write(params)
        	    print params
        	except:
        	    print "cannot SQL Execute"
	
	        conn.commit()
	        cur.close()
	        conn.close()


        except IOError:
            self.send_error(404, 'File Not Found')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
	if None != re.search('/session_number/*', self.path):
		recordID= self.path.split('/')[-1]
		print recordID
        print "in post method"
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        print data_string
	self.insert_db(data_string)
	

    def insert_db(self, data_x):
	try:
	    conn = psycopg2.connect("host='localhost' dbname='postgres' user=postgres password='6105'")
	    conn.autocommit = True
	    print 1 
	except:
	    print "not connect"

	cur=conn.cursor()
	try:
	    #sqlString = "INSERT INTO  Sessions (id,MeasurementTime,Nsamples, Data, device_id) VALUES (21,'03:04:52', 4,%s, 21);"
	    cur.execute("INSERT INTO  Sessions (id,MeasurementTime,Nsamples, Data, device_id) VALUES (31,'03:04:52', 4,%s, 21);", (data_x,))
	    print 2
	except:
	    print "cannot SQL Execute"

	conn.commit()
	cur.close()
	conn.close()

    def read_db(self, device_id):
	try: 
	    conn = psycopg2.connect("host='localhost' dbname='postgres' user=postgres password='6105'")
            conn.autocommit = True
        except:
            print "not connect"

        cur=conn.cursor()
        try:
	    print device_id
            # sqlString = "SELECT Device_Name FROM Devices WHERE id=%s"
            #sqlString = "SELECT Device_Name FROM Devices"
            cur.execute("SELECT Device_Name FROM Devices_Profile WHERE id=%s",(device_id,))
            x = cur.fetchone()[0]
	    #print x, type(x), repr(x)
	    print x
        except:
            print "cannot SQL Execute"

        conn.commit()
        cur.close()
        conn.close()

	
def main():
	try:
		server = HTTPServer(('',30004), MyHandler)
		print 'Welcome to the machine'
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()

if __name__== '__main__':
	main()			
