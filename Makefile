SHELL=/bin/bash

build-environment-and-services:
	@echo "Building Python environment"
	pip install pipenv &&\
	pipenv install
	@echo "Running MLFlow Server on localhost:5000"
	rm -rf mlflow.db mlruns/ &&\
	nohup mlflow server \
		--backend-store-uri sqlite:///mlflow.db \
		--default-artifact-root ./artifacts \
		--host localhost:5000 &
		
	@echo "Deploying Prefect Server on localhost:4200"
	nohup prefect server start &
	@echo "Deploying Monitoring Service"
	docker-compose  -f monitoring/docker-compose.yml up -d
	@echo "Deploying Grafana on localhost:3000"
	@echo "Deploying Adminer on localhost:8080"
	@echo "The local environment is ready to be used."
