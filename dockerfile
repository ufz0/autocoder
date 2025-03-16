FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      openjdk-8-jre curl && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install pipreqs

RUN pipreqs . --force

RUN pip install -r requirements.txt
RUN pip install flask tika

RUN mkdir scripts pdfs output

COPY . .

EXPOSE 8088

CMD ["python3", "main.py"]
