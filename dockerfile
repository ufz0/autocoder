FROM python:3.12

# Install Java 17 and curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      openjdk-17-jre-headless curl && \
    rm -rf /var/lib/apt/lists/*

# Use the default JVM path on x86
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
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
