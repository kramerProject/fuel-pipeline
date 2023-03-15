1 - [X] Subir IAC conforme aula 3_5

aws eks update-kubeconfig --region us-east-1 --name btc-edc-m3-kramer-eks

helm repo add apache-airflow https://airflow.apache.org

2 - [X] kubectl create ns airflow

3 - [X] kubectl create secret -n airflow generic aws-secret \
--from-literal=AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
--from-literal=AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
--from-literal=AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

4 - [X] kubectl apply -f manifests/airflow-crb.yaml -n airflow

5 - [X] Criar a fernet key e webserver secret key do arquivo do airflow
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
python -c 'import secrets; print(secrets.token_hex(16))'

6 - [X] Criar bucket de logs do airflow, precisa colocar o caminho no manifesto do airflow 
linha 1688
remote_base_log_folder: s3://airflow-logs-401868797180/edc-btc-m3
remote_log_conn_id: my_s3_conn

7 - [X] Colocar o caminho das dags no manifest do airflow 1787

8 - [X] Fazer / Conferir arquivos dags

9 - [X] Subir dags no github


10 - helm repo add apache-airflow https://airflow.apache.org

11 - helm repo update

10 - [X] helm upgrade --install airflow apache-airflow/airflow --namespace airflow -f manifests/airflow-values.yaml --create-namespace --version 1.7.0
 ou tentar se já tiver criado o name space
 helm install airflow apache-airflow/airflow --version 1.7.0 -n airflow -f manifests/airflow-values.yaml

caso reinicie sem limpar o kubectl
 kubectl port-forward service/airflow-webserver -n airflow 8080:8080

11 - [X] Cadastrar a connection "my_s3_conn" na UI do Airflow:
connection type Amazon Web Services


15 - [X] criar cluster connection id no airflow kubernetes_default
connection type Kubernetes Cluster Connection


1 - [X] Criar variavel de ambiente source urls no airflow
combustiveis_source_urls
[
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2015-01.csv",
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2015-02.csv",
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/ca-2016-01.csv"
]

12 - [X] helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

13 - [X] helm repo update

12 - [X] helm install spark-operator spark-operator/spark-operator --namespace processing \
--create-namespace -f manifests/spark-operator-values.yaml --version 1.1.26

13 - [X] kubectl create secret -n processing generic aws-secret \
--from-literal=AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> \
--from-literal=AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> \
--from-literal=AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

14 - [X] Criação dos buckets para a camada landing e a camada bronze

15 - [X] Conferir arquivos de ingestão e processamento do job

15 - [X] Buildar e subir a imagem
docker build -t kramerscs/btc-edc-m3-spark:3.1.1 -f docker/spark-operator.Dockerfile docker/


16 - [X] docker push kramerscs/btc-edc-m3-spark:3.1.1

16 - Rodar o job no airflow

17 - Helm chart notebook

