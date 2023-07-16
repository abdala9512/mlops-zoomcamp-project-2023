
import streamlit as st
import uuid
import json

BATCH_INFERENCE_SCHEDULE = None

def validate_params():
    assert PROJECT_NAME != "", "Fill the project with a valid name"
    assert TARGET_VARIABLE != "", "Fill the target variable with its correspondent name"
    assert EXPERIMENT_NAME != "", "Fill the experiment with a valid name"
    observability_options = [MODEL_PERFORMANCE, DATA_QUALITY, DATA_DRIFT]
    assert any(observability_options), "Select at least ONE observability tool"



st.set_page_config(page_title="Register ML project", page_icon="📦")
st.write("# Create New ML project 🚀")
st.write("**NOTE**: The ML platform only support supervised models.")

# generalities
PROJECT_NAME = st.text_input("**Project Name**",)
PROJECT_DESCRIPTION = st.text_area("**Project Description**")

# Orchestration

st.write("## Training and Orchestration")

TARGET_VARIABLE = st.text_input("**Target Variable name**")
EC2_INSTANCE = st.selectbox("**AWS EC2 instance type for model training**", options=["t2.micro","t2.medium","t3.medium"])
EXPERIMENT_NAME = st.text_input("**MLflow experiment name**")
st.text_input("**Training Schedule (Create a CRON)**")

st.write("## Serving")

DEPLOYMENT_OPTION = st.selectbox("**Select Deployment option**", options=["Rest API (online)", "Batch (Offline)"])
if DEPLOYMENT_OPTION == "Batch (Offline)":
    BATCH_INFERENCE_SCHEDULE = st.text_input("**Batch inference Schedule (CRON)**")


st.write("## Observability")
st.write(" #### Choose monitors you can to visualize on dashboard:")

MODEL_PERFORMANCE = st.checkbox(label="Model Performance")
DATA_DRIFT = st.checkbox(label="Data Drift")
DATA_QUALITY = st.checkbox(label="Data Quality",value=True)

# Validation

st.write("#### ML project JSON config (Make sure you enter correct configuration before deployment): ")

SERVING_TYPES = {
    "Rest API (online)": {
        "label": "rest_api",
        "options": {
            
        }
    },
    "Batch (Offline)":{
        "label":  "batch",
        "options": {
            "inference_schedule": BATCH_INFERENCE_SCHEDULE
        }
    }
}

DEPLOYMENT_CONFIG = {
    "project_name": PROJECT_NAME,
    "project_description": PROJECT_DESCRIPTION,
    "modeling": {
        "target_variable": TARGET_VARIABLE,
        "mlflow_experiment_name": EXPERIMENT_NAME,
        "aws_compute_instance": EC2_INSTANCE
    },
    "serving": {
        "type": SERVING_TYPES[DEPLOYMENT_OPTION]["label"],
        "options":  SERVING_TYPES[DEPLOYMENT_OPTION]["options"]
    },
    "observability": {
        "data_drift": DATA_DRIFT,
        "model_performance": MODEL_PERFORMANCE,
        "data_quality": DATA_QUALITY
    },
    "status": "active"
}

st.json(DEPLOYMENT_CONFIG)

st.write("## Deployment")
st.write("This project will be deployed with Terraform")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Terraform_Logo.svg/1280px-Terraform_Logo.svg.png", width=300)
st.write("### Credentials")
st.write("You need to pass the right credentials and configurations to deploy the project")
SECRET_PASS = st.text_input("**Secret pass**")

if st.button("Deploy!"):
    validate_params()
    project_id = uuid.uuid1()
    st.write("Deploying...")
    st.write(f"**Auto generated project ID**: {project_id}")

    st.write("**Your model has bee deployed! You can download the JSON config with the relevant project information:**")
    st.download_button(
            label='Download deployment config', 
            mime="application/json",
            file_name=f"{PROJECT_NAME}_deployment.json",
            data=json.dumps(DEPLOYMENT_CONFIG, indent=4)
            )

