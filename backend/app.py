from flask import Flask, request, jsonify, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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

# ================= START =================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco criado com sucesso")

    app.run(debug=True)
