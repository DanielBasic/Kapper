from flask import render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Barbeiro, Cliente, Data, Agendamentos, Horario
from calendar import HTMLCalendar
from datetime import date, datetime, timedelta, time
from calendar import Calendar
from uuid import uuid4

class ClienteController():  
    def index():
        return render_template("index.html")

    def quemsomos():
        return render_template("quemsomos.html")
  
    def opcao_cadastro():
        return render_template("opcao_cadastro.html")
  
    def cadastro_barbeiro():
      return render_template("cadastro_barbeiro.html")
      
    def cadastrar_barbeiro():
      email = request.form.get("email")
      first_name = request.form.get("first_name")
      second_name = request.form.get("second_name")
      cnpj = request.form.get("document")
      password = request.form.get("password")
      password_confirmation = request.form.get("password_confirmation")
      barbershop_name = request.form.get("barbershop_name")
      endereco = request.form.get("endereco")
      search_id = str(uuid4())

      user_e = Barbeiro.query.filter_by(email=email).first()
      user_c = Barbeiro.query.filter_by(cnpj = cnpj).first()
      
      if user_e:
        flash('E-mail ja cadastrado','error')  #Se o email ou cnpj já estiver cadastrado ele redireciona para a página de login

        #Possível mensagem de "email ou cnpj já cadastrado"
        return redirect("/")

      if user_c:
        flash('CNPJ já cadastrado','error')
        return redirect("/") 

      if password != password_confirmation:
        
        #Devemos plotar uma mensagem que as senhas não coincidem
        return redirect("/")
      
      barbeiro = Barbeiro(email = email, nome = (first_name + " " + second_name), cnpj = cnpj, senha = generate_password_hash(password, method='sha256'), barbershop_name = barbershop_name,endereco = endereco, search_id = search_id)
      
      db.session.add(barbeiro)
      db.session.commit()
      return redirect("/login")

      #Plotar uma mensagem que ele foi cadastrado com sucesso (A mensagem provavelmente vai ter que ser plotada na página de login, já que ele vai ser redirecionado depois que fizer o download)
      
      
      """
      #Lógica para validação de cnpj
      clean_cnpj = ""
      for i in cnpj:
        if i.isdigit():
          clean_cnpj += i
      if len(clean_cnpj) < 14:
        #Retornar uma mensagem de que o cnpj é inválido e redirecionar novamente para página de dacastro do barbeiro
        pass
      """

    def cadastro_cliente():
      return render_template('cadastro_cliente.html')
 
    def cadastrar_cliente():
      email = request.form.get("email")
      first_name = request.form.get("first_name")
      second_name = request.form.get("second_name")
      cpf = request.form.get("document")
      password = request.form.get("password")
      password_confirmation = request.form.get("password_confirmation")

      user_e = Cliente.query.filter_by(email=email).first()
      user_c = Cliente.query.filter_by(cpf = cpf).first()

      
      if user_e or user_c: #Se o email ou cpf já estiver cadastrado ele redireciona para a página de login

        #Possível mensagem de "email ou cpf já cadastrado"
        return redirect("/login")

      if password != password_confirmation:
        #Devemos plotar uma mensagem que as senhas não coincidem
        return redirect("/cadastro_cliente")
      
      cliente = Cliente(email = email, nome = (first_name + " " + second_name), cpf = cpf, senha = generate_password_hash(password, method='sha256'))
      
      db.session.add(cliente)
      db.session.commit()
      return redirect("/login")

    def login():
      return render_template("login.html")

    def logar():
      email = request.form.get("email")
      password = request.form.get("password") 
      user = Cliente.query.filter_by(email=email).first()
      if user and check_password_hash(user.senha, password):
        session['cliente_id'] = user.id
        return redirect('/tela_cliente/barbeiros')
      user = Barbeiro.query.filter_by(email=email).first()
      if user and check_password_hash(user.senha, password):
        session['barber_id'] = user.id
        return redirect('/tela_barbeiro/')
      else:
        return redirect("/login")

    def meus_agendamentos():
      if 'cliente_id' not in session:
        return redirect('/login')
      cliente_id = session['cliente_id']      
      datas = []
      horarios = []
      barbeiros = []
      cancelamentos = []
      size = 0

      cancelado = request.form.get("cancelado")
      concluido = request.form.get("concluido")
      datetime_now = datetime.now()
      if cancelado:
        agendamento = Agendamentos.query.filter_by(id = cancelado).first()
        date = Data.query.filter_by(id = agendamento.data_id).first()
        horario = Horario.query.filter_by(id = agendamento.horario_id).first()
        y, m, d = date.data_objt.split("-")
        h, mi = horario.horario_objt.split(":")
        datetime_chosen = datetime(int(y), int(m), int(d), int(h), int(mi))
        delta = datetime_chosen - datetime_now
        if delta.days < 0:
          return redirect("/meus_agendamentos")
          #Mostrar mensagem de que não é possível mais fazer o cancelamento
        
        
        if delta.days == 0:
          if int(str(delta).split(":")[0]) < 2:
            print("q")
            return redirect("/meus_agendamentos")
          #Mostrar mensagem de erro de que não foi possível efetuar o cancelamento
        #Mostrar mensagem que o agendamento foi cancelado com sucesso
        agendamento.cancelado = True
        db.session.commit()

      if concluido:
        agendamento = Agendamentos.query.filter_by(id = concluido).first()
        date = Data.query.filter_by(id = agendamento.data_id).first()
        horario = Horario.query.filter_by(id = agendamento.horario_id).first()
        
        y, m, d = date.data_objt.split("-")
        h, mi = horario.horario_objt.split(":")
        
        datetime_chosen = datetime(int(y), int(m), int(d), int(h), int(mi))
        delta = datetime_chosen - datetime_now
        print(delta)
        print(delta.days)

        if delta.days == 0:
          horario_escolhido = time(int(h), int(mi))
          horario_now = time(datetime_now.hour, datetime_now.minute) 
          if horario_escolhido.hour < horario_now.hour:
            return redirect("/meus_agendamentos")
            #Mostrar mensagem de erro de que não foi possível efetuar a conclusão
          elif horario_escolhido.hour - horario_now.hour == 0:
            if horario_escolhido.minute < horario_now.minute: 
              return redirect("/meus_agendamentos")
              #Mostrar mensagem de erro de que não foi possível efetuar a conclusão  
        
        if delta.days >= 0:
          return redirect("/meus_agendamentos")
          #Mostrar mensagem de erro de que não foi possível efetuar a conclusão
        
        agendamento = Agendamentos.query.filter_by(id = concluido).first()
        agendamento.concluido = True
        db.session.commit()
        #Mostrar mensagem que foi concluido com sucesso
        return redirect("/meus_agendamentos")
      agendamentos = Agendamentos.query.filter_by(cliente_id = cliente_id).all()
      
      for agendamento in agendamentos:
        date = Data.query.filter_by(id = agendamento.data_id).first()
        horario = Horario.query.filter_by(id = agendamento.horario_id).first()
        if date and horario:
          size += 1
          datetime_now = datetime.now()
          y, m, d = date.data_objt.split("-")
          h, mi = horario.horario_objt.split(":")
          datetime_chosen = datetime(int(y), int(m), int(d), int(h), int(mi))
          delta = datetime_chosen - datetime_now
          intervalo = timedelta(seconds = delta.seconds)
          horarios_escolhido = timedelta(hours = int(h), minutes = int(mi))
          if delta.days < 0:
            cancelamentos.append(False)
          
          elif delta.days == 0:
            if int(str(delta).split(":")[0]) < 2:
              cancelamentos.append(False)
          else:
            cancelamentos.append(True)
            
          data = Data.query.filter_by(id = agendamento.data_id).first()
          data = data.data_objt.split("-")
          data.reverse()
          data =  "/".join(data)
          datas.append(data)
          horarios.append(Horario.query.filter_by(id = agendamento.horario_id).first())
          barbeiros.append(Barbeiro.query.filter_by(id = agendamento.barbeiro_id).first())
        
      return render_template("meus_agendamentos.html", agendamentos = agendamentos, datas = datas, horarios = horarios, barbeiros = barbeiros, size = size, cancelamentos = cancelamentos)

