FROM python:3
ADD Bot.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./Bot.py" ]