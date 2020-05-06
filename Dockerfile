FROM ubuntu:20.04

RUN apt-get update && apt-get install --no-install-recommends --yes python3 python3-pip

WORKDIR /usr/lib/serotonin

ADD requirements.txt ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt
    #python3 -m pip install --no-cache-dir matplotlib==3.2.1 numpy==1.18.3 scipy==1.4.1

ADD . .

CMD [ "python3", "./app.py", "--mode=PLOT" ]
