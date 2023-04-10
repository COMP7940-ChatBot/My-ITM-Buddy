FROM python
COPY chatbot.py .
COPY config.py .

COPY requirements.txt /
RUN pip install pip update 
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python chatbot.py
