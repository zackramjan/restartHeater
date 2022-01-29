FROM centos:latest

RUN yum install -y git python3 python3-requests && pip3 install pyHS100
RUN git clone https://github.com/zackramjan/restartHeater.git
WORKDIR /restartHeater
ENTRYPOINT [ "/usr/bin/env", "bash", "entrypoint.sh" ]