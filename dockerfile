FROM python:3.12

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8085

CMD [ "python3", "main.py" ]