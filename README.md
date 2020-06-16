# news-manager
News service news manager microservice

![News Manager](https://github.com/DeejayRevok/news-manager/workflows/News%20Manager/badge.svg?branch=develop)
[![codecov](https://codecov.io/gh/DeejayRevok/news-manager/branch/develop/graph/badge.svg?token=AOD98UF75k)](https://codecov.io/gh/DeejayRevok/news-manager)

#### Local running

Run the parent's repo dev docker compose.

Inside the application folder run:
```
export JWT_SECRET={JWT_TOKEN_SECRET}
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements.txt
python webapp/main.py -p LOCAL
```
