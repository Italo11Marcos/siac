import os, shutil

#função que move os arquivos de uma pasta para outra
def moveArqToImgs(src, dst):

    shutil.move(src, dst)

#função que renomeia um arquivo 
def renameArq(path):
    
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            os.rename( path+'\\'+filename, path+'\\'+'contagem_final.csv' )

