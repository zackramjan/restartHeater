FROM almalinux:9

RUN yum install -y git python python-requests pip && pip install pyHS100
RUN git clone https://github.com/zackramjan/restartHeater.git
WORKDIR /restartHeater
ENTRYPOINT [ "/usr/bin/env", "bash", "entrypoint.sh" ]
