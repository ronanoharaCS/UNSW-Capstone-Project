FROM python:latest 

RUN apt-get update
RUN apt-get -y install software-properties-common

# install java 8 - add repo 
RUN add-apt-repository ppa:openjdk-r/ppa
RUN apt-get -y install openjdk-8-jdk 

# install text summary tool
RUN pip3 install giveme5w1h
RUN giveme5w1h-corenlp install'

EXPOSE 9000

# start coreNLP server
ENTRYPOINT ["giveme5w1h-corenlp"]
