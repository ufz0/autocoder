FROM openjdk:17-slim

# Install Python 3, pip, and other utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl && \
    rm -rf /var/lib/apt/lists/*

# (Optional) Set JAVA_HOME if needed
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip and install pipreqs
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pipreqs

# Regenerate requirements (if needed) and install dependencies
RUN pipreqs . --force
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install flask tika

# Create needed directories
RUN mkdir -p scripts pdfs output

# Copy the rest of the application
COPY . .

EXPOSE 8088

CMD ["python3", "main.py"]
