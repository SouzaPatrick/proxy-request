# Proxy Request

## Pré requisitos
- Python 3.10 ou superior
- PIP
- CMake (para rodar comando ```make```)

## Objetivo
O propósito deste projeto é criar uma lista de proxies válidas para uso pessoal, baixando acervos públicos e testando-os.

## A fazer
- [x] Utilizar uma proxy pública/privada para realizar uma request
- [x] Validar proxy, se está funcionando
- [x] Baixar proxies públicas para serem validadas
- [ ] Verificar pais de origem da proxy pelo IP através do https://ipapi.co/
- [ ] Flexibilizar o pais a qual quer utilizar a proxy
  - Dependendo da base pública que utilizar já traz o país de origem da proxy, caso não houver, é interessante o código analisar o pais de origem logo após a validação da proxy.
- [x] Rodar tudo com apenas um comando

## Antes de mais nada
Antes de mais nada, você precisará ter algumas libs pré-instaladas, recomendo usar o virtualenv para isso.

Neste caso será mostrado nos passos abaixo como criar uma virtualenv
```bash
$ python -m venv venv
```

Acesse a venv
```bash
$ source venv/bin/activate
```

Instale as dependencias(libs do projeto)
```bash
$ pip install -r requirements/dev-requirements.txt
```

###### É necessário criar um arquivo na raiz do projeto com o nome ```.env```, nele deve conter os seguintes dados:
```dotenv
#.env
DESTINATION_HOST=<URL_DESTINO_USADA_NOS_TESTES>
TIMEOUT_CHECK_PROXY=10
TTL_PROXY=5

```

---

## Iniciar o projeto - Primeiros comandos (dentro da ```venv```)
Para iniciar o projeto basta inserir o comando abaixo:
```bash
$ make install
```

Para baixar todas as listas de proxies pré instaladas insira o comando abaixo
```bash
$ make proxy
```

## Outros comandos
Para listar todos os comandos que podem ser usados basta informar
```bash
$ make help

Para rodar comandos: make alvo

Pre-commit
 - format: Format all code files

Start project
 - install: Create/reset the database

Commands
 - proxy: Download lists of public proxies
 - console: List all valid proxies
 - update: Revalidate valid proxies
```
###### Obs: O comando ```make help``` funciona apenas dentro da ```venv``` pois precisa da lib ```rich``` que ja foi instalada no ```dev-requirements.txt```

Para listar todas as proxies válidas basta informar
```bash
$ make console

                                  Table of valid proxies

  Nº   PROXY                  Url                          Protocol   Last check
 ─────────────────────────────────────────────────────────────────────────────────────────
  0    165.246.148.50:8088    https://www.sslproxies.org   http       01/03/2023 19:49:47
  1    201.17.26.54:80        https://www.sslproxies.org   http       01/03/2023 19:49:47
  2    172.105.253.213:3128   https://www.sslproxies.org   http       01/03/2023 19:49:47
  3    188.166.84.131:443     https://www.sslproxies.org   http       01/03/2023 19:49:47
  4    188.72.107.144:9090    https://www.sslproxies.org   http       01/03/2023 19:49:47
  5    118.27.113.167:8080    https://www.sslproxies.org   http       01/03/2023 19:49:47
  6    129.154.56.212:8088    https://www.sslproxies.org   http       01/03/2023 19:49:47
  7    146.59.127.168:80      https://www.sslproxies.org   http       01/03/2023 19:49:47
  8    116.98.181.242:10003   https://www.sslproxies.org   http       01/03/2023 19:49:47
  9    103.121.149.69:8080    https://www.sslproxies.org   http       01/03/2023 19:49:47
  10   116.98.230.208:10003   https://www.sslproxies.org   http       01/03/2023 19:49:47
  11   13.75.216.118:3128     https://www.sslproxies.org   http       01/03/2023 19:49:47
  12   114.7.27.98:8080       https://www.sslproxies.org   http       01/03/2023 19:49:47
  13   195.154.32.138:3128    https://www.sslproxies.org   http       01/03/2023 19:49:47
  14   20.241.236.196:3128    https://www.sslproxies.org   http       01/03/2023 19:49:47
  15   116.98.238.128:10003   https://www.sslproxies.org   http       01/03/2023 19:49:47
  16   116.98.182.19:10003    https://www.sslproxies.org   http       01/03/2023 19:49:47
  17   170.2.210.201:80       https://www.sslproxies.org   http       01/03/2023 19:49:47
```

Para retestar as listas que conseguiu e verificar se aquelas proxies ainda estão ativas, informe:
```bash
$ make update
```
