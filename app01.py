from flask import Flask

app = Flask(__name__)

@app.route("/status")
def statuspage():
 return "Company_url_tester"
app.run(host='0.0.0.0', port=8081)
