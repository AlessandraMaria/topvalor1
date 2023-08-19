from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Alessandra:alessadra@localhost:3306/bctopvalor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db= SQLAlchemy (app)

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
                    
@app.route("/")
def index():        
   return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
  return render_template('usuario.html', titulo="Cadastro de Usuario")

@app.route("/cad/caduser", methods=['POST'])
def caduser():
   return request.form

@app.route("/cad/anuncios")
def anuncios():
   return render_template('anuncios.html')

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

@app.route("/config/categoria")
def categoria():
   return render_template('categoria.html') 

@app.route("/relatorios/vendas")
def relvendas():
   return render_template('relvendas.html')

@app.route("/relatorios/compras")
def relcompras():
   return render_template('relcompras.html')

if __name__== '__main__':
    db.create_all()

    