from shutil import make_archive
from util import moves

path = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\imgs"

#compacta todos os arquivos da pasta para ZIP
def zip():

    moves.renameArq(path)

    make_archive('bk_imgs', 'zip', path)


