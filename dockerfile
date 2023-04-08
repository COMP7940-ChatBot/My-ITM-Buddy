FROM python
COPY chatbot.py .
COPY config.py .
RUN pip install pip update 
COPY requirements.txt .
ENV ACCESS_TOKEN 6090162920:AAFOV2pvgxUZILTb014kc4oRAK329fU5hnM
ENV HOST redis-19529.c302.asia-northeast1-1.gce.cloud.redislabs.com
ENV PASSWORD SkXQHWRRZlLEvJITiJ3f1X3N7ZiaULPS
ENV REDISPORT 19529
RUN pip install -r requirements.txt
CMD python chatbot.py
