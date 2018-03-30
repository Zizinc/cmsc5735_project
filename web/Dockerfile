FROM ubuntu:14.04
RUN apt-get update -y && apt-get -y install curl

# PYTHON
RUN apt-get install -y python-pip python-dev build-essential

# JAVA
#RUN apt-get install python-software-properties
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:webupd8team/java
RUN apt-get update
RUN apt-get install oracle-java8-installer -y -y

# SPARK
ARG SPARK_ARCHIVE=https://archive.apache.org/dist/spark/spark-2.1.0/spark-2.1.0-bin-hadoop2.7.tgz
RUN curl -s $SPARK_ARCHIVE | tar -xz -C /usr/local/

ENV SPARK_HOME /usr/local/spark-2.1.0-bin-hadoop2.7
ENV PATH $PATH:$SPARK_HOME/bin

# SETUP APPLICATION
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Run without Spark
#ENTRYPOINT ["python"]
#CMD ["app.py"]

# Run with Spark in local
ENTRYPOINT ["spark-submit"]
CMD ["server.py"]
