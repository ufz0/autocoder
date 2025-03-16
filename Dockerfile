FROM python:3.12

RUN apt-get update && apt-get install -y openjdk-17-jre && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

COPY requirements.txt . 

RUN pip install pipreqs 

RUN pipreqs . --force

RUN pip install flask

RUN pip install tika

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8088

CMD [ "python3", "main.py" ]