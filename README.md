# TechTrends - Cloud Native Application

## Project Overview
TechTrends is a dynamic web application that provides technical articles in the cloud-native ecosystem. This project serves as a comprehensive showcase of modern software engineering practices, covering the entire lifecycle from local development to automated cloud-native deployment.

This project is part of the **[Udacity Cloud Native Application Architecture](https://www.udacity.com/course/cloud-native-application-architecture--nd064)** Nanodegree program. It is based on the initial codebase provided in the **[nd064_course_1](https://github.com/udacity/nd064_course_1)** repository.

## Technical Knowledge & Skills Demonstrated
The implementation of TechTrends demonstrates proficiency in the following areas:

### 🚀 Backend Development
- **Framework:** Python Flask
- **Database:** SQLite
- **Logging:** Structured logging for application events and errors.
- **Monitoring:** Implementation of `/healthz` and `/metrics` endpoints for observability.

### 🐳 Containerization
- **Docker:** Multi-stage-like builds (using slim images) and optimized Dockerfiles.
- **Image Versioning:** Automated tagging based on Git commit SHAs via GitHub Actions.

### ☸️ Orchestration & Infrastructure
- **Kubernetes:** Declarative manifests for Deployments, Services, and Namespaces.
- **Helm:** Templated Kubernetes manifests for environment-specific configurations (Staging/Production).
- **K3s:** Lightweight Kubernetes distribution used for development and testing.
- **Vagrant:** Infrastructure-as-Code for reproducible local lab environments.

### 🔄 CI/CD & GitOps
- **GitHub Actions:** Automated testing (Pytest) and building/pushing of Docker images to DockerHub.
- **ArgoCD:** Implementation of GitOps principles for continuous delivery, ensuring the cluster state matches the git repository.

## Project Structure
- `techtrends/`: The core Flask application source code.
- `kubernetes/`: Plain Kubernetes manifests for manual deployment.
- `helm/`: Helm charts for scalable and configurable deployments.
- `argocd/`: Configuration files for ArgoCD applications.
- `.github/workflows/`: CI/CD pipeline definitions.
- `Vagrantfile`: Configuration for the local virtualized lab.
