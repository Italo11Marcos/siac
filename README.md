<h1>Sistema de Avaliação de Currículos - SIAC</h1>

<p align="center">
  <img src="https://img.shields.io/static/v1?label=python&message=3.9.0&color=3776AB&style=for-the-badge&logo=PYTHON"/>
  <img src="http://img.shields.io/static/v1?label=Flask&message=1.1.x&color=000000&style=for-the-badge&logo=Flask"/>
  <img src="http://img.shields.io/static/v1?label=STATUS&message=CONCLUIDO&color=green&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>

### :checkered_flag: Tópicos 

:pushpin: [Descrição do projeto](#descrição-do-projeto)

:pushpin: [Funcionalidades](#funcionalidades)

:pushpin: [Imagens da Aplicação](#imagens-da-aplicação)

:pushpin: [Pré-requisitos](#pré-requisitos)

:pushpin: [Como rodar a aplicação](#como-rodar-a-aplicação)

## Descrição do Projeto
<p align="justify">
  Projeto desenvolvido em um projeto no curso de Sistemas de Informação na Unimontes que tem como objetivo extrair dados
  dos currículos da plataforma Lattes.
</p>

## Funcionalidades
<p align="justify">
   :white_check_mark: Descompacta arquivo compactados
  
   :white_check_mark: Parser por toda a extrutura xml do arquivo
   
   :white_check_mark: Extrai os dados (mais de 90)
   
   :white_check_mark: Gera imagens comparando os arquivos analisados
</p>

## Imagens da Aplicação
<p align=justify>
    [Tela inicial](https://github.com/Italo11Marcos/siac/blob/master/prints/tela-principal.png)
    [Dúvidas Frequentes](https://github.com/Italo11Marcos/siac/blob/master/prints/duvidas-frequentes.png)
    [Imagens geradas](https://github.com/Italo11Marcos/siac/blob/master/prints/PARTICIPACAO-EM-CONGRESSO.png
    [Imagens geradas](https://github.com/Italo11Marcos/siac/blob/master/prints/PARTICIPACAO-EM-ENCONTRO.png)
</p>

## Pré Requisitos
    * Python 3.x
    * Flask 1.x
    * Virtualenv


## Como rodar a aplicação
    1. Clone o projeto

    git clone https://github.com/Italo11Marcos/siac.git

    2. Crie um virtualenv
    
    virtualenv venv --python=3.x.x

    3. Ative o seu virtualenv. 

    source venv/bin/activate

    4. Instale dependências

    pip3 -r install requirements.txt

    5. Execute o projeto

    python3 flask_app.py

## Considerações

Grande parte do código foi obtido por um projeto, Predilattes, desenvolvido por [Luis Guisso](https://www.linkedin.com/in/luis-guisso-8ba11527/?originalSubdomain=br)
