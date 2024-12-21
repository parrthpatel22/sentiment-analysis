FROM python:3.8-slim

COPY . ./
WORKDIR ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python","sentimentAnalysis.py" ]