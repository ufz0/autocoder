FROM python:3.12

# Install full Java (default-jdk) and dependencies
RUN apt-get update && apt-get install -y default-jdk && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"  
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV TIKA_SERVER_JAR="/app/tika-server.jar"

RUN java -version || (echo "Java installation failed!" && exit 1)

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 
RUN wget -q -O tika-server.jar https://repo1.maven.org/maven2/org/apache/tika/tika-server-standard/2.8.0/tika-server-standard-2.8.0.jar

EXPOSE ${PORT:-8088}

CMD ["sh", "-c", "/usr/bin/java -jar tika-server.jar --host 0.0.0.0 --port ${PORT:-8088} & python3 main.py"]
