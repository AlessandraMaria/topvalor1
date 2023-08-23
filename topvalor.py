from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alessandra1:LEle!2023@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Usuario (db.Model):
   id= db.Column('usu_id', db.Integer, primary_key=True)
   nome= db.Column('usu_nome', db.String(250))
   email= db.Column('usu_email', db.String(250))
   senha= db.Column('usu_senha', db.String(250))
   end= db.Column ('usu_end', db.String(250))

   def __init__(self,nome,email,senha,end):
      self.nome = nome
      self.email = email
      self.senha = senha
      self.end = end 

class Anuncio (db.Model):
   id= db.Column('anu_id', db.Integer, primary_key=True)
   nome= db.Column('anu_nome', db.String(250))
   prod= db.Column('anu_prod', db.String(250))
   qtd= db.Column('anu_qtd', db.String(250))
   preco= db.Column ('anu_preco', db.Double)

   def __init__(self,idanu,nome,prod,qtd,preco):
      self.id = idanu
      self.nome = nome
      self.prod = prod
      self.qtd = qtd
      self.preco = preco

class Categoria (db.Model):
   id= db.Column('cat_id', db.Integer, primary_key=True)
   prod= db.Column('cat_prod', db.String(250))
   
   def __init__(self,idcat,prod):
      self.id = idcat
      self.prod = prod


# tipo de definição de rota                   
@app.route("/")
def index():        
   return render_template('index.html')

@app.route("/cad/usuario")
def cadusuario():
  return render_template('usuario.html', usuarios= Usuario.query.all(),  titulo="Usuario")


@app.route("/usuario/novo", methods=['POST'])
def novousuario():
   usuario = Usuario(request.form.get('user'),request.form.get('email'), request.form.get('passwd'), request.form.get('end'))
   db.session.add(usuario)
   db.session.commit()  
   return redirect (url_for('cadusuario'))

# na função get pega apenas os dados do usuario (pego o dado)
# metodo post submeter alguma informação para o nosso servidor (mando o dado)

@app.route("/anuncio/novo", methods = ['POST'])
def novoanuncio():
   anuncio = Anuncio(request.form.get('nome'),request.form.get('desc'), request.form.get('qtd'), request.form.get('preco'))
   db.session.add(anuncio)
   db.session.commit()  
   return redirect (url_for('anuncio'))

@app.route("/cad/anuncio")
def anuncio():
  return render_template('anuncio.html', anuncios= Anuncio.query.all(),  categorias = Categoria)


@app.route("/anuncios/pergunta")
def perguntas():
   return render_template('pergunta.html')

@app.route ("/anuncios/compras")
def compras():
   print("anuncio comprado")
   return ""

@app.route("/anuncios/favoritos")
def favoritos():
   print("favorito inserido")
   return ""


@app.route("/categoria/novo", methods =['POST'])
def novacategoria():
   categoria = Categoria (request.form.get('nome'), request.form.get('desc'))
   db.session.add(categoria)
   db.session.commit()
   return redirect(url_for('categoria')) 

@app.route("/config/categoria")
def categoria():
  return render_template('categoria.html', categorias = Categoria.query.all(),  titulo = 'Categoria')


@app.route("/relatorios/vendas")
def relvendas():
   return render_template('relvendas.html')

@app.route("/relatorios/compras")
def relcompras():
   return render_template('relcompras.html')

if __name__== 'mydb':
    print("mydb")
    db.create_all()

    