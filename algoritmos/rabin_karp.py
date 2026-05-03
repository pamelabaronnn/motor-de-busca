import time


# algoritmo rabin-karp, usa hash rolante pra evitar comparar tudo de novo, a ideia é calcular um hash do padrao e do trecho do texto, se os hashes batem, ai sim compara caractere por caractere evitando falsos positivos
# complexidade  O(N+M) no caso medio
class RabinKarp:

    # base e modulo primos ajudam a distribuir melhor os hashes e evitar colisoes
    BASE = 256
    MODULO = 101

    def buscar(self, texto, padrao):
        inicio = time.perf_counter()

        posicoes = []
        tamanho_texto = len(texto)
        tamanho_padrao = len(padrao)

        if tamanho_padrao > tamanho_texto:
            fim = time.perf_counter()
            tempo_ms = (fim - inicio) * 1000
            return self._montar_resultado(posicoes, tamanho_texto, tamanho_padrao, tempo_ms)

        # fator pra remover o caractere mais antigo da janela BASE^(M-1) % MODULO
        fator = 1
        for _ in range(tamanho_padrao - 1):
            fator = (fator * self.BASE) % self.MODULO

        # calcula o hash inicial do padrao e da primeira janela do texto
        hash_padrao = 0
        hash_janela = 0
        for i in range(tamanho_padrao):
            hash_padrao = (self.BASE * hash_padrao + ord(padrao[i])) % self.MODULO
            hash_janela = (self.BASE * hash_janela + ord(texto[i])) % self.MODULO

        # desliza a janela pelo texto
        for i in range(tamanho_texto - tamanho_padrao + 1):
            # hashes iguais precisa confirmar pra evitar falso positivo
            if hash_padrao == hash_janela:
                if texto[i:i + tamanho_padrao] == padrao:
                    posicoes.append(i)

            # recalcula o hash da proxima janela removendo o primeiro e adicionando o proximo
            if i < tamanho_texto - tamanho_padrao:
                hash_janela = (
                    self.BASE * (hash_janela - ord(texto[i]) * fator) + ord(texto[i + tamanho_padrao])
                ) % self.MODULO

                # garante que o hash nao fique negativo
                if hash_janela < 0:
                    hash_janela += self.MODULO

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
