import sys
import os

# garante que os modulos do projeto sao encontrados
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algoritmos.forca_bruta import ForcaBruta
from algoritmos.rabin_karp import RabinKarp
from algoritmos.kmp import KMP
from algoritmos.boyer_moore import BoyerMoore


# casos de teste usados pra validar todos os algoritmos
casos_de_teste = [
    {
        "descricao": "padrao presente uma vez",
        "texto": "algoritmos avancados sao muito legais",
        "padrao": "avancados",
        "ocorrencias_esperadas": 1,
        "encontrado_esperado": True,
    },
    {
        "descricao": "padrao presente varias vezes",
        "texto": "abababab",
        "padrao": "ab",
        "ocorrencias_esperadas": 4,
        "encontrado_esperado": True,
    },
    {
        "descricao": "padrao nao encontrado",
        "texto": "knuth morris pratt",
        "padrao": "rabin",
        "ocorrencias_esperadas": 0,
        "encontrado_esperado": False,
    },
    {
        "descricao": "padrao igual ao texto",
        "texto": "hello",
        "padrao": "hello",
        "ocorrencias_esperadas": 1,
        "encontrado_esperado": True,
    },
    {
        "descricao": "padrao maior que o texto",
        "texto": "abc",
        "padrao": "abcdef",
        "ocorrencias_esperadas": 0,
        "encontrado_esperado": False,
    },
    {
        # texto - "aaa" * 100 = 300 chars de 'a'
        # o padrao "aaa" aparece em cada posicao 0..297 - total de 298 ocorrencias sobrepostas
        "descricao": "texto longo com padrao repetido e sobreposto",
        "texto": "aaa" * 100,
        "padrao": "aaa",
        "ocorrencias_esperadas": 298,
        "encontrado_esperado": True,
    },
]

algoritmos = {
    "forca-bruta": ForcaBruta(),
    "rabin-karp": RabinKarp(),
    "kmp": KMP(),
    "boyer-moore": BoyerMoore(),
}


def rodar_testes():
    total = 0
    passou = 0
    falhou = 0

    for nome_algo, algo in algoritmos.items():
        print(f"\n--- testando {nome_algo} ---")
        for caso in casos_de_teste:
            total += 1
            resultado = algo.buscar(caso["texto"], caso["padrao"])

            # valida usando as funcoes do python 
            posicoes_corretas = []
            txt = caso["texto"]
            pat = caso["padrao"]
            pos = 0
            while True:
                idx = txt.find(pat, pos)
                if idx == -1:
                    break
                posicoes_corretas.append(idx)
                pos = idx + 1

            ok_ocorrencias = resultado["ocorrencias"] == caso["ocorrencias_esperadas"]
            ok_encontrado = resultado["encontrado"] == caso["encontrado_esperado"]
            ok_posicoes = sorted(resultado["posicoes"]) == sorted(posicoes_corretas)

            if ok_ocorrencias and ok_encontrado and ok_posicoes:
                passou += 1
                print(f"  [ok] {caso['descricao']}")
            else:
                falhou += 1
                print(f"  [falhou] {caso['descricao']}")
                if not ok_ocorrencias:
                    print(f"         ocorrencias - esperado {caso['ocorrencias_esperadas']} - got {resultado['ocorrencias']}")
                if not ok_posicoes:
                    print(f"         posicoes - esperado {sorted(posicoes_corretas)} - got {sorted(resultado['posicoes'])}")

    print(f"\n=============================")
    print(f"total - {total} | passou - {passou} | falhou - {falhou}")
    if falhou == 0:
        print("todos os testes passaram!")
    else:
        print(f"atencao - {falhou} teste(s) falharam")
    print("=============================")

    return falhou == 0


if __name__ == "__main__":
    sucesso = rodar_testes()
    sys.exit(0 if sucesso else 1)
