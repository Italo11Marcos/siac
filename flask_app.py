from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file
from werkzeug.utils import secure_filename
import shutil, os, zipfile

from util import unzip, contagem, graficos, zipfile, apagaarquivos

UPLOAD_FOLDER = 'files'

#render template: passando o nome do modelo e a variáveis ele vai renderizar o template
#request: faz as requisições da nosa aplicação
#redirect: redireciona pra outras páginas
#session: armazena informações do usuário
#flash:mensagem de alerta exibida na tela
#url_for: vai para aonde o redirect indica

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'flask'
#chave secreta da sessão

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    linkdownload = False #Recebe falso. Se o arquivo for enviado e for executado corretamente, recebe o valor True no final

    countTotal = dict()

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        
        unzip.unzip() #descompacta o arquivo ZIP

        contagem.contagem() #faz a contagem dos atributos que são analisados

        countTotal = graficos.graficos() #gera os gráficos de comparação dos currículos

        zipfile.zip() #compacta os arquivos gerados para serem liberados para download

        apagaarquivos.apaga() #apaga os arquivos da pasta raiz

        linkdownload = True #recebe True para liberar o arquivo para donwload

    return render_template('index.html', linkdownload = linkdownload, countTotal = countTotal)


@app.route('/download')
def downloadFile():
    path = "C:\\Users\\italo.siqueira\\Documents\\FlaskProjects\\siac\\bk_imgs.zip"
    return send_file(path, as_attachment=True)


app.run(debug=True)