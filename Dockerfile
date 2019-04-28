FROM python:3

WORKDIR /project
 
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python3", "./start_crawler.py" ]