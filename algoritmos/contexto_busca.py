from algoritmos.forca_bruta import ForcaBruta
from algoritmos.rabin_karp import RabinKarp
from algoritmos.kmp import KMP
from algoritmos.boyer_moore import BoyerMoore


# dicionario que mapeia o nome que vem do dropdown pra classe do algoritmo correspondente
# a troca de algoritmo acontece aqui em tempo de execucao 
algoritmos_disponiveis = {
    "forca-bruta": ForcaBruta,
    "rabin-karp": RabinKarp,
    "kmp": KMP,
    "boyer-moore": BoyerMoore,
}


class ContextoBusca:
    # o contexto e quem delega a busca pra estrategia certa

    def __init__(self, nome_algoritmo):
        if nome_algoritmo not in algoritmos_disponiveis:
            raise ValueError(f"algoritmo desconhecido - {nome_algoritmo}")
        # instancia a estrategia escolhida em tempo de execucao
        self._estrategia = algoritmos_disponiveis[nome_algoritmo]()
        self._nome = nome_algoritmo

    def executar_busca(self, texto, padrao):
        return self._estrategia.buscar(texto, padrao)

    @property
    def nome(self):
        return self._nome
