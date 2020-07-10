# -*- coding: utf-8 -*-
from pandas import read_csv
import os
from lxml import etree

__author__ = 'Luis Guisso'

def rotular(id_lattes: str, ano_referencia=None, impactfactor='impactfactor.csv',
            caminho='filesextracted',
            ano_corrente=True,
            analisar_somente_pq2=False,
            explicar=False):

    if not ano_referencia:
        # Limitado a 2015 devido à coleta de dados realizada
        ano_referencia = 2015

    # Decêncio anterior, considerando o ano de referência
    ano_inicio_decenio = ano_referencia - 9

    if explicar:
        print('Ano de referencia.. ', ano_referencia)
        print('ID Lattes.......... ', id_lattes)


    df = read_csv(impactfactor)

    arquivo = caminho + os.path.sep + id_lattes + '.xml'
    tree = etree.parse(arquivo)
    root = tree.getroot()


    # PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO/ANO-DO-ARTIGO
    # PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DETALHAMENTO-DO-ARTIGO/ISSN

    # PRODUCAO-BIBLIOGRAFICA/TEXTOS-EM-JORNAIS-OU-REVISTAS/TEXTO-EM-JORNAL-OU-REVISTA/DADOS-BASICOS-DO-TEXTO/ANO-DO-TEXTO
    # PRODUCAO-BIBLIOGRAFICA/TEXTOS-EM-JORNAIS-OU-REVISTAS/TEXTO-EM-JORNAL-OU-REVISTA/DETALHAMENTO-DO-TEXTO/ISSN

    # PRODUCAO-BIBLIOGRAFICA/DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA/OUTRA-PRODUCAO-BIBLIOGRAFICA/DADOS-BASICOS-DE-OUTRA-PRODUCAO/ANO
    # PRODUCAO-BIBLIOGRAFICA/DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA/OUTRA-PRODUCAO-BIBLIOGRAFICA/DETALHAMENTO-DE-OUTRA-PRODUCAO/ISSN-ISBN

    # PRODUCAO-BIBLIOGRAFICA/DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA/PREFACIO-POSFACIO/DADOS-BASICOS-DO-PREFACIO-POSFACIO/ANO
    # PRODUCAO-BIBLIOGRAFICA/DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA/PREFACIO-POSFACIO/DETALHAMENTO-DO-PREFACIO-POSFACIO/ISSN-ISBN

    # PRODUCAO-BIBLIOGRAFICA/DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA/TRADUCAO/DADOS-BASICOS-DA-TRADUCAO/ANO
    # PRODUCAO-BIBLIOGRAFICA/DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA/TRADUCAO/DETALHAMENTO-DA-TRADUCAO/ISSN-ISBN

    # PRODUCAO-BIBLIOGRAFICA/ARTIGOS-ACEITOS-PARA-PUBLICACAO/ARTIGO-ACEITO-PARA-PUBLICACAO/DADOS-BASICOS-DO-ARTIGO/ANO-DO-ARTIGO
    # PRODUCAO-BIBLIOGRAFICA/ARTIGOS-ACEITOS-PARA-PUBLICACAO/ARTIGO-ACEITO-PARA-PUBLICACAO/DETALHAMENTO-DO-ARTIGO/ISSN


    consulta_issn_artigos_publicados_ano = etree.XPath(
        'PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@ANO-DO-ARTIGO = $ano]/../DETALHAMENTO-DO-ARTIGO')


    # OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/ANO
    # OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/ANO
    # OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO/ANO

    orientacoes_mestrado_concluidas_periodo = etree.XPath(
        'count(OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO[@ANO >= $ano_inicio][@ANO <= $ano_fim])')
    orientacoes_doutorado_concluidas_periodo = etree.XPath(
        'count(OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO[@ANO >= $ano_inicio][@ANO <= $ano_fim])')
    orientacoes_posdoutor_concluidas_periodo = etree.XPath(
        'count(OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS/ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO/DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO[@ANO >= $ano_inicio][@ANO <= $ano_fim])')


    # DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO/ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO/DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO/ANO
    # DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO/ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO/DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO/ANO
    # DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO/ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO/DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO/ANO

    orientacoes_mestrado_andamento = etree.XPath(
        'count(DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO/ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO/DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO[@ANO >= $ano_inicio][@ANO <= $ano_fim])')
    orientacoes_doutorado_andamento = etree.XPath(
        'count(DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO/ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO/DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO[@ANO >= $ano_inicio][@ANO <= $ano_fim])')
    orientacoes_posdoutor_andamento = etree.XPath(
        'count(DADOS-COMPLEMENTARES/ORIENTACOES-EM-ANDAMENTO/ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO/DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO[@ANO >= $ano_inicio][@ANO <= $ano_fim])')

    orientacoes_mestrado_pq2 = orientacoes_mestrado_concluidas_periodo(root, ano_inicio=ano_referencia - 4,
                                                                       ano_fim=ano_referencia)
    orientacoes_mestrado_pq1 = orientacoes_mestrado_concluidas_periodo(root, ano_inicio=ano_inicio_decenio,
                                                                       ano_fim=ano_referencia)
    orientacoes_doutorado_pq1 = orientacoes_doutorado_concluidas_periodo(root, ano_inicio=ano_inicio_decenio,
                                                                         ano_fim=ano_referencia)
    orientacoes_pos_doutorado_pq1 = orientacoes_posdoutor_concluidas_periodo(root, ano_inicio=ano_inicio_decenio,
                                                                             ano_fim=ano_referencia)

    orientacoes_em_andamento = orientacoes_mestrado_andamento(root, ano_inicio=ano_inicio_decenio, ano_fim=ano_referencia) \
                               + orientacoes_doutorado_andamento(root, ano_inicio=ano_inicio_decenio, ano_fim=ano_referencia) \
                               + orientacoes_posdoutor_andamento(root, ano_inicio=ano_inicio_decenio, ano_fim=ano_referencia)

    if explicar:
        msg = '> Orientacoes concluidas'
        msg += '\n  Ultimo quinquenio/Mestrado (PQ2)............. {}'.format(orientacoes_mestrado_pq2)
        msg += '\n  Ultimo decenio/Mestrado (PQ1)................ {}'.format(orientacoes_mestrado_pq1)
        msg += '\n  Ultimo decenio/Doutorado (PQ1)............... {}'.format(orientacoes_doutorado_pq1)
        msg += '\n  Ultimo decenio/Pos-Doutorado (PQ1)........... {}'.format(orientacoes_pos_doutorado_pq1)
        msg += '\n  Alguma orientacao em andamento? (PQ2 e PQ1).. ' + ('Sim' if orientacoes_em_andamento else 'Não')
        print(msg)

    # Listagem de ISSNs localizados no XML
    # for ano in artigos_publicados_periodo:
    #     issn = ano.get('ISSN')
    #     print(issn, end='\t')
    # print()


    # Lembrando que estes são válidos para 2015 a 2017
    regras2015a2017 = dict(pulicacoes_minimas_pq2=5, fator_minimo_pq2=1.0, pq2=0,
                           pulicacoes_minimas_pq1d_r1=20, fator_minimo_pq1d_r1=1.0, pq1d_r1=0,
                           pulicacoes_minimas_pq1d_r2=5, fator_minimo_pq1d_r2=1.5, pq1d_r2=0,
                           pulicacoes_minimas_pq1abc_r1=20, fator_minimo_pq1abc_r1=1.2, pq1abc_r1=0,
                           pulicacoes_minimas_pq1abc_r2=10, fator_minimo_pq1abc_r2=1.5, pq1abc_r2=0,
                           orientacoes=[[1],  # PQ2
                                        [2, 1],  # PQ1D
                                        [3, 1, 1]]  # PQ1ABC
                           )

    # Índices das linhas de orientações
    PQ2 = 0
    PQ1D = 1
    PQ1ABC = 2

    # Índices das colunas de orientações
    MESTRE = 0  # PQ2
    DOUTOR = 1  # PQ2, PQ1D
    POSDOC = 2  # PQ2, PQ1D, PQ1ABC

    # Parâmetros de varredura

    # Data frame
    # INDEX,JOURNAL,ISSN,2013/2014,2012,2011,2010,2009,2008
    # 0    ,1      ,2   ,3        ,4   ,5   ,6   ,7   ,8

    ano_limite_superior = 2012  # após este, os dados de dois anos são truncados em um (2013/2014)
    ano_limite_inferior = 2008  # antes deste não há dados, considerando-se, portanto, 2008 como limite inferior

    faixa = ano_limite_superior - ano_limite_inferior
    # ano_inicio = ano_inicio if ano_inicio >= 2008 else 2008  # limite do data frame

    # Varredura para verificação de IFs de artigos publicados
    for ano in range(ano_referencia, ano_inicio_decenio - 1, -1):
        artigos_publicados_ano = consulta_issn_artigos_publicados_ano(root, ano=ano)

        if explicar:
            print('> Artigos publicados em', ano)
        for artigo in artigos_publicados_ano:
            issn = artigo.get('ISSN')
            journal = df[df['ISSN'] == issn]

            if explicar and journal.empty:
                    print('  ', ano, ',ISSN:', (issn or '--------'), ',IF:-.---', sep='')

            # Somente os periódicos avaliados serão computados
            if not journal.empty:
                if ano > ano_limite_superior:
                    idx_column = 3
                elif ano <= ano_limite_inferior:
                    idx_column = 8
                else:
                    idx_column = ano_limite_superior - ano + faixa

                impact = float(journal[journal.columns[idx_column]])

                if explicar:
                    print('  ', ano, ',ISSN:', issn, ',IF:{:.3f}'.format(impact), sep='')

                # PQ 2
                if ano >= ano_referencia - 4 \
                        and impact >= regras2015a2017['fator_minimo_pq2']:
                    regras2015a2017['pq2'] += 1

                # PQ 1D
                if impact >= regras2015a2017['fator_minimo_pq1d_r1']:
                    regras2015a2017['pq1d_r1'] += 1
                if impact >= regras2015a2017['fator_minimo_pq1d_r2']:
                    regras2015a2017['pq1d_r2'] += 1

                # PQ 1ABC
                if impact >= regras2015a2017['fator_minimo_pq1abc_r1']:
                    regras2015a2017['pq1abc_r1'] += 1
                if impact >= regras2015a2017['fator_minimo_pq1abc_r2']:
                    regras2015a2017['pq1abc_r2'] += 1

    if explicar:
        print('> Sumario de artigos publicados')
        print('  PQ2    = publicacoes com fator de impacto >= 1.0 (min. 5)... {}'.format(regras2015a2017['pq2']))
        print('  PQ1D   = publicacoes com fator de impacto >= 1.0 (min. 20).. {}'.format(regras2015a2017['pq1d_r1']))
        print('  PQ1D   = publicacoes com fator de impacto >= 1.5 (min. 5)... {}'.format(regras2015a2017['pq1d_r2']))
        print('  PQ1ABC = publicacoes com fator de impacto >= 1.2 (min. 20).. {}'.format(regras2015a2017['pq1abc_r1']))
        print('  PQ1ABC = publicacoes com fator de impacto >= 1.5 (min. 10).. {}'.format(regras2015a2017['pq1abc_r2']))

    # Se a verificação não é para o ano corrente, "orientações em andamento" é ignorado
    # deixando "orientações concluídas" a cargo da classificação
    if not ano_corrente:
        orientacoes_em_andamento = True

    if not analisar_somente_pq2 \
            and orientacoes_em_andamento \
            and regras2015a2017['pq1abc_r1'] >= regras2015a2017['pulicacoes_minimas_pq1abc_r1'] \
            and regras2015a2017['pq1abc_r2'] >= regras2015a2017['pulicacoes_minimas_pq1abc_r2'] \
            and (orientacoes_mestrado_pq1 >= regras2015a2017['orientacoes'][PQ1ABC][MESTRE]
                 or orientacoes_doutorado_pq1 >= regras2015a2017['orientacoes'][PQ1ABC][DOUTOR]
                 or orientacoes_pos_doutorado_pq1 >= regras2015a2017['orientacoes'][PQ1ABC][POSDOC]):
        # print(' *', id_lattes, '=', 'PQ 1ABC')

        # 'PQ_1ABC'
        # return '3'
        return 1

    elif not analisar_somente_pq2 \
            and orientacoes_em_andamento \
            and regras2015a2017['pq1d_r1'] >= regras2015a2017['pulicacoes_minimas_pq1d_r1'] \
            and regras2015a2017['pq1d_r2'] >= regras2015a2017['pulicacoes_minimas_pq1d_r2'] \
            and (orientacoes_mestrado_pq1 >= regras2015a2017['orientacoes'][PQ1D][MESTRE]
                 or orientacoes_doutorado_pq1 >= regras2015a2017['orientacoes'][PQ1D][DOUTOR]):
        # print(' *', id_lattes, '=', 'PQ 1D')

        # 'PQ_1D'
        # return '2'
        return 1

    # Condição mínima segundo RN-016/2016
    elif orientacoes_em_andamento \
            and regras2015a2017['pq2'] >= regras2015a2017['pulicacoes_minimas_pq2'] \
            and orientacoes_mestrado_pq2 >= regras2015a2017['orientacoes'][PQ2][MESTRE]:
        # print(' *', id_lattes, '=', 'PQ 2')

        # 'PQ_2'
        return 2

    else:
        # print('* Não classificado')

        # 'NC'
        return 0



        # ##################################################################################################################
        #  2.1. Requisitos mínimos para acesso ao Nível 2
        #
        # Este nível é a porta de entrada convencional para obtenção de Bolsa PQ. Para ser classificado neste nível o pesquisador deverá satisfazer os seguintes requisitos mínimos no quinquênio anterior:
        #
        # a) ter publicado pelo menos 5 (cinco) trabalhos científicos em periódicos científicos com Fator de Impacto (ISI)
        # igual ou superior a ³1];
        # b) ter concluído a orientação de pelo menos 1 (um) Mestre;
        # c) estar em atividade de pesquisa e de orientação de Mestrandos ou Doutorandos;
        # d) ter linha de pesquisa definida e apresentar projeto de pesquisa de mérito científico, conforme avaliação do CA
        # com base nos pareceres dos consultores ad hoc.
        # e) atingir classificação compatível com a cota de bolsas disponíveis nesta categoria
        #
        # ##################################################################################################################
        # 2.2. Critérios de acesso ao nível 1D:
        #
        # Para ser classificado neste nível o pesquisador deverá satisfazer os seguintes requisitos mínimos no decênio anterior:
        #
        # a) ter publicado regularmente ao longo do decênio pelo menos 20 (vinte) trabalhos em periódicos científicos com
        # Fator de Impacto (ISI) igual ou superior a 1,0, sendo que 05 dessas produções deverão ter Fator de Impacto (ISI)
        # igual ou superior a 1,5.
        # b) ter concluído a orientação de pelo menos 01 Doutor ou 02 Mestres;
        # c) estar em atividade de pesquisa e de orientação de mestrandos ou doutorandos
        # d) ter linha de pesquisa definida e apresentar projeto de pesquisa de mérito científico, conforme avaliação do CA com base nos pareceres dos consultores ad hoc.
        # e) haver disponibilidade de bolsas novas ou liberadas e suas respectivas bolsas-prêmio.
        #
        # ##################################################################################################################
        # 2.3. Critérios para progressão aos níveis 1C , 1B e 1A:
        #
        # Para ser classificado nestes níveis o pesquisador deverá satisfazer os seguintes requisitos mínimos, no decênio anterior:
        #
        # a) ter publicado regularmente pelo menos 20 (vinte) trabalhos em periódicos científicos com Fator de Impacto (ISI)
        # igual ou superior a 1,2, sendo que 10 dessas produções deverão ter Fator de Impacto (ISI) igual ou superior a 1,5;
        # b) ter concluído a orientação de pelo menos 01 Doutor ou 03 mestres ou 1 pós-doutor;
        # c) estar em atividade de pesquisa e de orientação de Doutorandos e/ou mestres e/ou Pós-Doutor;
        # d) ter linha de pesquisa definida e apresentar projeto de pesquisa de mérito científico, conforme avaliação do CA
        # com base nos pareceres dos consultores ad hoc.
        # e) atingir classificação compatível com a cota de bolsas disponíveis nesta categoria
