FROM python:3.12

# Install Java and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre && rm -rf /var/lib/apt/lists/*

# Explicitly set Java path
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
ENV PATH="$JAVA_HOME/bin:$PATH"

# Verify Java installation
RUN java -version || (echo "Java installation failed!" && exit 1)

WORKDIR /app

# Copy dependencies
COPY requirements.txt . 

# Force reinstall to prevent issues
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Tika is downloaded and ready
RUN python -c "import tika; tika.initVM()"

COPY . . 

EXPOSE 8088

CMD ["python3", "main.py"]
