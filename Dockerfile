FROM python:3.8
COPY Bot.py ./
COPY helper.py ./
ADD mp3 ./mp3
ADD cogs ./cogs
COPY requirements.txt ./
RUN pip install -r requirements.txt

#libs
RUN apt-get update
RUN apt-get install libopus0 ffmpeg frei0r-plugins   -y

RUN chmod +x ./Bot.py

ENTRYPOINT [ "python", "./Bot.py" ]