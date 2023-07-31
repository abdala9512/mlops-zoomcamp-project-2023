FROM ubuntu:rolling
COPY ../churnlib /app/churnlib/
COPY ../batch_scoring_pipeline.py /app/batch_scoring_pipeline.py
COPY ../../../Pipfile /app/Pipfile
COPY ../../../Pipfile.lock /app/Pipfile.lock
COPY /data /app/data/
WORKDIR /app
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install pipenv
RUN pipenv install
RUN echo "Churn inference process finished sucessfully"
CMD pipenv run  /app/3_Deployment_Code/src/batch_scoring_pipeline.py