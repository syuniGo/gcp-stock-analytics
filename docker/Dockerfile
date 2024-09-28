FROM python:3.10-bullseye


WORKDIR /app

# Install wget and other necessary tools
RUN apt-get update && apt-get install -y wget build-essential

RUN apt-get update && \
    apt-get install -y \
        openjdk-11-jdk

# Set up Java environment variables

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH=$PATH:$JAVA_HOME/bin
# Install TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

# Set TA-Lib related environment variables
ENV TA_LIBRARY_PATH=/usr/lib
ENV TA_INCLUDE_PATH=/usr/include
RUN mkdir -p /opt/spark-jars && \
    wget https://jdbc.postgresql.org/download/postgresql-42.2.18.jar -O /opt/spark-jars/postgresql-42.2.18.jar

# Copy requirements filedoc
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application files
COPY ingest_data.py ingest_data.py
COPY scripts/ scripts/

RUN chmod 777 /app

# Expose Jupyter Notebook port
EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}
# Set the entrypoint
CMD ["jupyter", "notebook", "--allow-root"]


