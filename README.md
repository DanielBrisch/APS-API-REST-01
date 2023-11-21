# APS 01 - API REST com Postgres

Integrantes:

- Cezar Augusto Mezzalira

## Iniciando o projeto do zero

Siga esse passo a passo caso queira criar o projeto do zero.

### Criando a pasta do projeto e abrindo com o VSCode

O primeiro passo é criar uma pasta vazia para o projeto, de preferencia na pasta onde você costuma armazenar seus projetos.

Você pode usar gerenciador de arquivos do sistema para fazer isso.

Em seguida, abra o Visual Studio Code, vá até o menu `File>Open Folder` ou em português `Arquivo>Abrir Pasta`, navegue até a pasta criada e abra ela.

Agora, com o projeto aberto, vamos abrir o nosso terminal, através do menu `Terminal>New Terminal` ou português `Terminal>Novo Terminal`.

O uso do terminal é importante, pois, quando colocarmos uma aplicação para funcionar na prática em um servidor, só teremos um terminal a nossa disposição.

### Inicializando o projeto com Git

Utilizaremos o Git como ferramenta de versionamento de código do nosso projeto.

Antes de inicializar o nosso projeto, vamos criar na raiz um novo arquivo, chamado `.gitignore`.

Dentro dele, coloque o seguinte conteúdo:

```
.venv
__pycache__
```

Em seguida, digite o comando `git init` para que o seu projeto se torne um repositório.

### Inicializando o projeto com o poetry

O próximo passo é a inicializar o projeto com o poetry.

Caso ainda não tenha instalado, execute o comando `pip install poetry` no seu terminal.

Em seguida, caso tenha instalado o poetry, execute o comando `poetry config virtualenvs.in-project true`. Esse comando faz com que seja criado automaticamente dentro da pasta do nosso projeto um novo ambiente virtual, sem precisarmos nos preocupar com isso.

Em seguida, dentro do terminal que está aberto em nosso VSCode, vamos inicializar o projeto com `poetry init`.

Ao executar esse comando, serão feitas algumas perguntas, as quais vão gerar o arquivo `pyproject.toml` na raiz do seu projeto.

A primeira pergunta será o nome do pacote, o qual você pode deixar o nome do seu projeto, aperte `Enter`.

Em seguida será pedida a versão do seu projeto que pode ser a `0.1.0`. Aperte `Enter` novamente.

Depois será pedida uma descrição do projeto. Você pode colocar um pequeno texto aqui ou não e aperte `Enter`.

Agora, ele pede o autor do projeto. Se você estiver com o git configurado corretamente, ele vai pegar seu nome e email automaticamente. Se estiver tudo certo, aperte `Enter`.

Em seguida, é solicitado a licença do seu projeto, a qual por hora deixamos em branco e pressionamos `Enter`.

Na sequencia, é pedida a versão minima do python que o seu projeto precisa para ser executado, sendo que a versão que aparece é a versão que está rodando no seu computador. Vamos deixar a versão que está e pressionar `Enter`.

Nas duas próximas perguntas, são solicitados se queremos instalar as dependencias do nosso projeto de modo interativo. Você pode pressionar `n` e depois `Enter` para ambas.

Na última pergunta, ele pede se você deseja criar o arquivo `pyprject.toml`. Pressione `y` e depois `Enter`.

Agora, o nosso projeto já pode ser gerenciado com o poetry.

Abaixo exemplo da saída do comando `poetry init`:

```shell

$ poetry init

This command will guide you through creating your pyproject.toml config.

Package name [teste-poetry]:
Version [0.1.0]:
Description []:
Author [Cezar Augusto Mezzalira <email@email.com>, n to skip]:
License []:
Compatible Python versions [^3.12]:

Would you like to define your main dependencies interactively? (yes/no) [yes] n
Would you like to define your development dependencies interactively? (yes/no) [yes] n
Generated file

[tool.poetry]
name = "teste-poetry"
version = "0.1.0"
description = ""
authors = ["Cezar Augusto Mezzalira <email@email.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes] y
```

## Instalando as dependências do projeto

Ainda no terminal, vamos instalar as dependências que o nosso projeto precisará, executando o comando abaixo:

```shell
poetry add fastapi uvicorn sqlmodel psycopg2-binary
```

## Criando a base do projeto

Para testarmos nosso projeto, vamos criar na raiz dele uma pasta chamada `src` e dentro dela um arquivo chamado `server.py`.

Em seguida, vamos criar a nossa primeira rota. Para isso copie o código abaixo para dentro do arquivo `server.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}

```

Com o código acima, já conseguimos testar a nossa aplicação.

## Iniciando o servidor HTTP

```shell
poetry run uvicorn src.server:app --reload
```

Através do nosso navegador (Chrome, Edge, Firefox), vamos testar se nossa rota `healthcheck` está funcionando.

Vamos digitar na barra de endereços `http://localhost:8000/healthcheck`.

Deverá aparecer na tela a mensagem `{"status": "ok"}`.

## Configurando o banco de dados

Agora, com nosso projeto já configurado, vamos precisar subir um banco de dados dentro do nosso docker.

### Subindo um container docker com o postgres

Para esse trabalho, vamos precisar subir um novo container docker com o postgres para usa-lo como nosso banco de dados.

#### Passos para usuários Windows

