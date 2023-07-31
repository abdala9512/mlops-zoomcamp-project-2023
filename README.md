# MLOps zoomcamp Project - Cohort 2023

![](https://www.cleartouch.in/wp-content/uploads/2022/11/Customer-Churn.png)
# 1. Problem description

The **ABC Multistate bank**  has churn problem, also known as a customer churn problem, is a machine learning problem focused on predicting whether a customer is likely to leave (churn) or stay with a bank based on historical data. Churn refers to the process by which customers discontinue their relationship with a company or service, and in the context of a bank, it means customers closing their accounts and moving to another bank.

* Problem type: Supervised/Classification


## Dataset

 The dataset was found as a [Kaggle dataset](https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset). Sample data:
| customer_id | credit_score | country | gender | age | tenure | balance | products_number | credit_card | active_member | estimated_salary | churn |
|-------------|--------------|---------|--------|-----|--------|---------|-----------------|-------------|---------------|------------------|-------|
| 15634602    | 619          | France  | Female | 42  | 2      | 0       | 1               | 1           | 1             | 101348.88        | 1     |
| 15647311    | 608          | Spain   | Female | 41  | 1      | 83807.86| 1               | 0           | 1             | 112542.58        | 0     |
| 15619304    | 502          | France  | Female | 42  | 8      | 159660.8| 3               | 1           | 0             | 113931.57        | 1     |
| 15701354    | 699          | France  | Female | 39  | 1      | 0       | 2               | 0           | 0             | 93826.63         | 0     |
| 15737888    | 850          | Spain   | Female | 43  | 2      | 125510.82| 1               | 1           | 1             | 79084.1          | 0     |


## Proposed Solution

As a machine learning problem, the goal is to build a predictive model that can accurately identify customers who are at risk of churning. This model can help banks take proactive measures to retain valuable customers by offering targeted incentives, personalized services, or early intervention strategies.

* Solution type: **batch deployment** for the model tranining and inference.

# 2. Cloud

The tech stack used:

The project uses:

1. [Pipenv](https://docs.pipenv.org/)
2. [docker](https://docker.com)
3. [mlflow](https://mlflow.org)
4. [grafana](https://grafana.com)
5. [prefect](https://prefect.io)

And th VM used for the project (AWS EC2 instance):

![](/assets/aws_instance.png)

We use Makefile to reproduce the needed environment in any infrastructure.

```bash
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
```

Execute entire environment:

```bash
make
```

## Next steps - ML platform (WIP)

![](/assets/mlplatform_home.png)

A machine learning (ML) platform interface for deploying machine learning models using the stack of AWS, Flask, MLflow, and Prefect would provide a seamless and scalable solution for model deployment and management. Let's break down the components of the platform:

AWS (Amazon Web Services):
AWS is a cloud computing service that offers a wide range of tools and services to build, deploy, and manage applications. In the context of the ML platform, AWS will provide the infrastructure and services for hosting the platform components, managing data, and deploying machine learning models.

**Flask**:
Flask is a lightweight and flexible web framework for Python. It will be used to create the backend of the ML platform, handling HTTP requests and responses. Flask allows easy integration with other Python libraries and will serve as the API layer to interact with the ML models.

**MLflow**:
MLflow is an open-source platform for managing the end-to-end machine learning lifecycle. It allows data scientists to track and version their experiments, package and deploy models, and manage model deployments. MLflow also provides tools for model registry and collaboration between team members.

**Prefect**:
    Prefect is a workflow management system that helps in orchestrating complex data workflows, including ML model training, evaluation, and deployment. It provides a way to define, schedule, and monitor workflows, making it easier to automate and manage the deployment pipeline for machine learning models.

UI for deployment:

![](/assets/mlplatform_deployment.png)

# 3. Experiment Tracking and model registry

For experiment tracking and model registry we use `mlflow`

![](assets/mlflow_exp_sc.png)

2. Register model

![](/assets/mlflow_model_registry.png)

3. Promote best model to Production

![](/assets/mlflow_model_promotion.png)
# 4. Workflow orchestration

We use prefect for orchestration in:
![](/assets/prefect_flows.png)

1. Model training `src/training_pipeline.py`
![](/assets/model_training_prefect.png)
2. Model inference (Predict new data) `src/batch_scoring_pipeline.py`
![](/assets/score_churn_prefect.png))
3. Model monitoring (Calculate drift, and model performance) `src/monitor_ml_churn_model.py`
![](/assets/monitoring_prefect.png)


# 5. Model Deployment

Deployment is done via `Makefile` + `Dockerfile`

## Steps

0. clone the repository `git clone https://github.com/abdala9512/mlops-zoomcamp-project-2023.git`
1. Execute `Makefile` to create services `make`
2. Execute model training pipeline `python src/training_pipeline.py`
3. Promote any model to PROD in Mlflow
4. Execute scoring pipeline `python src/batch_scoring_pipeline.py`
5. Execute Monitoring pipeline  `python src/monitor_ml_churn_model.py`

# 6. Model monitoring

Machine learning monitoring with Grafana and Postgres involves using these two tools to track, visualize, and analyze the performance and behavior of machine learning models deployed in production. Let's break down how each component contributes to the monitoring process:

**Machine Learning Models in Production:**
When machine learning models are deployed in a production environment, they interact with real-world data, and their performance and behavior may change over time. Monitoring these models is essential to ensure they continue to make accurate predictions and maintain their desired performance.

**Grafana:**
Grafana is an open-source data visualization and monitoring tool. It allows you to create interactive and customizable dashboards to visualize and analyze data from various sources, including databases, APIs, and monitoring systems. Grafana is highly extensible and supports numerous data sources, making it suitable for integrating with different monitoring and logging tools.

**Postgres (PostgreSQL):**
Postgres is an open-source, powerful relational database management system (RDBMS). It is often used to store data from applications, including machine learning models. Postgres is known for its performance, scalability, and support for complex queries.

Adminer data explorer (PostgreSQL database)
![](/assets/adminer_sc.png  )

Grafana
![](/assets/grafana_dash.png)

# Reproducibility

1. Run `Makefile` (Local or cloud)
2. Execute docker files


```
echo "Build dockerfile"
docker build -t customer_churn_ml_pipeline ./src/deployment
docker run -v $(pwd):/app/ -it customer_churn_ml_pipeline
```
