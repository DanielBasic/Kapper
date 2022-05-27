import os
from flask import Flask
from database import db
from controllers import ClienteController, Screen, Returns

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "6F.w\oieh]k0F[-'`7F.w\oieh]k0F[-'`7"

db.init_app(app)


@app.route("/")
def Index():
  return ClienteController.index()

@app.route("/login")
def Login():
  return ClienteController.login()

@app.route("/logar", methods=["POST"])
def Logar():
  return ClienteController.logar()

@app.route("/cadastro_barbeiro")
def Cadastro_barbeiro():
  return ClienteController.cadastro_barbeiro()

@app.route("/cadastrar_barbeiro", methods=["POST"])
def Cadastrar_barbeiro():
  return ClienteController.cadastrar_barbeiro()

@app.route("/cadastro_cliente")
def Cadastro_cliente():
  return ClienteController.cadastro_cliente()

@app.route("/cadastrar_cliente", methods=["POST"])
def Cadastrar_cliente():
  return ClienteController.cadastrar_cliente()

@app.route("/opcao_cadastro")
def Opcao_cadastro():
  return ClienteController.opcao_cadastro()

@app.route("/tela_cliente/agendamento/<string:search_id>", methods=["POST", "GET"])
def Tela_cliente_agendamento(search_id):
  return Screen.tela_cliente_agendamento(search_id)

@app.route("/tela_cliente/barbeiros")
def Tela_cliente_barbeiros():
  return Screen.return_tela_cliente_barbeiros()

@app.route("/meus_agendamentos", methods=["POST", "GET"])
def Meus_agendamentos():
  return ClienteController.meus_agendamentos()


@app.route("/tela_barbeiro/", methods=["POST", "GET"])
def Tela_barbeiro():
  return Screen.tela_barbeiro()

@app.route("/deslogar")
def Deslogar():
  return Screen.deslogar()

@app.route("/quemsomos")
def Quemsomos():
  return ClienteController.quemsomos()

"""@app.route("/agendamento")
def Agendamento():
  return ScreenController.agendamento()"""

with app.app_context():
  db.create_all()

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host="0.0.0.0", port = port)