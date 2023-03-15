1 - [] Subir IAC conforme aula 3_5

2 - [] aws eks update-kubeconfig --region us-east-1 --name btc-edc-m3-kramer-eks

3 - [] helm repo add apache-airflow https://airflow.apache.org

4 - [] kubectl create ns airflow

5 - [] kubectl create secret -n airflow generic aws-secret \
--from-literal=AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
--from-literal=AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
--from-literal=AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

6 - [] kubectl apply -f manifests/airflow-crb.yaml -n airflow

7 - [] Criar a fernet key e webserver secret key do arquivo do airflow
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
python -c 'import secrets; print(secrets.token_hex(16))'

8 - [] Criar bucket de logs do airflow, precisa colocar o caminho no manifesto do airflow 
linha 1688
remote_base_log_folder: s3://nome-do-seu-bucket/edc-btc-m3
remote_log_conn_id: my_s3_conn

9 - [] Colocar o caminho das dags no manifest do airflow 1787
repo: https://github.com/kramerProject/airflow-dags.git
    branch: main
    rev: HEAD
    depth: 1
    subpath: "dags"

10 - [] Fazer / Conferir arquivos dags

11 - [] Subir dags no github


12 - helm repo add apache-airflow https://airflow.apache.org

13 - helm repo update

14 - [] helm install airflow apache-airflow/airflow --version 1.7.0 -n airflow -f manifests/airflow-values.yaml

15 - [] helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

16 - [] helm repo update

17 - [] helm install spark-operator spark-operator/spark-operator --namespace processing \
--create-namespace -f manifests/spark-operator-values.yaml --version 1.1.26

18 - [] kubectl create secret -n processing generic aws-secret \
--from-literal=AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
--from-literal=AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
--from-literal=AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>
 
19 - [] kubectl port-forward service/airflow-webserver -n airflow 8080:8080

20 - [] Cadastrar a connection em admin connections. "my_s3_conn" na UI do Airflow:
connection type Amazon Web Services

21 - [] Criar cluster connection id no airflow kubernetes_default
connection type Kubernetes Cluster Connection. Em admin > connections
marcar a caixinha in cluster configuration

22 - [] Criar variavel de ambiente combustiveis_source_urls no airflow em admin > variables

[
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2015-01.csv",
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2015-02.csv",
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2016-01.csv"
]


23 - [] Criação dos buckets para a camada landing e a camada bronze. Colocar os nomes dos buckets criados no arquivo aws da pasta docker>scripts>app>config>aws.py

24 - [] Conferir arquivos de ingestão e processamento do job

25 - [] Buildar e subir a imagem
docker build -t seu-docker-hub/btc-edc-m3-spark:3.1.1 -f docker/spark-operator.Dockerfile docker/


27 - [] docker push seu-docker-hub/btc-edc-m3-spark:3.1.1

28 - [] Rodar o job no airflow

29 - [] helm repo add pyspark-notebook https://a3data.github.io/pyspark-notebook-helm/

30 - [] helm repo update

31 - [] Criar imagem no docker hub seu-docker-hub/btc-edc-m3-notebook:3.1.1

32 - [] Buildar imagem do notebook docker build -t seu-docker-hub/btc-edc-m3-notebook:3.1.1 -f docker/notebook.Dockerfile docker/

****
33 - [] docker push kramerscs/btc-edc-m3-notebook:3.1.1

34 - [] helm install pyspark-notebook pyspark-notebook/pyspark-notebook -n processing -f manifests/notebook-values.yaml

35 - [] kubectl get all -n processing

36 - [] export POD_NAME=$(kubectl get pods --namespace processing -l "app.kubernetes.io/name=pyspark-notebook,app.kubernetes.io/instance=pyspark-notebook" -o jsonpath="{.items[0].metadata.name}")

37 - [] export CONTAINER_PORT=$(kubectl get pod --namespace processing $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")

38 - [] kubectl --namespace processing port-forward $POD_NAME 8888:$CONTAINER_POR

39 - [] kubectl get pods -n processing

40 - [] kubectl exec -it pods/pyspark-notebook-0 -n processing -- bash

41 - [] pegar o token jupyter server list

42 - [] fazer o upload 
