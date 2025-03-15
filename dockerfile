FROM python:3.12

WORKDIR /app

COPY requirements.txt . 

RUN pip install pipreqs 

RUN pipreqs . --force

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8088

CMD [ "python3", "main.py" ]
