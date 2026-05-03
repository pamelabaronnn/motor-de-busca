import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
import os


# configura o logger padrao do python junto com otel
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("motor-de-busca")


def configurar_otel():
    # recurso identifica a aplicacao nos traces e metricas
    recurso = Resource.create({"service.name": "motor-de-busca"})

    # endpoint do otel collector - padrao local via docker
    endpoint_otel = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

    # configura o tracer
    try:
        exportador_traces = OTLPSpanExporter(endpoint=endpoint_otel, insecure=True)
        provedor_traces = TracerProvider(resource=recurso)
        provedor_traces.add_span_processor(BatchSpanProcessor(exportador_traces))
        trace.set_tracer_provider(provedor_traces)
    except Exception as e:
        logger.warning(f"nao conseguiu conectar ao otel collector pra traces - {e}")
        trace.set_tracer_provider(TracerProvider(resource=recurso))

    # configura as metricas
    try:
        exportador_metricas = OTLPMetricExporter(endpoint=endpoint_otel, insecure=True)
        leitor = PeriodicExportingMetricReader(exportador_metricas, export_interval_millis=5000)
        provedor_metricas = MeterProvider(resource=recurso, metric_readers=[leitor])
        metrics.set_meter_provider(provedor_metricas)
    except Exception as e:
        logger.warning(f"nao conseguiu conectar ao otel collector pra metricas - {e}")
        metrics.set_meter_provider(MeterProvider(resource=recurso))

    return trace.get_tracer("motor-de-busca"), metrics.get_meter("motor-de-busca")


tracer, meter = configurar_otel()

# metricas obrigatorias 
histograma_duracao = meter.create_histogram(
    name="search_duration_ms",
    description="tempo de execucao da busca em milissegundos",
    unit="ms",
)

contador_buscas = meter.create_counter(
    name="search_requests_total",
    description="total de buscas realizadas",
)

histograma_tamanho_doc = meter.create_histogram(
    name="document_size_chars",
    description="tamanho do documento em caracteres",
)


def registrar_busca(nome_algoritmo, texto, padrao, resultado):
    # labels pra filtrar no grafana
    labels = {
        "algorithm": nome_algoritmo,
        "found": str(resultado["encontrado"]).lower(),
    }

    # log de inicio
    logger.info(
        f"iniciando busca - algoritmo={nome_algoritmo} | N={resultado['n']} | M={resultado['m']}"
    )

    # registra as metricas
    histograma_duracao.record(resultado["tempo_ms"], labels)
    contador_buscas.add(1, labels)
    histograma_tamanho_doc.record(resultado["n"], {"algorithm": nome_algoritmo})

    # log de conclusao
    logger.info(
        f"busca concluida - tempo={resultado['tempo_ms']}ms | ocorrencias={resultado['ocorrencias']}"
    )
