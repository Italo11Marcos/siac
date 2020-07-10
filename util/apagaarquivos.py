import os

#Apaga os arquivos de cada pasta informada.
#Nesse meu caso, já que a base do caminho é igual, poderia deixar somente com uma variável e depois passar somente a pasta

def apaga():

    path1 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\files"
    path2 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\filesextracted"
    path3 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\imgs"
    path4 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac"

    for filename in os.listdir(path1):
        if filename.endswith('.zip'):
            os.unlink(path1+'\\'+filename)

    for filename in os.listdir(path2):
        if filename.endswith('.xml'):
            os.unlink(path2+'\\'+filename)

    for filename in os.listdir(path3):
        if filename.endswith('.png') or filename.endswith('.csv'):
            os.unlink(path3+'\\'+filename)

    for filename in os.listdir(path4):
        if filename.endswith('.zip'):
            if filename != 'bk_imgs.zip':
                os.unlink(path4+'\\'+filename)