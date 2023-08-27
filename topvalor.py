from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alessandra1:LEle!2023@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

app.secret_key = 'pazebemeamor94'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario (db.Model):
   _tablename_ = "usuario"
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

   
   def is_authenticated(self):
      return True

   def is_active(self):
      return True

   def is_anonymous(self):
      return False

   def get_id(self):
      return str(self.id)   

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Double)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, desc, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__ (self, nome, desc):
        self.nome = nome
        self.desc = desc

@app.errorhandler(404)
def paginanaoencontrada(error):
   return render_template('paginanaoencontrada.html')

@login_manager.user_loader
def load_user(id):
   return Usuario.query.get(id)

@app.route("/login", methods=['GET','POST'])
def login():
   if request.method == 'POST':
      email = request.form.get('email')
      passwd = request.form.get('passwd')

      user = Usuario.query.filter_by(email=email, senha=passwd).first()

      if user:
         login_user(user)
         return redirect(url_for('index'))
      else:
         return redirect(url_for('login'))
   return render_template('login.html')  

@app.route("/logout") 
def logout():
    logout_user()
    return redirect(url_for('index'))


# tipo de definição de rota                   
@app.route("/")
def index():        
   return render_template('index.html')

@app.route("/cad/usuario")
@login_required
def usuario():
  return render_template('usuario.html', usuarios= Usuario.query.all(),  titulo="Usuario")


@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
   usuario = Usuario(request.form.get('user'),request.form.get('email'), request.form.get('passwd'), request.form.get('end'))
   db.session.add(usuario)
   db.session.commit()  
   return redirect (url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
   usuario = Usuario.query.get(id)
   return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
   usuario = Usuario.query.get(id)
   if request.method == 'POST':
      usuario.nome = request.form.get('user')
      usuario.email = request.form.get('email')
      usuario.senha = hashlib.sha512(str(request.form.get('passwd')).encode("utf-8")).hexdigest()  
      usuario.end = request.form.get('end')
      db.session.add(usuario)
      db.session.commit()
      return redirect(url_for('usuario')) 
    
   return render_template('edicaousuario.html', usuario=usuario,  titulo="Usuario")


@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
   usuario = Usuario.query.get(id)
   db.session.delete(usuario)
   db.session.commit()
   return redirect(url_for('usuario'))


# na função get pega apenas os dados do usuario (pego o dado)
# metodo post submeter alguma informação para o nosso servidor (mando o dado)

@app.route("/anuncio/criar", methods = ['POST'])
def criaranuncio():
   anuncio = Anuncio(request.form.get('nome'),request.form.get('desc'), request.form.get('qtd'), request.form.get('preco'),request.form.get('cat'),request.form.get('uso'))
   db.session.add(anuncio)
   db.session.commit()  
   return redirect (url_for('anuncio'))

@app.route("/cad/anuncio")
def anuncio():
  return render_template('anuncio.html', anuncios = Anuncio.query.all(),  categorias = Categoria.query.all(), titulo="Anuncio")


@app.route("/anuncios/pergunta")
def perguntas():
   return render_template('pergunta.html')

@app.route ("/anuncios/compra")
def compras():
   print("anuncio comprado")
   return ""

@app.route("/anuncios/favoritos")
def favoritos():
   print("favorito inserido")
   return ""

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))


@app.route("/relatorios/vendas")
def relvendas():
   return render_template('relvendas.html')

@app.route("/relatorios/compras")
def relcompras():
   return render_template('relcompras.html')

if __name__== 'mydb':
    print("mydb")
    db.create_all()

    