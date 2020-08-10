FROM python:3
COPY Bot.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN chmod +x ./Bot.py

ENTRYPOINT [ "python", "./Bot.py" ]