# -*- coding:utf-8 -*-
"""
Procedimentos de contagem de elementos em contextos por período
com rotulação tomando por base o ano final do período.
"""

import lxml
import os
import pandas as pd
from util import rotulador

__author__ = 'Luis Guisso'


def contar(id_lattes, contextos, ano_inicio, ano_fim, fatores_impacto=None,
           caminho='filesextracted', rotular=True):
    """
    Montagem de consulta adequada a um contexto dinâmico:
    contexto = [['caminho1', 'ANO'],
                ['caminho2', 'ANO-DO-ARTIGO'],
                ['caminho3', 'ANO-INICIO', 'ANO-FIM'],
                ...]

    :param id_lattes: Número identificador do pesquisador.
    :param contextos: Contextos as serem contados.
    :param ano_inicio: Ano de início da contagem.
    :param ano_fim: Ano de fim da contagem.
    :param caminho: Local onde encontram-se o currículo do pesquisador.
    :param rotular: Define rótulo de PQ potencial com o ano_fim como referência.
    :return: Lista com contagem dos contextos e, se solicitado, rótulo.
    """

    arquivo = caminho + os.path.sep + id_lattes + '.xml'
    arvore = lxml.etree.parse(arquivo)
    raiz = arvore.getroot()

    if not fatores_impacto:
        fatores_impacto = pd.read_csv('impactfactor.csv', encoding='ISO-8859-1')

    # consultas = list()
    # for consulta in contextos:
    #     if len(consulta) == 3:
    #         sentenca = 'count(::caminho::[@::ano_fim:: >= $ano_inicio][@::ano_inicio:: <= $ano_fim])' \
    #             .replace('::caminho::', consulta[0]) \
    #             .replace('::ano_inicio::', consulta[1]) \
    #             .replace('::ano_fim::', consulta[2])
    #     else:
    #         sentenca = 'count(::caminho::[@::ano:: >= $ano_inicio][@::ano:: <= $ano_fim])' \
    #             .replace('::caminho::', consulta[0]) \
    #             .replace('::ano::', consulta[1])
    #     consultas.append(etree.XPath(sentenca))

    sentencas = list()
    for consulta in contextos:
        if len(consulta) == 3:
            sentenca = 'count(::caminho::[@::ano_fim:: >= $ano_inicio][@::ano_inicio:: <= $ano_fim])' \
                .replace('::caminho::', consulta[0]) \
                .replace('::ano_inicio::', consulta[1]) \
                .replace('::ano_fim::', consulta[2])
        else:
            if not consulta[0].startswith('ESPECIAL'):
                sentenca = 'count(::caminho::[@::ano:: >= $ano_inicio][@::ano:: <= $ano_fim])' \
                    .replace('::caminho::', consulta[0]) \
                    .replace('::ano::', consulta[1])
            else:
                sentenca = consulta[0]
        sentencas.append(lxml.etree.XPath(sentenca))

    consulta_especial = lxml.etree.XPath(
        'PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@ANO-DO-ARTIGO >= $ano_inicio][@ANO-DO-ARTIGO <= $ano_fim]/../DETALHAMENTO-DO-ARTIGO')

    contagem = list()
    for consulta in sentencas:
        # print(consulta)
        cont = 0
        if consulta.path.startswith('ESPECIAL'):
            tipo = consulta.path
            artigos_publicados = consulta_especial(raiz, ano_inicio=ano_inicio, ano_fim=ano_fim)

            for artigo in artigos_publicados:
                issn = artigo.get('ISSN')
                periodico = fatores_impacto[fatores_impacto['ISSN'] == issn]

                # impacto = 0
                if not periodico.empty:
                    # 3 é o índice para 2013/2014/2015
                    impacto = float(periodico[periodico.columns[3]])

                    # --------------------------------------------------------
                    # IMPORTANTE!!
                    # A indentação deste bloco resulta no cômputo de apenas os
                    # periódicos avaliados
                    # --------------------------------------------------------

                    # Caso especial: IF < 1.0
                    if tipo == 'ESPECIAL-ARTIGO-FATOR-IMPACTO-0' and impacto < 1.0:
                        cont += 1

                    # Caso especial: 1.0 =< IF < 1.2
                    elif tipo == 'ESPECIAL-ARTIGO-FATOR-IMPACTO-1-0' and 1.0 <= impacto < 1.2:
                        cont += 1

                    # Caso especial: 1.2 =< IF < 1.5
                    elif tipo == 'ESPECIAL-ARTIGO-FATOR-IMPACTO-1-2' and 1.2 <= impacto < 1.5:
                        cont += 1

                    # Caso especial: IF >= 1.5
                    elif tipo == 'ESPECIAL-ARTIGO-FATOR-IMPACTO-1-5' and impacto >= 1.5:
                        cont += 1

                    # --------------------------------------------------------
                    # Fim do bloco de contagens de artigos segmentados
                    # --------------------------------------------------------
        else:
            cont = int(consulta(raiz, ano_inicio=ano_inicio, ano_fim=ano_fim))

        contagem.append(cont)

    if rotular:
        rotulo = rotulador.rotular(id_lattes, ano_referencia=ano_fim)
        contagem.append(rotulo)

    return contagem
