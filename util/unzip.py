import shutil, os, zipfile

def unzip():
    
    path1 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\files"
    path2 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac"
    path3 = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\filesextracted"

    #descompacta a primeira vez
    for filename in os.listdir(path1):
        if filename.endswith('.zip'):
            arq = filename
            firstarq = arq
            fileExtract = zipfile.ZipFile(path1+'\\'+arq)
            fileExtract.extractall()

    #descompacta a segunda vez e renomeia o arquivo com o nome da pasta
    for filename in os.listdir(path2):
        if filename.endswith('.zip'):
            arq = filename.split('.')[0]
            print(arq)
            fileExtract = zipfile.ZipFile(path2+'\\'+filename)
            fileExtract.extractall()
            try:
                os.rename(path2+'\\'+'curriculo.xml',path2+'\\'+arq+'.xml')
            except: #esse except é só para resolver um problema específico. Mais info abaixo.
                print('relaxa, ta dando certo')
        #envia os arquivos .xml para outra pasta        
        for filexml in os.listdir(path2):
            if filexml.endswith('.xml'):
                shutil.move(filexml,path3)

#Sobre o except, é para não tentar salvar outro arquivo com o nome errado
