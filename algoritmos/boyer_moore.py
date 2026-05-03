import time


# algoritmo boyer-moore  pra textos naturais, compara o padrao de tras pra frente
# usa duas heuristicas, bad character e good suffix
# pode pular varios caracteres de uma vez, sublinear no melhor caso O(N/M)
class BoyerMoore:

    def _construir_tabela_bad_char(self, padrao):
        # bad character, quando da mismatch, pula ate o ultimo lugar onde aquele caractere aparece no padrao e se nao aparece, pula o padrao inteiro
        tabela = {}
        for i, char in enumerate(padrao):
            tabela[char] = i
        return tabela

    def _construir_tabela_good_suffix(self, padrao):
        # good suffix, quando da mismatch, usa o sufixo que ja casou pra decidir quanto pular sem perder nenhuma ocorrencia
        tamanho = len(padrao)
        tabela = [tamanho] * (tamanho + 1)
        borda = [0] * (tamanho + 1)

        i = tamanho
        j = tamanho + 1
        borda[i] = j

        while i > 0:
            while j <= tamanho and padrao[i - 1] != padrao[j - 1]:
                if tabela[j] == tamanho:
                    tabela[j] = j - i
                j = borda[j]
            i -= 1
            j -= 1
            borda[i] = j

        j = borda[0]
        for i in range(tamanho + 1):
            if tabela[i] == tamanho:
                tabela[i] = j
            if i == j:
                j = borda[j]

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

        tabela_bc = self._construir_tabela_bad_char(padrao)
        tabela_gs = self._construir_tabela_good_suffix(padrao)

        i = 0  # posicao no texto
        while i <= tamanho_texto - tamanho_padrao:
            j = tamanho_padrao - 1  # começa a comparar pelo final do padrao

            # vai comparando de tras pra frente
            while j >= 0 and padrao[j] == texto[i + j]:
                j -= 1

            if j < 0:
                # achou uma ocorrencia
                posicoes.append(i)
                # usa good suffix pra decidir o proximo salto
                i += tabela_gs[0]
            else:
                # mismatch escolhe o maior salto entre as duas heuristicas
                char_texto = texto[i + j]
                salto_bc = j - tabela_bc.get(char_texto, -1)
                salto_gs = tabela_gs[j + 1]
                i += max(salto_bc, salto_gs)

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
