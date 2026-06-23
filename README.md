# Chicken Disease Classification Project

End-to-end deep learning project for chicken disease classification with training pipeline, DVC workflow, web app, and optional cloud deployment using AWS or Azure.

---

# Project Workflow

1. Update `config.yaml`
2. Update `secrets.yaml` *(optional)*
3. Update `params.yaml`
4. Update the entity definitions
5. Update the configuration manager in `src/config`
6. Update the components
7. Update the pipeline
8. Update `main.py`
9. Update `dvc.yaml`

---

# How to Run

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/chicken-disease-classification-project-end2end.git
cd chicken-disease-classification-project-end2end
```

---

## 2. Create a conda environment

```bash
conda create -n cnncls python=3.8 -y
conda activate cnncls
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the application

```bash
python app.py
```

Then open the local host URL shown in the terminal.

---

# DVC Commands

```bash
dvc init
dvc repro
dvc dag
```

---

# AWS CI/CD Deployment with GitHub Actions

## 1. Log in to AWS Console

---

## 2. Create an IAM user for deployment

Grant access required for:

* **EC2** → for running the application server
* **ECR** → for storing Docker images

### Deployment flow

1. Build Docker image from source code
2. Push Docker image to Amazon ECR
3. Launch EC2 instance
4. Pull Docker image from ECR on EC2
5. Run the Docker container on EC2

### Recommended IAM policies

* `AmazonEC2ContainerRegistryFullAccess`
* `AmazonEC2FullAccess`

---

## 3. Create an ECR repository

Create a repository to store Docker images.

Example format:

```bash
<aws-account-id>.dkr.ecr.<aws-region>.amazonaws.com/<repository-name>
```

Example:

```bash
123456789012.dkr.ecr.us-east-1.amazonaws.com/chicken
```

Save this URI for later use in GitHub Secrets.

---

## 4. Create an EC2 machine (Ubuntu)

Launch an Ubuntu EC2 instance that will be used for deployment.

---

## 5. Install Docker on EC2

### Optional

```bash
sudo apt-get update -y
sudo apt-get upgrade -y
```

### Required

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

---

## 6. Configure EC2 as a self-hosted GitHub Actions runner

Go to:

* **GitHub Repository**
* **Settings**
* **Actions**
* **Runners**
* **New self-hosted runner**

Choose the EC2 OS and run the commands provided by GitHub one by one on the EC2 machine.

---

## 7. Add GitHub Secrets

In your GitHub repository, go to:

**Settings → Secrets and variables → Actions**

Add the following secrets:

```txt
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
AWS_REGION=<your-aws-region>
AWS_ECR_LOGIN_URI=<your-ecr-login-uri>
ECR_REPOSITORY_NAME=<your-ecr-repository-name>
```

Example:

```txt
AWS_REGION=us-east-1
AWS_ECR_LOGIN_URI=123456789012.dkr.ecr.us-east-1.amazonaws.com
ECR_REPOSITORY_NAME=chicken
```

---

# Azure CI/CD Deployment with GitHub Actions

## Add GitHub Secret

Add the following GitHub secret:

```txt
AZURE_CLIENT_SECRET=<your-azure-client-secret>
```

---

## Build and Push Docker Image to Azure Container Registry

```bash
docker build -t <acr-login-server>/<image-name>:latest .
docker login <acr-login-server>
docker push <acr-login-server>/<image-name>:latest
```

Example:

```bash
docker build -t chickenapp.azurecr.io/chicken:latest .
docker login chickenapp.azurecr.io
docker push chickenapp.azurecr.io/chicken:latest
```

---

## Azure Deployment Flow

1. Build the Docker image from source code
2. Push the Docker image to Azure Container Registry
3. Launch the Azure Web App service
4. Pull the Docker image from the container registry
5. Run the container on the Azure Web App server

---

# Notes

* Never commit real credentials, access keys, client secrets, or registry passwords to the repository.
* Store secrets only in:

  * GitHub Actions Secrets
  * local `.env` files
  * `secrets.yaml` excluded via `.gitignore`
* Use placeholders in documentation instead of real account IDs or secret values.

---

# Suggested `.gitignore` additions

```gitignore
.env
secrets.yaml
*.pem
*.key
```
