from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ================= BANCO =================
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pethope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= ONG =================
class ONG(db.Model):
    __tablename__ = 'ongs'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=True)
    endereco = db.Column(db.String(150), nullable=False)
    contato = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "endereco": self.endereco,
            "contato": self.contato
        }

# ================= USUÁRIO =================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)  
    # exemplo: voluntario, adotante, administrador

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo
        }

# ================= ANIMAL =================
class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    condicao = db.Column(db.String(100))
    historico_medico = db.Column(db.String(200))

    ong_id = db.Column(db.Integer, db.ForeignKey('ongs.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "raca": self.raca,
            "idade": self.idade,
            "condicao": self.condicao,
            "historico_medico": self.historico_medico,
            "ong_id": self.ong_id
        }
# ==================================
@app.route('/api/ongs', methods=['POST'])
def cadastrar_ong():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Dados não enviados"}), 400

    if not data.get('nome') or not data.get('endereco') or not data.get('contato'):
        return jsonify({"erro": "Campos obrigatórios não informados"}), 400

    nova_ong = ONG(
        nome=data['nome'],
        cnpj=data.get('cnpj'),
        endereco=data['endereco'],
        contato=data['contato']
    )

    db.session.add(nova_ong)
    db.session.commit()

    return jsonify({
        "mensagem": "ONG cadastrada com sucesso",
        "ong": nova_ong.to_dict()
    }), 201

# ==================================
@app.route('/api/users', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Dados não enviados"}), 400

    if not data.get('nome') or not data.get('email') or not data.get('senha') or not data.get('tipo'):
        return jsonify({"erro": "Campos obrigatórios não informados"}), 400

    # Verifica se email já existe
    email_existente = User.query.filter_by(email=data['email']).first()
    if email_existente:
        return jsonify({"erro": "Email já cadastrado"}), 409

    novo_usuario = User(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],  # depois pode criptografar
        tipo=data['tipo']
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        "mensagem": "Usuário cadastrado com sucesso",
        "usuario": novo_usuario.to_dict()
    }), 201

# ==================================
@app.route('/api/animals', methods=['POST'])
def cadastrar_animal():
    data = request.get_json()

    if not data:
        return jsonify({"erro": "Dados não enviados"}), 400

    # Campos obrigatórios
    if not data.get('nome') or not data.get('especie') or not data.get('ong_id'):
        return jsonify({"erro": "Campos obrigatórios não informados"}), 400

    # Verifica se a ONG existe
    ong = ONG.query.get(data['ong_id'])
    if not ong:
        return jsonify({"erro": "ONG não encontrada"}), 404

    animal = Animal(
        nome=data['nome'],
        especie=data['especie'],
        raca=data.get('raca'),
        idade=data.get('idade'),
        condicao=data.get('condicao'),
        historico_medico=data.get('historico_medico'),
        ong_id=data['ong_id']
    )

    db.session.add(animal)
    db.session.commit()

    return jsonify({
        "mensagem": "Animal cadastrado com sucesso",
        "animal": animal.to_dict()
    }), 201

# ================= INICIALIZAÇÃO =================
@app.route('/')
def home():
    return {"mensagem": "PetHope rodando 🐾"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
