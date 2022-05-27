from database import db

class Cliente(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(500))
  email = db.Column(db.String(100), unique=True)
  senha = db.Column(db.String(100))
  cpf = db.Column(db.String(14), unique=True)

class Barbeiro(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(500))
  email = db.Column(db.String(200), unique=True)
  senha = db.Column(db.String(100))
  cnpj = db.Column(db.String(14), unique=True)
  barbershop_name = db.Column(db.String(100))
  endereco = db.Column(db.String())
  search_id = db.Column(db.String, unique=True)

class Data(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data_objt = db.Column(db.String, unique= True)
  qnt_a_disponiveis = db.Column(db.Integer())
  barbeiro_id = db.Column(db.Integer, db.ForeignKey("barbeiro.id"))
  
class Agendamentos(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data_id = db.Column(db.Integer(), db.ForeignKey("data.id"))
  horario_id = db.Column(db.Integer(), db.ForeignKey("horario.id"))
  barbeiro_id = db.Column(db.Integer(), db.ForeignKey("barbeiro.id"))
  cliente_id = db.Column(db.Integer(), db.ForeignKey("cliente.id"))
  cancelado = db.Column(db.Boolean(), default=False)
  concluido = db.Column(db.Boolean(), default=False)

  
class Horario(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  horario_objt = db.Column(db.String)
  data_id = db.Column(db.Integer(), db.ForeignKey("data.id"))
  barbeiro_id = db.Column(db.Integer(), db.ForeignKey("barbeiro.id"))
  agendado = db.Column(db.Boolean, default=False)
  