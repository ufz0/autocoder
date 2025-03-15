FROM python:3.12

# Install Java and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENV PATH="$JAVA_HOME/bin:$PATH"

RUN java -version || (echo "Java installation failed!" && exit 1)

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import tika; tika.initVM()"

COPY . . 
RUN wget -q -O tika-server.jar https://repo1.maven.org/maven2/org/apache/tika/tika-server-standard/2.8.0/tika-server-standard-2.8.0.jar

EXPOSE ${PORT:-8088}

CMD ["sh", "-c", "/usr/bin/java -jar tika-server.jar --host 0.0.0.0 --port ${PORT:-8088} & python3 main.py"]
