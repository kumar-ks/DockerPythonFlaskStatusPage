from flask import Flask
from time import sleep
import os
import psutil
import socket
import datetime
import html

app = Flask(__name__)
@app.route("/status")

def statuspage():
  statusrefreshperiod = os.getenv("STATUS_REFRESH_PERIOD")
  sleep(statusrefreshperiod)
  datetimenow = datetime.datetime.now()
  memouse = psutil.virtual_memory()[2]
  storagepercent = psutil.disk_usage('/')[3]
  cpupercent = psutil.cpu_percent(interval=None, percpu=True)
  statusmessage = [datetimenow,memouse,storagepercent,cpupercent]
  return statusmessage


  # return html.format(print("The Date is",datetimenow), print("CPU Usage is",cpupercent), print("Memory Used",memouse), print("Storage Used",storagepercent))


#if __name__ == "__main__":
app.run(host='0.0.0.0', port=8081)

