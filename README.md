# 📦 AtlasFlow — Cloud-Native Logistics & Order Fulfillment Platform

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions)](https://github.com/Urgsalman/atlasflow/actions)
[![GitOps](https://img.shields.io/badge/CD-ArgoCD-ef7b4d?logo=argo)](https://argo-cd.readthedocs.io/)
[![Infrastructure](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform)](https://www.terraform.io/)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes)](https://kubernetes.io/)

## 🚀 Overview
AtlasFlow is a professional, cloud-native order fulfillment platform built to demonstrate enterprise-grade **DevOps, DevSecOps, and GitOps** practices. The architecture relies on asynchronous microservices to handle high-throughput logistics events with zero downtime and automated self-healing.

## 🏗️ Architecture & Tech Stack

### Application Layer (Microservices)
- **Framework:** FastAPI (Python 3.12), Pydantic
- **Database:** PostgreSQL (SQLAlchemy, Alembic migrations)
- **Event Streaming:** Apache Kafka (Asynchronous messaging & decoupling)

### Infrastructure & DevOps
- **Containerization:** Docker & Kubernetes (Local/Kind & AWS EKS ready)
- **CI/CD:** GitHub Actions (Linting, Docker Build, Trivy Security Scanning, ECR Push)
- **GitOps:** ArgoCD for automated synchronization of Kubernetes manifests
- **Infrastructure as Code (IaC):** Terraform (AWS IAM, OIDC, ECR)

### DevSecOps & Observability
- **Security (Security-by-Design):** Kubernetes Network Policies (Zero Trust), Non-Root Containers, IAM OIDC (No static AWS keys).
- **Monitoring:** Prometheus & Grafana (Resource tracking, Pod metrics)
- **Load Testing:** k6 (Validated for 50+ concurrent VUs with <20ms p95 latency)

## ⚙️ Key Features Implemented
1. **Idempotency:** Prevents duplicate order creation during retries.
2. **Self-Healing:** Kubernetes automatically restarts failed pods.
3. **Automated GitOps Flow:** Any commit to the `main` branch triggers a CI build, vulnerability scan, and ArgoCD deployment.
4. **Zero-Cost Local Dev:** Fully functional local environment replicating cloud behavior.

## 🛠️ Local Setup (Quick Start)

1. **Clone the repository:**


git clone https://github.com/Urgsalman/atlasflow.git
cd atlasflow

2. **Run local dependencies (Kafka, Postgres):**

bash
docker-compose up -d

3. **Deploy to local Kubernetes (using Helm & ArgoCD):**

bash
kubectl apply -f infrastructure/kubernetes/argocd-app.yaml

## 👨‍💻 Author
**Cherif Haouate Soulaimane** - *Cloud & DevSecOps Engineering Student*