class Screen():
  def tela_cliente_agendamento(search_id):
    if 'cliente_id' not in session:
      return redirect('/login')
    cliente_id = session['cliente_id']
    barbeiro = Barbeiro.query.filter_by(search_id = search_id).first()
    datas = Data.query.filter_by(barbeiro_id = barbeiro.id).all()
    datas_objt = []
    for d in datas:
      if d.qnt_a_disponiveis > 0:
        datas_objt.append(d.data_objt)
    

    mes = {'JANUARY': 'JANEIRO', 'FEBRUARY': 'FEVEREIRO', 'MARCH': 'MARÇO', 'APRIL': 'ABRIL', 'MAY': 'MAIO', 'JUNE': 'JUNHO', 'JULY': 'JULHO', 'AUGUST': 'AGOSTO', 'SEPTEMBER': 'SETEMBRO', 'OCTOBER': 'OUTUBRO', 'NOVEMBER': 'NOVEMBRO', 'DECEMBER': 'DEZEMBRO'}
    date_now = date.today()
    datetime_now = datetime.today()
    dates_of_month = []
    calendar = Calendar()
    datas_disponiveis = []
    horarios_disponiveis = []
    #Trocar por função str
    for i in calendar.itermonthdates(date_now.year, date_now.month):
      if str(i)[5:7] == date_now.strftime("%m"):
          dates_of_month.append(date(int(str(i)[:4]), int(str(i)[5:7]), int(str(i)[8:])))
    month = mes[date_now.strftime("%B").upper()]
    #
    horarios_dia = None
    horario_escolhido = request.form.get("horario_escolhido")
    data_escolhida = request.form.get("data_escolhida")
    agendamentos = Agendamentos.query.all()
    if data_escolhida:
      data = Data.query.filter_by(data_objt = data_escolhida).first()
      horarios_dia = Horario.query.filter_by(data_id = data.id, agendado = False, barbeiro_id = barbeiro.id).all()
      session['data_id'] = data.id
      if horarios_dia:
        if str(date.fromisoformat(data.data_objt) - date_now) == "0:00:00":
          flag = True
          while flag:
            for h in range(len(horarios_dia)):
              flag = False
              if horarios_dia[h].data_id == data.id:
                if int(horarios_dia[h].horario_objt.split(":")[0]) - int(datetime_now.strftime("%H:%M").split(":")[0]) < 0:
                  horarios_dia.pop(h)
                  flag = True
              if h + 1 == len(horarios_dia):
                break
              
          
    if horario_escolhido:
      data = Data.query.filter_by(id = session['data_id']).first()
      data.qnt_a_disponiveis -= 1
      horario = Horario.query.filter_by(horario_objt = horario_escolhido, data_id = session['data_id']).first()
      horario.agendado = True
      agendamento = Agendamentos(data_id = session['data_id'], horario_id = horario.id, barbeiro_id = barbeiro.id, cliente_id = cliente_id)
      db.session.add(agendamento)
      db.session.commit()
      return redirect("/meus_agendamentos")
        
    return render_template("tela_cliente_agendamento.html", month = month, dates_of_month = dates_of_month, barbeiro = barbeiro, datas = datas_objt, horarios_dia = horarios_dia, agendamentos = agendamentos, date_today = date_now)
  
  def return_tela_cliente_barbeiros():
    if 'cliente_id' not in session:
      return redirect('/login')
    cliente_id = session['cliente_id']
    
    all_barbeiros = Barbeiro.query.all()
    return render_template("tela_cliente-barbeiros.html", barbeiros = all_barbeiros)
    
  
  
  def tela_barbeiro():
    if 'barber_id' not in session:
      return redirect('/login')
    barber_id = session['barber_id']

    def convert_minutes(minutes, intv, start):
      """
      Essa função recebe dois parâmetros, sendo minutes recebendo os minutos que serão convertidos e_
      intv que será o intervalo a ser convertido;
      Start será o parâmetro usado para sabermos a partir de qual horário iremos criar os possíveis
      horários com o intervalo(intv), esse parâmetro deve ser uma string no formato: 'hh:mm'(13:45)
      Essa função retornará uma lista contendo os horários possíveis a cada intervalo;
      Minutes será usado como o intervalo existente entre o começo do horário "start" o horário final
      Exemplo:
      convert_minutes(230, 60, 13:40)
      retorno:
      3, [14:40, 15:40, 16:40]
      """
      try:
        minutes = int(minutes)
        intv = int(intv)
        start = str(start)
        qnt = minutes // intv
        lista = [start]
        hour, minute = start.split(":")
        zero_before = False
        for i in range(qnt):
          hour = str(int(hour) + ((int(intv) + int(minute)) // 60))
          if float("0." + ((str((float(intv) + float(minute))/ 60)).split(".")[1])) <= 0.1666:
            zero_before = True
          minute = str(round(float("0." + ((str((float(intv) + float(minute))/ 60)).split(".")[1])) * 60))
          if len(minute) < 2:
            if zero_before:
              minute = "0" + minute
            else:
              minute = minute + "0"
          if len(hour) < 2:
            hour = "0" + hour
          if len(minute) < 2:
            minute = "0" + minute
          lista.append(":".join([hour,minute]))
        return lista[:len(lista) - 1]
      except:
        return None

    #Obter data atual:
    mes = {'JANUARY': 'JANEIRO', 'FEBRUARY': 'FEVEREIRO', 'MARCH': 'MARÇO', 'APRIL': 'ABRIL', 'MAY': 'MAIO', 'JUNE': 'JUNHO', 'JULY': 'JULHO', 'AUGUST': 'AGOSTO', 'SEPTEMBER': 'SETEMBRO', 'OCTOBER': 'OUTUBRO', 'NOVEMBER': 'NOVEMBRO', 'DECEMBER': 'DEZEMBRO'}
    date_now = date.today()
    dates_of_month = []
    calendar = Calendar()
    date_today = date.today()
    #Trocar por função str
    for i in calendar.itermonthdates(date_now.year, date_now.month):
      if str(i)[5:7] == date_now.strftime("%m"):
          dates_of_month.append(date(int(str(i)[:4]), int(str(i)[5:7]), int(str(i)[8:])))
    month = mes[date_now.strftime("%B").upper()]
    #
    
    dias_escolhido = request.form.getlist("dia_escolhido")
    tempo_por_procedimento = request.form.get("tempo_por_procedimento")
    start_time_escolhido = request.form.get("start_time_escolhido")
    end_time_escolhido = request.form.get("end_time_escolhido")
    if start_time_escolhido != None and tempo_por_procedimento != None and end_time_escolhido != None:
      if int(start_time_escolhido[:2]) > int(end_time_escolhido[:2]):
        """
        Retornar uma mensagem de erro (Horário de abertura não pode ser após o horário de fechamento)
        """
        pass
      #Atribui a 'minutes_funcionamento' o horário de funcionamento em minutos
      else:
        minutes_funcionamento = (int(end_time_escolhido[:2]) - int(start_time_escolhido[:2])) * 60
        if int(start_time_escolhido[3:]) - int(end_time_escolhido[3:]) < 0:
          minutes_funcionamento -= int(end_time_escolhido[3:])
        else:
          minutes_funcionamento += int(end_time_escolhido[3:]) - int(start_time_escolhido[3:])
      #
      #Atribui a 'minutes_procedimento' o tempo por procedimento em minutos
        minutes_procedimento = int(tempo_por_procedimento[:2]) * 60 + int(tempo_por_procedimento[3:])
        if minutes_procedimento > minutes_funcionamento:
          """
          Retornar uma mensagem de erro (O tempo de cada procedimento é maior que o tempo de funcionamento da barbearia )
          """
          pass

        horarios_disponiveis = convert_minutes(minutes_funcionamento,minutes_procedimento, start_time_escolhido)
        
        for day in dias_escolhido:
          ja_cadastrada = Data.query.filter_by(data_objt = day).first()
          
          if ja_cadastrada:
            db.session.delete(ja_cadastrada)
            db.session.commit()
          date_ = Data(data_objt = day, qnt_a_disponiveis = len(horarios_disponiveis), barbeiro_id = barber_id)
          db.session.add(date_)
          db.session.commit()
          for hor in horarios_disponiveis:
            data_id = Data.query.filter_by(data_objt = day).first()
            horario = Horario(horario_objt = hor, data_id = data_id.id, barbeiro_id = barber_id)
            db.session.add(horario)
            db.session.commit()

    db_datas_config = Data.query.filter_by(barbeiro_id = barber_id).all()
    datas_config = []
    barber = Barbeiro.query.filter_by(id = barber_id)
    for data in db_datas_config:
      datas_config.append(data.data_objt)

    return render_template("tela_barbeiro.html", dates_of_month = dates_of_month, month = month, datas_config = datas_config, barbeiro = barber, date_today = date_today)

  def deslogar():
    if 'barber_id' in session:
      session.pop('barber_id', None)
      return redirect("/")
    elif 'cliente_id' in session:
      session.pop('cliente_id', None)
      return redirect("/")



class Returns():

  def return_tela_barbeiro():
    return redirect("/tela_barbeiro/calendar")

