import time


# algoritmo de forca bruta, mais simples de todos, compara o padrao com cada posicao do texto, caractere por caractere
# complexidade O(N*M) no pior caso
class ForcaBruta:

    def buscar(self, texto, padrao):
        inicio = time.perf_counter()

        posicoes = []
        tamanho_texto = len(texto)
        tamanho_padrao = len(padrao)

        # se o padrao for maior que o texto não precisa tentar
        if tamanho_padrao > tamanho_texto:
            fim = time.perf_counter()
            tempo_ms = (fim - inicio) * 1000
            return self._montar_resultado(posicoes, tamanho_texto, tamanho_padrao, tempo_ms)

        # percorre cada posicao possivel do texto
        for i in range(tamanho_texto - tamanho_padrao + 1):
            j = 0
            # tenta casar o padrao a partir da posicao i
            while j < tamanho_padrao and texto[i + j] == padrao[j]:
                j += 1
            # se j chegou no fim do padrao, encontrou uma ocorrencia
            if j == tamanho_padrao:
                posicoes.append(i)

        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000
        return self._montar_resultado(posicoes, tamanho_texto, tamanho_padrao, tempo_ms)

    def _montar_resultado(self, posicoes, n, m, tempo_ms):
        return {
            "posicoes": posicoes,
            "ocorrencias": len(posicoes),
            "encontrado": len(posicoes) > 0,
            "tempo_ms": round(tempo_ms, 4),
            "n": n,
            "m": m,
        }
