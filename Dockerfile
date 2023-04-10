FROM python
COPY chatbot.py .
COPY config.py .

COPY requirements.txt /
RUN pip install pip update 
RUN pip install -r requirements.txt

CMD python chatbot.py
