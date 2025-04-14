from flask import Flask, render_template, flash
from controllers import routes
from models.database import db
import os
import pymysql

# Criando a instância do Flask na variável app
app = Flask(__name__, template_folder='views')  # Representa o nome do arquivo
routes.init_app(app)

app.secret_key = os.urandom(24)

# Permite ler o diretório de um determinado arquivo
dir = os.path.abspath(os.path.dirname(__file__))

DB_NAME = 'galeria'
app.config['DATABASE_NAME'] = DB_NAME

# Passamos o diretório ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:@localhost/{DB_NAME}'

# Define pasta que receberá arquivos de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Define o tamanho máximo de um arquivo de upload
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



# Iniciar o servidor
if __name__ == '__main__':
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            print(f'O banco de dados está criado!')
    except Exception as e:
            print(f'Erro ao criar o banco de dados: {e}')
    finally:
        connection.close()
        
    db.init_app(app=app)
    # Verifica no inicio da aplicação se o BD já existe. Caso contrário ele  criará o BD.
    with app.test_request_context():
        db.create_all()
    app.run(host='0.0.0.0', port=4000, debug=True)