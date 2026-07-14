from flask import Flask, request, jsonify, render_template, session, redirect
from sqlmodel import SQLModel, Field, Session, create_engine, select
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from datetime import date


def limpar_cnpj(cnpj):
    return cnpj.replace('.', '').replace('/', '').replace('-', '').strip()


app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.config['SECRET_KEY'] = 'pethope-secret'

DATABASE_URL = "mysql+pymysql://root:admin@localhost/pethope"

engine = create_engine(DATABASE_URL, echo=False)


# ================= MODELOS =================

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    tipo: str


class Ong(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cnpj: str
    endereco: Optional[str] = None
    contato: Optional[str] = None
    senha: str


class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    especie: str
    raca: Optional[str] = None
    idade: Optional[int] = None
    sexo: Optional[str] = None
    descricao: Optional[str] = None
    status: str = "Disponível"    
    ong_id: int = Field(foreign_key="ong.id")

class Adocao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="user.id")
    animal_id: int = Field(foreign_key="animal.id")
    data: date
    status: str

# ================= ROTAS HTML =================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
    
@app.route('/opcoes_login') 
def opcoes():
    return render_template('opcoes_login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/cadastro_ong')
def cadastro_ong_page():
    return render_template('cadastro_ong.html')


@app.route('/login_ong')
def login_ong_page():
    return render_template('login_ong.html')


@app.route('/cadastro_animal')
def cadastro_animal_page():
    if 'ong_id' not in session:
        return redirect('/login_ong')

    return render_template('cadastro_animal.html')


# ================= USUÁRIOS =================

