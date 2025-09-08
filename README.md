# MyApp

A sample Python application packaged in Docker, with full CI/CD pipelines on **GitHub Actions**.  
The project includes unit tests, linting/formatting, security scans, container builds, and Kubernetes deployment with a MySQL database and Flyway migrations.

# Purpose of project
The idea of the project is to set up a CI/CD pipeline for a simple App.
---

📂 Project Structure
```bash
├── Dockerfile
├── flyway.conf
├── requirements.txt
├── sonar-project.properties
│
├── k8/                  
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── mysql-configmap.yaml
│   ├── mysql-deployment.yaml
│   ├── mysql-secret.yaml
│   ├── mysql-service.yaml
│   └── service.yaml
│
├── sql/                         
│   ├── V1__Create_person_table.sql
│   ├── V2__Add_people.sql
│   └── V3__Add_more_people.sql
│
└── src/
    ├── app.py
    └── app_test.py
```
## ⚙️ CI Pipeline (`.github/workflows/ci.yaml`)

Triggered on pushes and pull requests to `main`, `dev`, or `feature/**` branches.

**Stages:**
1. **Build & Test**
   - Lint with `pylint`
   - Format check with `black`
   - Run unit tests (`pytest`)
   - Build Docker image (`myapp:<commit-sha>`)

2. **Security Tests**
   - [Snyk](https://snyk.io/) (DAST)
   - [Trivy](https://aquasecurity.github.io/trivy/) (FS scan)
   - [Gitleaks](https://github.com/gitleaks/gitleaks) (secrets detection)
   - [SonarCloud](https://sonarcloud.io/) (SAST)

3. **Push to Docker Hub**
   - Builds production image
   - Scans Docker image with Trivy (we have set up level to be only CRITICAL)
   - Pushes to Docker Hub (`<DOCKER_USERNAME>/myapp:<commit-sha>`)

---

## 🚀 CD Pipeline (`.github/workflows/cd.yaml`)

Triggered automatically after a successful **CI Pipeline** run on the ONLY `main` branch. 

NOTE: I wanted to make sure that if we push into main the CD will start after the CI finishes. The reason is that the docker image we use in the CD, should be taken from the Docker repository (with the tag). If we dont specify this, there is a chance of error in the CD.yaml, because it couldnt pull the wanted image ~ "race condition"

**Steps:**
1. Provision a local **Kind** Kubernetes cluster.
2. Deploy **MySQL** with Secrets & ConfigMaps.
3. Wait for MySQL readiness & test connectivity.
4. Pull application image from Docker Hub & load into Kind.
5. Apply Kubernetes manifests from `k8/` (excluding MySQL).
6. Run **Flyway** migrations inside the cluster using SQL files in `/sql`.
7. Verify final deployment and print logs.

---


## Things which are done only for the testing

What we do with starting the database from the CD
1. Start the database (MySQL pod + service in the Kind cluster).

2. Load configuration & secrets (ConfigMap + Secret).

3. Wait until the DB is ready.

4. Run Flyway migrations inside Kubernetes (so schema is up-to-date).

5. Deploy your app (which then connects to the migrated DB).

Pros for this type of solution:

1) Test migrations are on the same commit that passed CI.
2) The database is fresh every run, so Flyway always starts from a clean state → catches migration errors early.
3) App + DB work together

Cons:

1) !!! Each time i deploy i start a new DB, which will be bad for productions.

## 🐳 Docker

Build the image locally:

```bash
docker build -t myapp:local .

🛡️ Security

The CI pipeline enforces:

1.Code quality (lint, format)

2.Unit testing

3.Secret scanning (Gitleaks)

4.Dependency scanning (Snyk, Trivy)

5.Static analysis (SonarCloud)

🗄️ Database

Runs MySQL 8.0.33

Credentials and DB name are injected via Secrets and ConfigMaps

Flyway handles migrations (sql/ directory)

🔑 Required GitHub Secrets
Secret	Description
DOCKER_USERNAME	Docker Hub username
DOCKER_PASSWORD	Docker Hub password or token
MYSQL_ROOT_PASSWORD	Root password for MySQL
MYSQL_DATABASE_PASSWORD	Application DB user password
SNYK_TOKEN	Snyk API token
SONAR_TOKEN	SonarCloud token

📊 SonarCloud

This repo integrates with SonarCloud for:

Code coverage

Vulnerability scanning

Maintainability checks

📦 CI/CD Flow Summary

Developer pushes code → CI Pipeline runs.

If all checks pass → Docker image is pushed to Docker Hub.

CD Pipeline triggers → Deploys app + MySQL + migrations to Kind.

Final deployment is verified & logs displayed.

✨ Future Improvements

In the CI:
1. We could reposition the composotion of the CI pipeline and create seperate jobs for each kind of security testing.

2. Using other type of package (not only Docker) ~ we can try to set up the CI using Nix

In the CD:

1.Use Helm charts instead of raw manifests.

2.Deploy to managed Kubernetes (EKS/GKE/AKS) instead of Kind.

3.Add monitoring (Prometheus + Grafana).

4.Automate rollback on failed deployment.

5.Use of Terraform.