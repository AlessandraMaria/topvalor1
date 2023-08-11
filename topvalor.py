from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

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