@app.route('/api/users', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Sem dados"}), 400

    with Session(engine) as db:

        usuario_existente = db.exec(select(User).where(User.email == data['email'])).first()

        if usuario_existente:
            return jsonify(
                {"erro": "Email já existe"}
            ), 409

        user = User(
            nome=data['nome'],
            email=data['email'],
            senha=generate_password_hash(data['senha']),
            tipo=data['tipo']
        )

        db.add(user)
        db.commit()

    return jsonify(
        {"mensagem": "Usuário criado"}
    ), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    with Session(engine) as db:

        user = db.exec(select(User).where(User.email == data['email'])).first()

        if user and check_password_hash(user.senha, data['senha']):
            session['user_id'] = user.id
            session['user_nome'] = user.nome
            session['user_tipo'] = user.tipo

            return jsonify(
                {"ok": True}
            ), 200

    return jsonify(
        {"erro": "Login inválido"}
    ), 401


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    tipo = session.get('user_tipo')
    nome = session.get('user_nome')

    if tipo == 'voluntario':
        return render_template('dashboard_voluntario.html', nome=nome)

    elif tipo == 'adotante':
        return render_template('dashboard_adotante.html', nome=nome)

    return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/minhas_adocoes')
def minhas_adocoes():

    if 'user_id' not in session:
        return redirect('/login')

    with Session(engine) as db:

        adocoes = db.exec(
            select(Adocao).where(Adocao.usuario_id == session['user_id'])
        ).all()

        dados = []

        for adocao in adocoes:
            animal = db.get(Animal, adocao.animal_id)

            dados.append({
                "animal": animal,
                "status": adocao.status,
                "data": adocao.data
            })

    return render_template(
        "minhas_adocoes.html",
        adocoes=dados
    )

# ================= ONGS =================

@app.route('/api/cadastro_ong', methods=['POST'])
def cadastrar_ong():

    data = request.get_json()
    cnpj = limpar_cnpj(data['cnpj'])

    with Session(engine) as db:

        ong_existente = db.exec(select(Ong).where(Ong.cnpj == cnpj)).first()

        if ong_existente:
            return jsonify(
                {'erro': 'CNPJ já cadastrado'}
            ), 409

        nova_ong = Ong(
            nome=data['nome'],
            cnpj=cnpj,
            endereco=data.get('endereco'),
            contato=data.get('contato'),
            senha=generate_password_hash(data['senha'])
        )

        db.add(nova_ong)
        db.commit()

    return jsonify(
        {'mensagem': 'ONG cadastrada com sucesso'}
    ), 201


@app.route('/api/login_ong', methods=['POST'])
def login_ong():

    data = request.get_json()
    cnpj = limpar_cnpj(data['cnpj'])

    with Session(engine) as db:

        ong = db.exec(select(Ong).where(Ong.cnpj == cnpj)).first()

        if ong and check_password_hash(ong.senha, data['senha']):
            session['ong_id'] = ong.id
            session['ong_nome'] = ong.nome

            return jsonify(
                {'ok': True}
            ), 200

    return jsonify(
        {'erro': 'CNPJ ou senha inválidos'}
    ), 401


@app.route('/dashboard_ong')
def dashboard_ong():

    if 'ong_id' not in session:
        return redirect('/login_ong')

    return render_template('dashboard_ong.html', nome=session.get('ong_nome'))

@app.route('/solicitacoes')
def solicitacoes():

    if 'ong_id' not in session:
        return redirect('/login_ong')

    with Session(engine) as db:

        solicitacoes = db.exec(
            select(Adocao)
        ).all()

        dados = []

        for s in solicitacoes:
            animal = db.get(Animal, s.animal_id)
            usuario = db.get(User, s.usuario_id)

            if animal.ong_id == session['ong_id']:

                dados.append({
                    "id": s.id,
                    "animal": animal,
                    "usuario": usuario,
                    "status": s.status
                })

    return render_template(
        "solicitacoes.html",
        solicitacoes=dados
    )

# ================= ANIMAIS =================

@app.route('/api/cadastro_animal', methods=['POST'])
def cadastrar_animal():

    if 'ong_id' not in session:
        return jsonify(
            {'erro': 'ONG não autenticada'}
        ), 401

    data = request.get_json()

    animal = Animal(
        nome=data['nome'],
        especie=data['especie'],
        raca=data.get('raca'),
        idade=data.get('idade'),
        sexo=data.get('sexo'),
        descricao=data.get('descricao'),
        status="Disponível",
        ong_id=session['ong_id']
    )

    with Session(engine) as db:
        db.add(animal)
        db.commit()

    return jsonify(
        {'mensagem': 'Animal cadastrado com sucesso'}
    ), 201


@app.route('/animais')
def listar_animais():

    if 'ong_id' not in session:
        return redirect('/login_ong')

    with Session(engine) as db:

        animais = db.exec(select(Animal).where(Animal.ong_id == session['ong_id'])).all()

    return render_template('lista_animais.html', animais=animais)


@app.route('/animal/<int:id>')
def detalhes(id):

    with Session(engine) as db:
        animal = db.get(Animal, id)

        if not animal:
            return "Animal não encontrado", 404

    return render_template(
        'animal_detalhes.html',
        animal=animal
    )

# ================= ADOÇÃO =================
@app.route('/adocao')
def adocao():
    with Session(engine) as db:
        animais = db.exec(
            select(Animal).where(Animal.status == "Disponível")
        ).all()
    return render_template('adocao.html', animais=animais)

@app.route('/adotar/<int:id>', methods=['POST'])
def adotar(id):
    if 'user_id' not in session:
        return redirect('/login')

    with Session(engine) as db:

        animal = db.get(Animal, id)

        if not animal:
            return "Animal não encontrado", 404

        if animal.status != "Disponível":
            return "Esse animal não está disponível para adoção."

        nova_adocao = Adocao(
            usuario_id=session['user_id'],
            animal_id=animal.id,
            data=date.today(),
            status="Pendente"
        )

        animal.status = "Em processo de adoção"

        db.add(nova_adocao)
        db.add(animal)
        db.commit()

    return redirect('/adocao')

@app.route('/aprovar/<int:id>', methods=['POST'])
def aprovar(id):

    if 'ong_id' not in session:
        return redirect('/login_ong')

    with Session(engine) as db:

        adocao = db.get(Adocao, id)

        if not adocao:
            return "Solicitação não encontrada",404

        animal = db.get(Animal, adocao.animal_id)

        adocao.status = "Aprovada"
        animal.status = "Adotado"

        db.add(adocao)
        db.add(animal)

        db.commit()

    return redirect('/solicitacoes')

@app.route('/recusar/<int:id>', methods=['POST'])
def recusar(id):

    if 'ong_id' not in session:
        return redirect('/login_ong')

    with Session(engine) as db:

        adocao = db.get(Adocao, id)

        if not adocao:
            return "Solicitação não encontrada",404

        animal = db.get(Animal, adocao.animal_id)

        adocao.status = "Recusada"
        animal.status = "Disponível"

        db.add(adocao)
        db.add(animal)

        db.commit()

    return redirect('/solicitacoes')

# ================= START =================

if __name__ == '__main__':

    SQLModel.metadata.create_all(engine)

    print("Banco MySQL criado com sucesso")

    app.run(debug=True)
