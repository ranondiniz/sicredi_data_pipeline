# Base Python com Java (para Spark)
FROM openjdk:11-jdk-slim

# Variáveis de ambiente
ENV SPARK_VERSION=3.4.1 \
    HADOOP_VERSION=3 \
    DELTA_CORE_VERSION=2.4.0 \
    PYTHON_VERSION=3.10

# Instalação de dependências
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev curl wget git build-essential nano && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install --upgrade pip

# Instalação de Spark
ENV SPARK_VERSION=3.4.4
ENV HADOOP_VERSION=3

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Instalação de Python libs
RUN pip install \
    pyspark==3.4.1 \
    delta-spark==2.4.0 \
    pandas \
    notebook \
    jupyterlab

# Criação da pasta de trabalho
WORKDIR /app

# Expõe porta do Jupyter
EXPOSE 8888

# Comando para iniciar o JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password=", "--no-browser"]

# Para evitar warning
RUN apt-get update && apt-get install -y procps
