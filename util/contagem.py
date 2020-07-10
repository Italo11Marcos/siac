# -*- coding: utf-8 -*-
"""
Geração de contagem de contextos do último decênio, considerando-se
um período de deslocamento a partir do ano de doutoramento.
"""

from datetime import datetime
import os
from os import walk
import pandas as pd
from util import alerta
from util import contador
from util import rotulador
from lxml import etree

__author__ = 'Luis Guisso'

def contagem():

    pqs2_2015 = list()

    path = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\filesextracted"

    for xml in os.listdir(path):
        x = xml.split('.')
        pqs2_2015.append(x[0])


    inicio_execucao = datetime.now()

    diretorio = 'filesextracted'


    # Lista especifica de currículos a serem processados
    arquivos = especificos = pqs2_2015  # + pqs1_2015


    print('Arquivos selecionados:', len(arquivos))

    
    arquivo_contextos = 'results\\contextos_contagem.csv'

    #
    # Configuração de período de rotulação
    #

    # Se verdadeiro, considera o ano de doutoramento como ano de referência
    ano_doutoramento_referencia = False

    # Ano considerado para rotulação
    ano_referencia = 2015

    # Ano anterior ao ano de referência o qual é considerado como término da contagem
    deslocamento = 5

    # Controla a contagem por segmentação de artigos por IF do periódico
    segmentacao = True

    # Considerado APENAS quando o ano de doutoramento é a referência,
    # indica em quantos anos deve ocorrer a projeção
    projecao = 0

    # arquivo_contagens = 'results/contagem_especificos_pqs_2_2012_teste_' + str(ano_referencia) + '_A+' + str(deslocamento) + '.csv'
    # arquivo_contagens = 'results/contagem_sem_pqs_2014_' + str(ano_referencia) + '_A+' + str(deslocamento) + '.csv'
    # arquivo_contagens = 'results/contagem_primeira_bolsa_pq2_' + str(ano_referencia) + '_A+' + str(deslocamento) + '.csv'
    # arquivo_contagens = 'results/contagem_primeira_bolsa_pq2.csv'
    # arquivo_contagens = 'results/contagem_doutoramento_d+' + str(deslocamento) \
    #                     + '_p' + str(projecao) \
    #                     + '.csv'

    # arquivo_contagens = 'results/contagem_final_todospqs_sem_seg_' \
    #                     + str(ano_referencia - deslocamento) \
    #                     + '_p' + str(deslocamento) + '.csv'

    # arquivo_contagens = 'results/contagem_final_apenas_pqs1_e_2_' \
    
    arquivo_contagens = 'results/contagem_final_apenas_pqs_2_' \
                       + str(ano_referencia - deslocamento) \
                        + '_p' + str(deslocamento) + '.csv'
    
    #arquivos_contagens = 'results/contagem_final.csv'

    print(arquivo_contagens)

    fatores_impacto = pd.read_csv('impactfactor.csv', encoding='ISO-8859-1')

    with open(arquivo_contextos, 'r') as contextos, open(arquivo_contagens, 'w') as contagens:
        cabecalho = 'ANO-DOUTORADO,NUMERO-IDENTIFICADOR'
        contextos_contagem = list()
        for contexto in contextos:
            # Constrói cabeçalho para arquivo CSV
            tmp = contexto.split(',')[0].split('/')[-1]
            if tmp.startswith('DADOS-BASICOS-'):
                # Utiliza ancestral da tag 'dados-basicos' como título do atributo
                cabecalho += ',' + contexto.split(',')[0].split('/')[-2]
            elif segmentacao and tmp.startswith('ESPECIAL-'):
                cabecalho += ',' + tmp[9:]
            elif not segmentacao and tmp.startswith('ESPECIAL-'):
                # Insere um cabeçalho para contagem única
                if tmp == 'ESPECIAL-ARTIGO-FATOR-IMPACTO-0':
                    cabecalho += ',ARTIGOS-PUBLICADOS'
                    contexto = 'PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS/ARTIGO-PUBLICADO/DADOS-BASICOS-DO-ARTIGO[@ANO-DO-ARTIGO >= $ano_inicio],ANO-DO-ARTIGO'
                else:
                    continue
            else:
                cabecalho += ',' + tmp

            # Inclui contexto para pesquisa
            contextos_contagem.append(contexto.replace('\n', '').split(','))

        cabecalho += ',CLASSE'
        contagens.write(cabecalho + '\n')

        # Pesquisa por todos os arquivos XML e...
        for arquivo in arquivos:
            # for arquivo, ano_referencia in zip(especificos, ano_bolsa_pq2):
            id_lattes = str(arquivo.split('.')[0])

            print('Processando', id_lattes, '...')

            arvore = etree.parse(diretorio + os.path.sep + id_lattes + '.xml')
            raiz = arvore.getroot()
            ano_doutoramento = int(raiz.find('DADOS-GERAIS/FORMACAO-ACADEMICA-TITULACAO/DOUTORADO').get('ANO-DE-CONCLUSAO'))

            # Configura períodos de contagem e rotulação
            if ano_doutoramento_referencia:
                ano_fim = ano_doutoramento + deslocamento
            else:
                ano_fim = ano_referencia - deslocamento

            ano_inicio = ano_fim - 9

            # ... gera a respectiva contagem de elementos para o decênio anterior ao ano de fim da análise
            contagem = contador.contar(id_lattes, contextos_contagem,
                                    ano_inicio=ano_inicio,
                                    ano_fim=ano_fim
                                    # Caso rotular seja falso, pode-se fazer a rotulação com a data
                                    # que se julgar mais apropriada, incluindo a projeçao para
                                    # o ano seguinte.
                                    , rotular=False
                                    )

            # Aplica a rotulação apropriada ao cenário
            if ano_doutoramento_referencia:
                # Estipula que o currículo em analise não deve ter "orientações em andamento"
                # em consideração, exceto para os doutores do ano corrente
                contagem.append(rotulador.rotular(id_lattes, ano_fim + projecao,
                                                ano_corrente=(ano_doutoramento == 2015)))
            else:
                # contagem.append(rotulador.rotular(id_lattes, ano_referencia, ano_corrente=False))

                if id_lattes in especificos:
                    # Rotulação específica
                    contagem.append(1)
                else:
                    contagem.append(rotulador.rotular(id_lattes, ano_referencia, ano_corrente=False))

            contagens.write(str(ano_doutoramento) + ',' + id_lattes + ',' + ','.join(map(str, contagem)) + '\n')

    fim_execucao = datetime.now()

    print('Processado em', (fim_execucao - inicio_execucao))
    alerta.alerta()
