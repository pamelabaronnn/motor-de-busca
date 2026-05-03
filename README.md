# Motor de Busca em Documentos

Trabalho pratico de Algoritmos Avancados. Busca de palavras e trechos em documentos de texto usando algoritmos de substring search com observabilidade via OpenTelemetry.

**Integrantes**
- Pâmela Baron
- Dereck Conink

---

## Funcionalidades

- Upload de arquivos `.txt` e `.pdf`
- Selecao do algoritmo de busca em tempo de execucao via dropdown
- Campo para digitar o termo ou trecho a buscar
- Area de resultados exibindo: encontrado ou nao, numero de ocorrencias, posicoes no texto, tempo de execucao em ms, tamanho do texto N e do padrao M
- Telemetria com OpenTelemetry — traces, metricas e logs
- Dashboard no Grafana com comparacao de desempenho entre algoritmos

---

## Algoritmos implementados

Todos os 4 algoritmos foram implementados.

| Algoritmo | Complexidade | Como funciona |
|---|---|---|
| Forca Bruta | O(N\*M) pior caso | Compara caractere por caractere em cada posicao |
| Rabin-Karp | O(N+M) caso medio | Hash rolante evita comparacoes redundantes |
| KMP | O(N+M) garantido | Tabela de falhas evita voltar no texto |
| Boyer-Moore | O(N/M) melhor caso | Compara de tras pra frente e pula varios chars |

---

## Arquitetura — Strategy Pattern

Cada algoritmo e uma classe independente com o metodo `buscar(texto, padrao)`. A classe `ContextoBusca` recebe o nome do algoritmo escolhido no dropdown e delega a execucao para a estrategia correta em tempo de execucao, sem if-else espalhado no codigo.

---

## Como executar

### Pre-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado e rodando
- [Python 3.10+](https://www.python.org/downloads/)

### Com Docker

Sobe a aplicacao junto com toda a stack de observabilidade.

```bash
git clone https://github.com/pamelabaronnn/motor-de-busca
cd motor-de-busca
python -m venv venv
venv\Scripts\activate
docker compose up --build
```

> A primeira vez demora mais porque o Docker precisa baixar as imagens.

Apos subir, acesse:

| Servico | Endereco | Credenciais |
|---|---|---|
| Aplicacao | http://localhost:5000 | — |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |

### Sem Docker

Roda apenas a aplicacao Flask. A telemetria registra os logs no console.

```bash
git clone https://github.com/pamelabaronnn/motor-de-busca
cd motor-de-busca
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse em http://localhost:5000

---

## Testes

Os testes validam todos os 4 algoritmos em 6 casos diferentes, comparando os resultados com `str.find()` do Python.

```bash
python testes.py
```

Saida esperada:

```
total - 24 | passou - 24 | falhou - 0
todos os testes passaram!
```

---

## Estrutura do projeto

```
motor-de-busca/
├── app.py                      # aplicacao Flask principal
├── telemetria.py               # configuracao do OpenTelemetry
├── testes.py                   # testes unitarios
├── requirements.txt            # dependencias para rodar sem Docker
├── Dockerfile
├── docker-compose.yaml
├── otel-collector-config.yaml
├── prometheus.yaml
├── tempo.yaml
├── algoritmos/
│   ├── forca_bruta.py
│   ├── rabin_karp.py
│   ├── kmp.py
│   ├── boyer_moore.py
│   └── contexto_busca.py       # strategy pattern
├── templates/
│   └── index.html
├── txt_testes/
│   ├── A Biblia Sagrada, Contendo o Velho e o Novo Testamento.txt
│   ├── Amor de Salvacao.txt
│   ├── La Catedral y el Bazar.txt
│   └── Os Lusiadas.txt
└── grafana/
    └── provisioning/           # datasources e dashboard pre-configurados
```

---

## Documentos de teste

Disponiveis na pasta `txt_testes/`.

| Documento | Autor | Observacao |
|---|---|---|
| A Biblia Sagrada | Dominio publico | Texto longo — bom para testes de desempenho com N grande |
| Os Lusiadas | Luis de Camoes | Literatura portuguesa com acentuacao e caracteres especiais |
| La Catedral y el Bazar | Eric S. Raymond | Ensaio tecnico sobre software open source |
| Amor de Salvacao | Camilo Castelo Branco | Obra adicional — disponivel no Project Gutenberg |

---

## Observabilidade

Stack completa via `docker compose up`:

```
Aplicacao Flask
      |
      v
OTEL Collector
      |
      +---------> Prometheus (metricas)
      |
      +---------> Tempo (traces)
                      |
                      v
                  Grafana (dashboard)
```

O dashboard exibe tempo medio de busca por algoritmo, total de buscas realizadas e comparacao visual entre os algoritmos.

---

