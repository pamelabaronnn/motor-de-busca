import os
import io
from flask import Flask, request, jsonify, render_template
from algoritmos.contexto_busca import ContextoBusca, algoritmos_disponiveis
from telemetria import tracer, registrar_busca
from opentelemetry import trace

# suporte a pdf
try:
    import pypdf
    suporte_pdf = True
except ImportError:
    suporte_pdf = False

app = Flask(__name__)

# limite de upload 20mb suficiente pra textos grandes e PDFs simples, mas evita abusos e arquivos muito pesados que podem travar o app
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


def extrair_texto_do_arquivo(arquivo):
    # tenta descobrir o tipo pelo nome do arquivo
    nome = arquivo.filename.lower()

    if nome.endswith(".pdf"):
        if not suporte_pdf:
            raise ValueError("suporte a pdf nao disponivel - instale pypdf")
        # le o pdf em bytes e extrai o texto pagina por pagina
        conteudo_bytes = arquivo.read()
        leitor = pypdf.PdfReader(io.BytesIO(conteudo_bytes))
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto

    elif nome.endswith(".txt"):
        # tenta utf-8 primeiro, se falhar tenta latin-1 
        conteudo_bytes = arquivo.read()
        try:
            return conteudo_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return conteudo_bytes.decode("latin-1")

    else:
        raise ValueError("formato nao suportado - use .txt ou .pdf")


@app.route("/")
def index():
    nomes_algoritmos = list(algoritmos_disponiveis.keys())
    return render_template("index.html", algoritmos=nomes_algoritmos, suporte_pdf=suporte_pdf)


@app.route("/buscar", methods=["POST"])
def buscar():
    # um trace por requisicao span raiz
    with tracer.start_as_current_span("requisicao-busca") as span_raiz:
        try:
            arquivo = request.files.get("arquivo")
            padrao = request.form.get("padrao", "").strip()
            nome_algoritmo = request.form.get("algoritmo", "forca-bruta")

            if not arquivo or not arquivo.filename:
                return jsonify({"erro": "nenhum arquivo enviado"}), 400

            if not padrao:
                return jsonify({"erro": "campo de busca nao pode estar vazio"}), 400

            # span de leitura do arquivo
            with tracer.start_as_current_span("leitura-arquivo") as span_leitura:
                span_leitura.set_attribute("arquivo.nome", arquivo.filename)
                texto = extrair_texto_do_arquivo(arquivo)
                span_leitura.set_attribute("arquivo.tamanho_chars", len(texto))

            if not texto.strip():
                return jsonify({"erro": "arquivo vazio ou sem texto legivel"}), 400

            # span de execucao do algoritmo
            with tracer.start_as_current_span("execucao-algoritmo") as span_algo:
                span_algo.set_attribute("algoritmo.nome", nome_algoritmo)
                span_algo.set_attribute("padrao.tamanho", len(padrao))

                contexto = ContextoBusca(nome_algoritmo)
                resultado = contexto.executar_busca(texto, padrao)

                span_algo.set_attribute("resultado.ocorrencias", resultado["ocorrencias"])
                span_algo.set_attribute("resultado.tempo_ms", resultado["tempo_ms"])

            # span de formatacao do resultado
            with tracer.start_as_current_span("formatacao-resultado"):
                registrar_busca(nome_algoritmo, texto, padrao, resultado)

                # manda so as primeiras 100 posicoes pra nao travar o front com textos gigantes
                posicoes_exibidas = resultado["posicoes"][:100]
                tem_mais = resultado["ocorrencias"] > 100

                resposta = {
                    "encontrado": resultado["encontrado"],
                    "ocorrencias": resultado["ocorrencias"],
                    "posicoes": posicoes_exibidas,
                    "tem_mais_posicoes": tem_mais,
                    "tempo_ms": resultado["tempo_ms"],
                    "n": resultado["n"],
                    "m": resultado["m"],
                    "algoritmo": nome_algoritmo,
                }

            span_raiz.set_attribute("busca.sucesso", True)
            return jsonify(resposta)

        except ValueError as e:
            span_raiz.set_attribute("busca.sucesso", False)
            span_raiz.record_exception(e)
            return jsonify({"erro": str(e)}), 400
        except Exception as e:
            span_raiz.set_attribute("busca.sucesso", False)
            span_raiz.record_exception(e)
            return jsonify({"erro": f"erro inesperado - {str(e)}"}), 500


if __name__ == "__main__":
    porta = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=False)
