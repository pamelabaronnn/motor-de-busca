import time


# algoritmo kmp, quando da um mismatch ele nao volta pro inicio do padrao, usa uma tabela de falhas pra saber ate onde pode pular
# complexidade O(N+M) garantido
class KMP:

    def _construir_tabela_falhas(self, padrao):
        # a tabela de falhas diz o tamanho do maior prefixo do padrao que tambem é sufixo, serve pra nao comparar de novo o que ja foi comparado
        tamanho = len(padrao)
        tabela = [0] * tamanho
        tamanho_prefixo = 0
        i = 1

        while i < tamanho:
            if padrao[i] == padrao[tamanho_prefixo]:
                tamanho_prefixo += 1
                tabela[i] = tamanho_prefixo
                i += 1
            else:
                if tamanho_prefixo != 0:
                    # volta na tabela sem incrementar i
                    tamanho_prefixo = tabela[tamanho_prefixo - 1]
                else:
                    tabela[i] = 0
                    i += 1

        return tabela

    def buscar(self, texto, padrao):
        inicio = time.perf_counter()

        posicoes = []
        tamanho_texto = len(texto)
        tamanho_padrao = len(padrao)

        if tamanho_padrao > tamanho_texto:
            fim = time.perf_counter()
            tempo_ms = (fim - inicio) * 1000
            return self._montar_resultado(posicoes, tamanho_texto, tamanho_padrao, tempo_ms)

        tabela = self._construir_tabela_falhas(padrao)

        i = 0  # indice no texto
        j = 0  # indice no padrao

        while i < tamanho_texto:
            if texto[i] == padrao[j]:
                i += 1
                j += 1

            if j == tamanho_padrao:
                # achou uma ocorrencia, a posicao de inicio é i - j
                posicoes.append(i - j)
                # usa a tabela pra saber onde continuar sem voltar ao inicio
                j = tabela[j - 1]
            elif i < tamanho_texto and texto[i] != padrao[j]:
                if j != 0:
                    # pula usando a tabela de falhas
                    j = tabela[j - 1]
                else:
                    i += 1

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
