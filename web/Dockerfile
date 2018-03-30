FROM ubuntu:14.04
RUN apt-get update -y && apt-get -y install curl

# PYTHON
RUN apt-get install -y python-pip python-dev build-essential

# JAVA
RUN apt-get -y install default-jre
RUN apt-get install -y software-properties-common python-software-properties

RUN apt-get -y -q update && \
    apt-get -y -q upgrade && \
    apt-get -y -q install software-properties-common htop && \
    add-apt-repository ppa:webupd8team/java && \
    apt-get -y -q update && \
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
    apt-get -y -q install oracle-java8-installer && \
    update-java-alternatives -s java-8-oracle

# SPARK
ARG SPARK_ARCHIVE=https://archive.apache.org/dist/spark/spark-2.1.0/spark-2.1.0-bin-hadoop2.7.tgz
RUN curl -s $SPARK_ARCHIVE | tar -xz -C /usr/local/

ENV SPARK_HOME /usr/local/spark-2.1.0-bin-hadoop2.7
ENV PATH $PATH:$SPARK_HOME/bin

# SETUP APPLICATION
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# SETUP DATA (can be remove in production)
COPY ./data /data

# Run without Spark
#ENTRYPOINT ["python"]
#CMD ["app.py"]

# Run with Spark in local
ENTRYPOINT ["spark-submit"]
CMD ["server.py"]
