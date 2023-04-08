FROM python
COPY chatbot.py .
COPY requirements.txt /
RUN pip install pip update 
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN 6090162920:AAFOV2pvgxUZILTb014kc4oRAK329fU5hnM
ENV HOST redis-19529.c302.asia-northeast1-1.gce.cloud.redislabs.com
ENV PASSWORD SkXQHWRRZlLEvJITiJ3f1X3N7ZiaULPS
ENV REDISPORT 19529
CMD python chatbot.py
