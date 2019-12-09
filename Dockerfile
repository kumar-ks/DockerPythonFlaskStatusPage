From httpd:latest
RUN apk add python3 py3-pip3 && \
pip3 install --upgrade pip3 && \
pip3 install wget &&\
pip3 install sys &&\
pip3 install threading &&\
pip3 install time &&\
pip3 install requests &&\
pip3 install paho-mqtt &&\
pip3 install logging &&\
rm -rf /var/cache/apk/*
RUN apk add flask 
ENV PYTHONPATH /usr/lib/python3.7/site-packages
RUN make /app
RUN cp status.py /app
RUN cp templates /app
EXPOSE 8080/tcp 
EXPOSE 8081/tcp 
WORKDIR /app
CMD [ "python", "./status.py" ]

