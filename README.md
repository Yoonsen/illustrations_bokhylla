# illustrations_bokhylla
Fetch illustrations from bokhylla



# Dockerfile

Legg inn i en fil ved navn `Dockerfile`

```
FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run <file-name>.py
```

Kjør kommandoene i terminal
```
docker build -t gcr.io/norwegian-language-bank/appname:v1 .
kubectl create deployment <appname> --image=gcr.io/norwegian-language-bank/<file-name>:v1
kubectl expose deployment <appname> --name=<app-service-name> --type=LoadBalancer --port 80 --target-port 8501
```
