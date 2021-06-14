# ML project for ML in Production course

## Prerequisites

* Python >= 3.6
* pip >= 20.0.0
* docker
* [docker-compose](https://docs.docker.com/compose/install/) >= 1.25.0

## Usage

```bash
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")
docker-compose up --build
```


After that, go to http://localhost:8080/ (use `login = admin` and `password = admin`), unpause all DAGs, then, while `download` and `train` are running, go to Admin -> Variables (see the screenshot below) and add the variable with name `model` and value that is the date of any `train` DAG in `YYYY-MM-DD` format.
