# Motor de Busca em Documentos

Trabalho de Algoritmos Avancados - busca de palavras e trechos em documentos de texto usando algoritmos de substring search com observabilidade via OpenTelemetry.

## Funcionalidades

- upload de arquivos .txt e .pdf
- selecao do algoritmo de busca em tempo de execucao
- campo para digitar o termo ou trecho a buscar
- resultado exibindo, encontrado ou nao, numero de ocorrencias, posicoes no texto, tempo de execucao (ms), tamanho do texto N e do padrao M
- telemetria com OpenTelemetry - traces, metricas e logs
- dashboard no Grafana com comparacao entre algoritmos

## Algoritmos implementados

todos os 4 algoritmos

- **Forca Bruta** - O(N*M) no pior caso - compara caractere por caractere em cada posicao
- **Rabin-Karp** - O(N+M) no caso medio - usa hash rolante pra evitar comparacoes redundantes
- **KMP (Knuth-Morris-Pratt)** - O(N+M) garantido - tabela de falhas evita voltar no texto
- **Boyer-Moore** - O(N/M) no melhor caso - compara de tras pra frente e pula varios chars

## Arquitetura - Strategy Pattern

Cada algoritmo é uma classe independente com o metodo `buscar(texto, padrao)`. a classe `ContextoBusca` recebe o nome do algoritmo e delega a execucao pra estrategia certa em tempo de execucao. O front manda o nome via dropdown e o backend instancia a classe correta sem precisar de if-else espalhado.

## Como instalar e executar com docker

É preciso ter Docker e Python instalados.


```bash
git clone https://github.com/pamelabaronnn/motor-de-busca
python -m venv venv     - cria o ambiente virtual
venv\script\activate     - executa o ambiente virtual
pip install -r requirements.txt  - (caso vá rodar sem docker)
cd motor-de-busca
docker compose up --build
```

apos subir:
- aplicacao - http://localhost:5000
- grafana - http://localhost:3000 (usuario: admin       senha: admin)
- prometheus - http://localhost:9090

acesse http://localhost:5000. a telemetria vai logar no console ja que o otel collector não estará rodando.



## Rodar os testes

```bash
python testes.py
```

os testes validam todos os 4 algoritmos em 6 casos diferentes, comparando os resultados com o `str.find()` do python.

## Estrutura do projeto

```
motor-de-busca/
- app.py                    - aplicacao flask principal
- telemetria.py             - configuracao do opentelemetry
- testes.py                 - testes unitarios
- requirements.txt          - caso rode sem docker
- Dockerfile
- docker-compose.yaml
- otel-collector-config.yaml
- prometheus.yaml
- tempo.yaml
- algoritmos/
  - forca_bruta.py
  - rabin_karp.py
  - kmp.py
  - boyer_moore.py
  - contexto_busca.py       - strategy pattern
- templates/
  - index.html
-txt_testes/
  - A Biblia Sagrada, Contendo o Velho e o Novo Testamento.txt
  - Amor de Salvação.txt
  - La Catedral y el Bazar.txt
  -Os Lusíadas.txt
- grafana/
  - provisioning/           - datasources e dashboard pre-configurados
```

## Documentos de teste obrigatorios

Disponiveis em txt_testes
- Biblia
- Os Lusiadas - Camões
- A Catedral e o Bazar - Eric S. Raymond
- Amor de Salvação - obra adicional disponivel em Project Gutenberg

---

