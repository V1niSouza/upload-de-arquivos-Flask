from flask import render_template, request, redirect, url_for, flash
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json
# Importando o Model
from models.database import db, Imagem
#
import os
import uuid


gatos = []
gatolist = []


def init_app(app):
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Define tipos de arquivos permitidos
    FILE_TYPES = set (['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in FILE_TYPES
    
    #UPLOAD DE IMAGENS
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        # Selecione os nomes dos arquivos de imagens no banco
        imagens = Imagem.query.all()
        if request.method == 'POST':
            file = request.files['file']
            # Verifica se a extensão do arquivo é permitido
            if not arquivos_permitidos(file.filename):
                flash("Utilize os tipos de arquivos referente a imagem.", 'danger')
                return redirect(request.url)
            # Define um nome aleatório para o arquivo
            filename = str(uuid.uuid4())
            # Gravando o nome do arquivo o banco
            img = Imagem(filename)
            db.session.add(img)
            db.session.commit()
            # Salva o arquivo na pasta de uploads
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Imagem enviada com sucesso!", 'success')
        return render_template('galeria.html', imagens=imagens)