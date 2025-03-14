# Base image
FROM apache/flink:1.18.0-scala_2.12-java8

ARG PYTHON_VERSION=3.10.0

# SET MongoDB cdc connector args
ARG MONGO_CONNECTOR_VERSION=3.2.1
ARG MONGO_CONNECTOR_NAME=flink-sql-connector-mongodb-cdc-${MONGO_CONNECTOR_VERSION}.jar
ARG MONGO_CONNECTOR_URI=https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-mongodb-cdc/${MONGO_CONNECTOR_VERSION}/${MONGO_CONNECTOR_NAME}

# SET PostgreSQL cdc connector args
ARG POSTGRES_CONNECTOR_VERSION=3.2.1
ARG POSTGRES_CONNECTOR_NAME=flink-sql-connector-postgres-cdc-${POSTGRES_CONNECTOR_VERSION}.jar
ARG POSTGRES_CONNECTOR_URI=https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-postgres-cdc/${POSTGRES_CONNECTOR_VERSION}/${POSTGRES_CONNECTOR_NAME}

# SET JDBC connector args
ARG JDBC_CONNECTOR_VERSION=3.2.0-1.18
ARG JDBC_CONNECTOR_NAME=flink-connector-jdbc-${JDBC_CONNECTOR_VERSION}.jar
ARG JDBC_CONNECTOR_URI=https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/${JDBC_CONNECTOR_VERSION}/${JDBC_CONNECTOR_NAME}

# Connectors download
RUN echo "Downloading ${MONGO_CONNECTOR_URI}" && \
    wget -q -O /opt/flink/lib/${MONGO_CONNECTOR_NAME} ${MONGO_CONNECTOR_URI} && \
    echo "Downloading ${POSTGRES_CONNECTOR_URI}" && \
    wget -q -O /opt/flink/lib/${POSTGRES_CONNECTOR_NAME} ${POSTGRES_CONNECTOR_URI} && \
    echo "Downloading ${JDBC_CONNECTOR_URI}" && \
    wget -q -O /opt/flink/lib/${JDBC_CONNECTOR_NAME} ${JDBC_CONNECTOR_URI}

COPY requirements.txt ./requirements.txt

RUN set -ex; \
    apt-get update && \
    apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libffi-dev lzma liblzma-dev && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --without-tests --enable-shared && \
    make -j4 && \
    make install && \
    ldconfig /usr/local/lib && \
    cd .. && rm -f Python-${PYTHON_VERSION}.tgz && rm -rf Python-${PYTHON_VERSION} && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    ln -s /usr/local/bin/pip3 /usr/local/bin/pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip; \
    pip install -r ./requirements.txt

# Set S3 plugin dir
RUN mkdir -p /opt/flink/plugins/s3-fs-hadoop && \
    cp /opt/flink/opt/flink-s3-fs-hadoop-1.18.0.jar ./plugins/s3-fs-hadoop/

WORKDIR /opt/flink