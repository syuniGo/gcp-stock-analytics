FROM python:3.10

WORKDIR /app

# Install wget and other necessary tools
RUN apt-get update && apt-get install -y wget build-essential

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

# Copy requirements filedoc
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application files
COPY ingest_data.py ingest_data.py
COPY scripts/ scripts/

# Set the entrypoint
CMD ["/bin/bash"]


