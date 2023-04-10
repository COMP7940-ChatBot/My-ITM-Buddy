FROM python
COPY chatbot.py .
COPY config.py .

COPY requirements.txt /
RUN pip install pip update 
RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 8080
EXPOSE 80
EXPOSE 443
EXPOSE 8050
EXPOSE 8081
EXPOSE 3000

CMD python chatbot.py
