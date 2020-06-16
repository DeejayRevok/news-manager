# news-manager
News service news manager microservice

#### Local running

Run the parent's repo dev docker compose.

Inside the application folder run:
```
export JWT_SECRET={JWT_TOKEN_SECRET}
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements.txt
python webapp/main.py -p LOCAL
```