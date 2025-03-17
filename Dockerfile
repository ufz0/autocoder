FROM python:3.12

RUN apt-get update && apt-get install -y openjdk-17-jre wget && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV PATH="$JAVA_HOME/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh && \
    chmod +x dotnet-install.sh && \
    ./dotnet-install.sh --channel 6.0 --install-dir /usr/share/dotnet && \
    rm dotnet-install.sh
ENV DOTNET_ROOT=/usr/share/dotnet
ENV PATH="$DOTNET_ROOT:$PATH"


RUN "$DOTNET_ROOT/dotnet" tool install -g dotnet-script --version 1.5.0
ENV PATH="/root/.dotnet/tools:$PATH"

WORKDIR /app

COPY requirements.txt . 

RUN pip install pipreqs 
RUN pipreqs . --force
RUN pip install flask
RUN pip install tika
RUN pip install -r requirements.txt

COPY . . 
RUN mkdir -p scripts pdfs output

EXPOSE 8088

CMD [ "python3", "main.py" ]