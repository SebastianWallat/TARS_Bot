FROM python:3
COPY Bot.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD [ "python", "./Bot.py" ]