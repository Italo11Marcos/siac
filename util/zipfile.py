from shutil import make_archive
from util import moves

path = "C:\\Users\\italo\\Documents\\python\\flask\\siac\\siac\\imgs"

#compacta todos os arquivos da pasta para ZIP
def zip():

    moves.renameArq(path)

    make_archive('bk_imgs', 'zip', path)


