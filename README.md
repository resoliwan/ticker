# ticker

# Run server
```shell
docker-compose build
# or, make build

docker-compose up
# or, make up
```

# swagger
```
http://localhost/docs
```


## Requirements
* python 3.10
* docker with docker-compose
* [poetry](https://python-poetry.org/docs/)

## Creating a local dev environment
```shell
poetry install
```


## Running the tests
```shell
make up
make test

# or, if you have a local virtualenv
make unit
make inte
make e2e
```
