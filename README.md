# DockerPythonFlask_ForwardProxy_Mini_Project

Presenter Mo

## Introduction 

A docker container from a specified repository image docker [(httpd:latest]()) is to server as forward proxy for a specified company website. The chosen port on the host is 8080, on the container its 80. This container will also present a status page on port 8081. The status will reflect Processes, CPU, memory and storage utilization on the continer.
<p>

The specification as interpreted , suggest the passing of variables that behave like arrays, (in that they have multiple values, arranged in positional way).

<p>Var UNSET_HTTP_HEADER = [Accept-Encoding, User-Agent, Cookie]</p>
<p>Var SET_HTTP_HEADER =[ (User-Agent: [TechTest]()),( Host: ​ www.companyurl.co.uk)</p>
<p>Var STATUS_REFRESH_PERIOD = (X im seconds for monitoring page)</p>


Status page components:
Var STATUS_REFRESH_PERIOD = (X im seconds for monitoring page).

a. The date the status page was generated.
b. The number of running processes within the container and their CPU utilisation.
c. The memory usage within the container.
d. The disk usage within the container.


# Linux Host adjustment: Prior to testing its important to ensure the teargeted ports are fre to relay the traffic intended.

```
firewall-cmd  --permanent --add-port=8080/tcp
firewall-cmd  --permanent --add-port=8081/tcp

```

## Testing:

Initial test run of part one of the requirement after downloading the image was carried out with the syntax below:

```
   docker run -itd -p 8080:80 --name mo_httpd httpd:latest

```

## 2nd run: More Advanced test was comprising the extra settings that added modifiation to the apache configuration files, these were aimed at enabling the forward proxy functionality in accordance with the understanding of the specificaiton.


```
docker container run  --publish 8080:80  --name morawi_httpd -d -v /apacheVhosts/sites:/usr/local/apache2/conf/sites  httpd:latest

```
## Webserver configuration as ""Forward Proxy"" addition to configuration

To make this config more flexibe and re-usable it was best to configure the proxy settings via 'Virtual hosts' setup. The configuration is to be dropped inside the following path 
within the webserver configuration.

<td>  [/apps/docker/apacheconf/sites](file:///apps/docker/apacheconf/sites)       </td>


```
<VirtualHost *:80>
	
ServerName companyurl.co.uk
ServerAlias www.companyurl.co.uk

ServerAdmin [admin@companyurl.co.uk](mailto:admin@companyurl.co.uk)
DocumentRoot /usr/local/apache2/companyurl.co.uk
	
<Directory "/usr/local/apache2/companyurl.co.uk">
Order allow,deny
AllowOverride All
Allow from all
Require all granted
</Directory>

 # Not part of the specificaiton, preserved for future. 
# Load the SSL module that is needed to terminate SSL on Apache LoadModule ssl_module modules/mod_ssl.so.

#This directive toggles the usage of the SSL/TLS Protocol Engine for proxy. 
# Without this you cannot use HTTPS URL as your Origin Server.
# SSLProxyEngine on.

# To prevent SSL Offloading.
# Set the X-Forwarded-Proto to be https for your Origin Server to understand that this request is made over HTTPS 
# <https://httpd.apache.org/docs/2.2/mod/mod_headers.html#requestheader>.
# RequestHeader set X-Forwarded-Proto “https”
 # RequestHeader set X-Forwarded-Port “443”	

ErrorLog logs/companyurl.co.uk-error.log
CustomLog logs/companyurl.co.uk-access.log combined

# The ProxyPass directive specifies the mapping of incoming requests to the backend server (or a cluster of servers known as a Balancer group).
# It proxies the requests only with matching URI “/status”

ProxyPass /status <https://www.companyurl.co.uk/status>

#To ensure that and Location: headers generated from the backend are modified to point to the reverse proxy, instead of back to itself, #the ProxyPassReverse directive is most often required:

ProxyPassReverse /status <https://www.companyurl.co.uk/status>

</VirtualHost>
	
```

## Note: 'Server name' will be looked up in the address bar: Example


One needs to be aware the ServerName specified in the configuration file is companyurl.co.uk and Apache would look for this name on the Address bar when you try to reach the website.

In enterprise such matters are managed with internal DNS servers. For testing, one can utilize '/etc/hosts' file

Make an entry in your /etc/hosts file like shown below


```
127.0.0.1   www.companyurl.co.uk

```

## 3nd run command test: Passing variables to container run command
After further inverstigation on the way to pass variable to the container run command, it was established that the way below is the most suitable to the scenario interpretation

```
docker container run  --publish 8080:80  --name morawi_httpd -d -v /apacheVhosts/sites:/usr/local/apache2/conf/sites  -v /apacheVhosts/htmlfiles:/usr/local/apache2/companyurl.co.uk  -e UNSET_HTTP_HEADER="Accept-Encoding, User-Agent,Cookie" -e SET_HTTP_HEADER="User-Agent:TechTest, Host:www.companyurl.co.uk"  httpd:latest

```

## To build own image, to be able to add the monitoring requirements of stage 2:

```
image: httpd:latest
  hostname: comapnyurl.co.uk
  ports:
 - "8080:80"
 
```


##Monitoring the container

This can be best serverd via a Python app, in the knowledge that most functions can be servers via python libraries, more portability do different operating systems as most have python libraries that will deliver same result, some might need more adjustment.

The variable that will be passed by system and parsed into the applicaiton by 'os.getenv' is the 'STATUS_REFRESH_PERIOD' It is determined to be the most accurate interpretation of the specificaiton. Pass from the Docker environment through the '-e' key to the OS, this case its the docker based container os using Linux/Ubuntu, then parsed into the flask based monitoring appliaiton via  os.getenv Python library function.  

Early Example Monitoring app: Designed to test flask in the most basic way,(app01.py):
  

```
from flask import Flask

app = Flask(__name__)

@app.route("/status")
def statuspage():
 return "Company_url_tester"
app.run(host='0.0.0.0', port=8081)


```

A more detailed application to test the requirements fully, this was arrived at after the flask experimentation



```
from flask import Flask
from flask import render_template
from time import sleep
import os
import psutil
import socket
import datetime
import html

app = Flask(__name__)
@app.route("/status")

def statuspage():

 os.getenv(STATUS_REFRESH_PERIOD)
 sleep(STATUS_REFRESH_PERIOD)
 now = datetime.datetime.now()
 memouse = psutil.virtual_memory()[2]
 storagepercent = psutil.disk_usage('/')[3]
 cpupercent = psutil.cpu_percent(interval=None, percpu=True)
return render_template('status.html',datetimenow=datetimenow ,memouse=memouse, cpupercent=cpupercent, storagepercent=storagepercent) 

app.run(host='0.0.0.0', port=8081)

```

The flask application for monitoring was made to publish on ip "0.0.0.0" as this was going to serve through a container. An IP will not be fixed, this is like a catch all. 

The testsing url for the monitoring applicaiton is

```
<http://www.companyurl.co.uk:8081/status>

```
## Note
As indicate previously '/etc/hosts' file on the local machine was adjusted to have the entry below:


```
127.0.0.1 www.which.co.uk <http://companyurl.co.uk>
#localhost localhost.localdomain localhost4 localhost4.localdomain4

```

During testing the environment variable was exported to the local environment


```
export STATUS_REFRESH_PERIOD=2

env | grep STATUS_REFRESH_PERIOD
STATUS_REFRESH_PERIOD=2

```

### Displaying the output on the monitoring page

The monitoring page will use format compatible with Jinja2, a templating technology that is widley used within Python's frameworks<p>
The listed lines below are processed by the render module which will replace he variables within to curly bracked with their value.<p>
 


```
<html><head><title>conmpanyurl.co.uk-container-status-page</title></head>
<body>


<h2> Date </h2>
{{ datetimenow }}



<h2> Memory </h2>
{{ memouse }}
</br>

<h2> CPU </h2>
{{ cpupercent }}
</br>


<h2> Storage </h2>
{{ storagepercent }}
</br>


</body>
</html>


```

