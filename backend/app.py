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

# ================= INICIALIZAÇÃO =================
@app.route('/')
def home():
    return {"mensagem": "PetHope rodando 🐾"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
