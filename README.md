# FastAPI template

## Installation

Use Docker & Docker Compose

- Clone Project
- Run docker-compose

```
$ docker-compose build      # build docker image depend on Dockerfile
$ docker-compose up -d      # auto build docker image depend on Dockerfile & run service
```

## Project structure

```
.
├── app
│   ├── api         // api endpoint
│   ├── core        // contain config of project
│   ├── db          // connect to db
│   ├── helpers     // helper functions
│   ├── migrations  // Contain database model, and alembic for auto generating migration
│   ├── schemas     // Pydantic Schema
│   ├── services    // Contain business logic and communicate 
│   └── main.py     // config middleware, handle exception etc
├── tests
│   ├── api         // contain file test for each api
│   ├── .env        // config DB test
│   └── conftest.py // config for testing
├── .gitignore
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── env.example
├── logging.ini     // config logging
├── README.md
└── requirements.txt
```

## Migration

- `alembic revision -m "your message" --autogenerate`   # Create migration versions depend on changed in models
- `alembic upgrade head`   # Upgrade to last version migration
- `alembic downgrade -1`   # Downgrade to before version migration

## Run code

- `pip install -r requirements.txt`
- `uvicorn --host 0.0.0.0 app.main:app --reload --reload-dir=app --port 8000`

## How to remove cache submodule

```
https://stackoverflow.com/questions/4185365/no-submodule-mapping-found-in-gitmodule-for-a-path-thats-not-a-submodule
```

- Flow template:

```bash
git submodule update --init

git rm --cached templates
```

## Kafka and proto

Example generate file python from proto

```bash
protoc -I=. --python_out=. app/dto/proto/booking.proto
```


Compile the .proto files...
```bash 
python -m grpc_tools.protoc -I definitions/ --python_out=definitions/builds/ --grpc_python_out=definitions/builds/ definitions/service.proto
```
