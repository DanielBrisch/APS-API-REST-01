# APS 01 - API REST com Postgres

Integrantes: 
- Fulano de tal
- Ciclano de tal


## Dependências do projeto

```shell
poetry add fastapi
poetry add sqlmodel
poetry add uvicorn
poetry add psycopg2-binary
```


## Iniciando o servidor HTTP

```shell
uvicorn src.server:app --reload
```

Caso queira subir sem carregar o shell, execute o comando abaixo:

```shell
poetry run uvicorn src.server:app --reload
```
