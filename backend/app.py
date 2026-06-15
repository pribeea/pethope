from flask import Flask, request, jsonify, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

def limpar_cnpj(cnpj):
    return cnpj.replace('.', '').replace('/', '').replace('-', '').strip()

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

app.config['SECRET_KEY'] = 'pethope-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pethope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= MODELO =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)

class Ong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(30), unique=True, nullable=False)
    endereco = db.Column(db.String(150))
    contato = db.Column(db.String(100))
    senha = db.Column(db.String(200), nullable=False)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # cachorro, gato…
    raca = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(20))
    descricao = db.Column(db.Text)
    disponivel = db.Column(db.Boolean, default=True)

    ong_id = db.Column(db.Integer, db.ForeignKey('ong.id'), nullable=False)

# ================= ROTAS HTML =================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/cadastro_ong')
def cadastro_ong():
    return render_template('cadastro_ong.html')

@app.route('/login_ong')
def login_ong_page():
    return render_template('login_ong.html')

@app.route('/cadastro_animal')
def cadastro_animal_page():
    if 'ong_id' not in session:
        return redirect('/login_ong')
    return render_template('cadastro_animal.html')

# ================= API =================

@app.route('/api/users', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Sem dados"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"erro": "Email já existe"}), 409

    user = User(
        nome=data['nome'],
        email=data['email'],
        senha=generate_password_hash(data['senha']),
        tipo=data['tipo']
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.senha, data['senha']):
        session['user_id'] = user.id
        session['user_nome'] = user.nome
        session['user_tipo'] = user.tipo
        return jsonify({"ok": True}), 200

    return jsonify({"erro": "Login inválido"}), 401

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

    elif tipo == 'administrador':
        return render_template('dashboard_admin.html', nome=nome)

    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= ONGs =================

@app.route('/api/cadastro_ong', methods=['POST'])
def cadastrar_ong():
    data = request.get_json()
    cnpj = limpar_cnpj(data['cnpj'])

    if Ong.query.filter_by(cnpj=cnpj).first():
        return jsonify({'erro': 'CNPJ já cadastrado'}), 409

    nova_ong = Ong(
        nome=data['nome'],
        cnpj=cnpj,
        endereco=data.get('endereco'),
        contato=data.get('contato'),
        senha=generate_password_hash(data['senha'])
    )

    db.session.add(nova_ong)
    db.session.commit()

    return jsonify({'mensagem': 'ONG cadastrada com sucesso'}), 201
    
@app.route('/api/login_ong', methods=['POST'])
def login_ong():
    data = request.get_json()
    cnpj = limpar_cnpj(data['cnpj'])
    ong = Ong.query.filter_by(cnpj=cnpj).first()

    if ong and check_password_hash(ong.senha, data['senha']):
        session['ong_id'] = ong.id
        session['ong_nome'] = ong.nome
        return jsonify({'ok': True}), 200

    return jsonify({'erro': 'CNPJ ou senha inválidos'}), 401

@app.route('/dashboard_ong')
def dashboard_ong():
    if 'ong_id' not in session:
        return redirect('/login_ong')

    return render_template(
        'dashboard_ong.html',
        nome=session.get('ong_nome')
    )

# ================= Animais =================

@app.route('/api/cadastro_animal', methods=['POST'])
def cadastrar_animal():
    if 'ong_id' not in session:
        return jsonify({'erro': 'ONG não autenticada'}), 401

    data = request.get_json()

    animal = Animal(
        nome=data['nome'],
        especie=data['especie'],
        raca=data.get('raca'),
        idade=data.get('idade'),
        sexo=data.get('sexo'),
        descricao=data.get('descricao'),
        ong_id=session['ong_id']
    )

    db.session.add(animal)
    db.session.commit()

    return jsonify({'mensagem': 'Animal cadastrado com sucesso'}), 201

@app.route('/animais')
def listar_animais():
    if 'ong_id' not in session:
        return redirect('/login_ong')

    animais = Animal.query.filter_by(ong_id=session['ong_id']).all()

    return render_template('lista_animais.html', animais=animais)
    
# ================= START =================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco criado com sucesso")

    app.run(debug=True)
