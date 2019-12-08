from flask import Flask
from flask import render_template
from time import sleep
import os
import psutil
import socket
import datetime
import html
import sys

app = Flask(__name__)
@app.route("/status")

def statuspage():
  try:  
    statusrefreshperiod = int(os.environ.get('STATUS_REFRESH_PERIOD'))
  except KeyError:
    print("Please ensure the Variable STATUS_REFRESH_PERIOD is set correctly")
    sys.exit(1)
  sleep(statusrefreshperiod)
  datetimenow = datetime.datetime.now()
  memouse = psutil.virtual_memory()[2]
  storagepercent = psutil.disk_usage('/')[3]
  cpupercent = psutil.cpu_percent(interval=None, percpu=True)
  return render_template('status.html',datetimenow=datetimenow ,memouse=memouse, cpupercent=cpupercent, storagepercent=storagepercent) 

app.run(host='0.0.0.0', port=8081)

