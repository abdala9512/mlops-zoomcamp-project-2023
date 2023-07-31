FROM ubuntu:rolling
COPY /deployment/. /app/deployment/
COPY /model /app/model/
COPY /data /app/data/
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -r /app/3_Deployment_Code/src/requirements.txt
RUN echo "Batch prediction succeed"
CMD python3 /app/3_Deployment_Code/src/orchestration_docker.py