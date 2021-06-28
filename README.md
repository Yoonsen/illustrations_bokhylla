# illustrations_bokhylla
Fetch illustrations from bokhylla



# Dockerfile
`FROM python:3.8
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run app.py`

`docker build -t gcr.io/norwegian-language-bank/appname:v1 .
kubectl create deployment foodlessons-app --image=gcr.io/norwegian-language-bank/foodlessons_webapp:v1
kubectl expose deployment foodlessons-app --name=foodlessons-app-service --type=LoadBalancer --port 80 --target-port 8501
`
