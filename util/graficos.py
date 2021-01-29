import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import shutil
from util import moves, contagemTotal

def graficos():

    df1 = pd.read_csv('results/contagem_final_apenas_pqs_2_2010_p5.csv')

    #path recebe o caminho da pasta em que os gráficos serão salvos  
    path = "C:\\Users\\italo\\Documents\\python\\flask\\siac\\siac\\imgs"

    nomescampos = list()
    i = 0

    #Essa leitura serve para poder pegar os nomes das colunas
    with open('results/contagem_final_apenas_pqs_2_2010_p5.csv') as csvfile:
        content = csv.reader(csvfile)
        for row in content:
            i += 1
            if i == 1:
                nomescampos = row
            else:
                break        

    del(nomescampos[0]) #Deleta a coluna ANO-DOUTORADO
    del(nomescampos[0]) #Deleta a coluna NUMERO-IDENTIFICADOR

    #Para não passar os nomes dos currículos na mão
    curriculos = list()
    for ind in df1.index:
        curriculos.append(df1['NUMERO-IDENTIFICADOR'][ind])


    group1 = list()
    j = 0
    for i in nomescampos:
        for ind in df1.index:
            group1.append(df1[i][ind])
        print(group1)
        ax = plt.subplots()
        ax = sns.barplot(x=curriculos, y=group1)
        ax.set_title(i)
        ax.set_xlabel('curriculos')
        ax.set_ylabel('quantidade')
        group1.clear() #Limpa a lista para ela não c
        if j == len(nomescampos):
            break
        j += 1
        #plt.show()
        #print('Gerando a imagem...')
        plt.savefig('{}.png'.format(i)) #Salva a imagem
        print('Movendo a imagem..')
        shutil.move('{}.png'.format(i), path)
        print('Salvando imagem -> {}.png'.format(i))

    countTotal = contagemTotal.contatemTotal('results/contagem_final_apenas_pqs_2_2010_p5.csv')

    moves.moveArqToImgs('results/contagem_final_apenas_pqs_2_2010_p5.csv',path)
    
    print('Done')
    return countTotal

#graficos()