Como vimos nas aulas anteriores, nosso docker está rodando dentro do WSL (Windows Subsystem Linux) que é uma espécie de máquina virtual que roda uma distribuição Linux, que no nosso caso é um Ubuntu 22.04 somente com terminal.

Vamos então abrir nosso Linux. Recomendo executar um novo terminal fora do VSCode, indo através do menu iniciar, digite powershell e depois clique no programa `Windows PowerShell`.

Dentro do PowerShell, digite o comando `wsl`. Esse comando inicializa nosso Ubuntu Linux dentro da mesma janela do PowerShell.

Assim que carregar, siga para a próxima sessão.

#### Iniciando um container docker com postgres

Para iniciar um container docker com o postgres, basta executar o comando abaixo:

```shell
docker run --name pg-db -p 54322:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=race_db -d postgres:14
```

Nosso postgres estará rodando no host `localhost`, porta `54322`, com usuário `root` e senha `postgres` e irá criar o banco que vamos usar nessa aplicação com o nome de `race_db`.

### Criando o arquivo de configuração de banco de dados

Para usarmos o banco de dados na nossa API, vamos criar um arquivo de configuração para centralizarmos a responsabilidade do que relacionado a banco de dados.

Vamos criar uma nova pasta, dentro da pasta `src` com nome `config`. Dentro da pasta `config` vamos criar um arquivo novo chamado `database.py`.

Agora, abra o arquivo [database.py](https://gist.github.com/cezarmezzalira/a112c6f576615abee97b876523834138) no Gist, copie e cole dentro do arquivo `database.py` do seu projeto.

### Criando os modelos de mapeamento do banco (ORM)

Uma vez que já temos nossa configuração do banco, vamos criar os modelos que vamos precisar nesse projeto.

Para isso, crie uma pasta chamada `models` dentro de `src`.

Em seguida crie dois arquivos: `provas_model.py` e `resultados_model.py`.

Agora, copie do Gist que está nesse [link](https://gist.github.com/cezarmezzalira/a6feb6004890d0fcf33028fabe09ac19) o conteúdo de cada um dos arquivos.

### Ajustando o server para subir as configurações do banco

Com o SQLModel, ao criarmos nosso mapeamento, podemos executar um comando que irá criar as tabelas do nosso banco de dados, baseado nos modelos.

Para isso acontecer, vamos alterar nosso arquivo `server.py` conforme abaixo:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

```

Através da chamada da função `create_db_and_tables` dentro da função assincrona `lifespan`, são criadas no nosso banco de dados as tabelas `provas` e `resultados`.

## Configurando as rotas

Agora, vamos criar as primeiras rotas para cada uma das nossas tabelas.

Para isso, vamos criar uma nova pasta dentro de `src` chamada `routes`.

Dentro da pasta `routes` vamos criar dois arquivos: `provas_routes.py` e `resultados_routes.py`.

Agora, copie o conteúdo dos dois arquivos que está no Gist através desse [link](https://gist.github.com/cezarmezzalira/e79a6a8a62ce5e68e70f68ffc5298a7d).

### Adicionando as rotas ao servidor

Para finalizarmos, vamos adicionar ao nosso servidor as rotas que criamos.

Para isso, no arquivo `server.py` vamos fazer o import dos arquivos das rotas e incluir na instancia do `app` as rotas.

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import create_db_and_tables

# import das novas rotas
from src.routes.provas_routes import provas_router
from src.routes.resultados_routes import resultados_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Inclusão de novas rotas
app.include_router(provas_router)
app.include_router(resultados_router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

```

### Testando as rotas

Para finalizar, vamos testar as rotas usando um client HTTP (Postman, Insomnia ou Thunder Client).

Vamos testar a primeira rota que é a criação de provas, criando uma chamada do tipo `POST` para URL `http://localhost:8000/provas` com seguinte body:

```json
{
  "descricao": "Prova 1",
  "data_prova": "2023-11-20T19:10:000",
  "q1": "A",
  "q2": "B",
  "q3": "C",
  "q4": "D",
  "q5": "A",
  "q6": "B",
  "q7": "C",
  "q8": "D",
  "q9": "A",
  "q10": "B"
}
```

O retorno esperado é um retorno com status code 200 e com seguinte body:

```json
{
  "q1": "A",
  "descricao": "Prova 1",
  "id": 1,
  "q2": "B",
  "q3": "C",
  "q5": "A",
  "q7": "C",
  "q9": "A",
  "data_prova": "2023-11-20T19:10:000",
  "q4": "D",
  "q6": "B",
  "q8": "D",
  "q10": "B"
}
```

A segunda rota que vamos testar é a criação de resultado.

Vamos criar uma nova requisição do tipo `POST` no endereço `http://localhost:8000/resultados` com o seguinte body:

```json
{
  "nome": "Fulano",
  "prova_id": 1,
  "q1": "A",
  "q2": "B",
  "q3": "C",
  "q4": "D",
  "q5": "A",
  "q6": "B",
  "q7": "C",
  "q8": "D",
  "q9": "A",
  "q10": "B"
}
```

O resultado esperado é um status 200 com o seguinte body:

```json
{
  "q1": "A",
  "q3": "C",
  "q5": "A",
  "q7": "C",
  "q9": "A",
  "nota": 10.0,
  "nome": "Fulano",
  "id": 1,
  "q2": "B",
  "q4": "D",
  "q6": "B",
  "q8": "D",
  "q10": "B",
  "prova_id": 1
}
```
