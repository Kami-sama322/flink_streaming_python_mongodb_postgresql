## **Stream Processing Pipeline: MongoDB to PostgreSQL with Apache Flink on Python**

This project demonstrates how to set up a data streaming pipeline from MongoDB to PostgreSQL using Apache Flink on Kubernetes with Python script's. The pipeline processes data in real-time, leveraging MinIO for checkpoint storage and Kubernetes for orchestration.

---

### **Prerequisites**

Ensure the following tools are installed:

- **Docker**
- **Minikube**
- **Helm**
- **kubectl**

---

### **Setup Steps**

#### **1. Start Minikube**

Allocate resources for Minikube:

```bash
minikube start --cpus=5 --memory=8096
```

Launch the Kubernetes dashboard:

```bash
minikube dashboard
```

---

#### **2. Install Certificates**

Install the Cert-Manager for Kubernetes:

```bash
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.11.0/cert-manager.yaml
```

Wait until all pods are running.

---

#### **3. Deploy MongoDB**

1. Create a namespace for MongoDB:

```bash
kubectl create namespace mongodb
```

2. Create a ConfigMap for database initialization:

```bash
kubectl -n mongodb create configmap init-mongo --from-file ./bitnami-mongo-replica-set/init-mongo.js
```

3. Deploy MongoDB using Helm:

```bash
helm install mongodb oci://registry-1.docker.io/bitnamicharts/mongodb -f ./bitnami-mongo-replica-set/values.yaml --namespace mongodb --create-namespace
```

4. Verify MongoDB setup:
    - Access the pod:

```bash
kubectl exec -it <mongodb-pod-name> --namespace=mongodb -- mongosh
```

    - Check the database:

```javascript
use database;
db.users.find();
```


---

#### **4. Deploy PostgreSQL**

Deploy PostgreSQL using a pre-configured manifest:

```bash
kubectl apply -f ./postgresql-deployment.yaml
```

Forward PostgreSQL service port for external access:

```bash
kubectl port-forward service/postgresql-nodeport 30432:5432 --namespace=postgresql
```

Verify the database setup using a tool like DBeaver.

---

#### **5. Deploy MinIO**

Deploy MinIO for checkpoint storage:

```bash
kubectl apply -f ./minio.yaml
```

Forward MinIO service port to access the UI:

```bash
kubectl port-forward services/minio-service 9090:9090 --namespace=minio
```

---

#### **6. Set Up Fake Data Generator**

Build and deploy a custom Docker image to generate fake data in MongoDB:

```bash
eval $(minikube docker-env)
docker build -t myimages/python_mongo_generator:latest ./path/to/folder/with/fake_source_pipe
```

Wait until Docker image is built.

```bash
kubectl apply -f ./fake_source_pipe/python-pod.yaml
```
---

### **Apache Flink Deployment**

#### **Option 1: Flink Kubernetes Operator**

1. Build the custom Flink Docker image:

```bash
eval $(minikube docker-env)
docker build -t myimages/pyflink-base:latest ./path/to/folder/with/flink_job
```

2. Install the Flink Kubernetes Operator via Helm:

```bash
helm repo add flink-operator-1-10-0-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.10.0/
helm install flink-kubernetes-operator flink-operator-1-10-0-repo/flink-kubernetes-operator --namespace flink-operator --create-namespace
```

3. Submit the Flink job:

```bash
kubectl apply -f ./flink-operator/flink_job/flink-users-job.yaml
```

4. Forward the Job Manager UI port to view job details:

```bash
kubectl port-forward -n flink-operator <job-manager-pod-name> 8081:8081
```


---

#### **Option 2: Native Flink on Kubernetes (HA Mode)**
for NON HA Mode use ./flink_cluster_no_high_availability dir

1. Build the custom Flink Docker image:

```bash
eval $(minikube docker-env)
docker build -t myimages/pyflink-base:latest ./path/to/folder/with/flink_jobs
```

2. Deploy the Flink cluster in HA mode:

```bash
kubectl apply -f ./flink_cluster_high_availability/
```

3. Forward the Job Manager UI port to view job details:

```bash
kubectl port-forward services/flink-jobmanager-rest 8081:8081 --namespace=flink
```

4. Submit a Python job manually:
Copy the job script to the Job Manager pod:

```bash
kubectl -n flink cp ./flink_cluster_high_availability/flink-jobs/users-job.py <job-manager-pod-name>:/tmp/users-job.py;
```

Run the job:

```bash
kubectl -n flink exec -it <job-manager-pod-name> -- /opt/flink/bin/flink run --python /tmp/users-job.py;
```


---

### **Stopping and Cleaning Up**

#### **Flink Kubernetes Operator**

To delete a job deployment:

```bash
kubectl delete -n flink-operator flinkdeployments/<job-name>
```

To stop/start a job, update its state in `flink-users-job.yaml` (state: `suspended` or `running`) and reapply.

#### **Native Flink**

To cancel a job via UI, click "Cancel Job" or use CLI commands.
```bash
kubectl -n flink exec -it <job-manager-pod-name> -- /opt/flink/bin/flink stop --savepointPath s3a://apache-flink/savepoints/<job-name>/ <job-id>
```

To uninstall Flink resources:

```bash
helm uninstall flink-kubernetes-operator -n flink-operator;
kubectl delete namespace flink-operator;
```
```bash
kubectl delete namespace flink;
```

Minikube stopping / deleting
```bash
minikube stop;
```
or
```bash
minikube delete;
```
---

### **Conclusion**

This pipeline showcases real-time streaming from MongoDB to PostgreSQL using PyFlink with two deployment modes: Operator-based and Native Kubernetes-based setups. Adjust configurations as needed for production environments!
