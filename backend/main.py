"""
Backend FastAPI do PetHope.

Expõe uma API REST em JSON, consumida pelo frontend em Vue.js (frontend/).
Reaproveita a mesma modelagem de dados e regras de negócio que existiam no
protótipo original em Flask (mesmas tabelas, mesmas validações, mesmo
fluxo de cadastro/login/adoção), agora reescritas em FastAPI.

Como rodar (veja também README.md na raiz do projeto):
    pip install -r backend/requirements.txt
    uvicorn backend.main:app --reload --port 8000
"""
import logging
from datetime import date
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select
from starlette.middleware.sessions import SessionMiddleware
from werkzeug.security import check_password_hash, generate_password_hash

from .database import engine, get_session
from .models import Adocao, Animal, FormularioAdocao, Ong, User
from .schemas import (
    AdocaoRead,
    AdocaoSolicitar,
    AnimalCreate,
    AnimalRead,
    AnimalUpdate,
    LoginOng,
    LoginUsuario,
    MeResponse,
    OngCreate,
    OngRead,
    SolicitacaoRead,
    UserCreate,
    UserRead,
)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def limpar_cnpj(cnpj: str) -> str:
    return cnpj.replace(".", "").replace("/", "").replace("-", "").strip()


app = FastAPI(
    title="PetHope API",
    description="API REST do PetHope, consumida pelo frontend Vue.js",
    version="1.0.0",
)

# Sessão baseada em cookie (equivalente à session do Flask), mas com nome
# de cookie e chave secreta próprios para não colidir com o cookie de
# sessão usado pelo backend Flask.
app.add_middleware(
    SessionMiddleware,
    secret_key="pethope-fastapi-secret",
    session_cookie="pethope_fastapi_session",
    same_site="lax",
)

# CORS liberado para os servidores de desenvolvimento do Vite (Vue).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Idempotente: cria as tabelas caso ainda não existam (por exemplo, em
    # um banco novo). Se o Flask já criou as tabelas, não há efeito algum.
    SQLModel.metadata.create_all(engine)
    logger.info("Aplicação iniciada e tabelas verificadas")


# ================= HELPERS DE SESSÃO =================

def usuario_logado(request: Request) -> Optional[dict]:
    if "user_id" in request.session:
        return {
            "id": request.session["user_id"],
            "nome": request.session.get("user_nome"),
            "tipo": request.session.get("user_tipo"),
        }
    return None


def ong_logada(request: Request) -> Optional[dict]:
    if "ong_id" in request.session:
        return {
            "id": request.session["ong_id"],
            "nome": request.session.get("ong_nome"),
        }
    return None


def exigir_usuario(request: Request) -> dict:
    usuario = usuario_logado(request)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    return usuario


def exigir_ong(request: Request) -> dict:
    ong = ong_logada(request)
    if not ong:
        raise HTTPException(status_code=401, detail="ONG não autenticada")
    return ong


# ================= USUÁRIOS =================

@app.post("/api/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UserCreate, db: Session = Depends(get_session)):
    logger.info(f"Tentativa de cadastro de usuário: {dados.email}")
    
    existente = db.exec(select(User).where(User.email == dados.email)).first()
    if existente:
        logger.warning(f"Tentativa de cadastro com email já existente: {dados.email}")
        raise HTTPException(status_code=409, detail="Email já existe")

    user = User(
        nome=dados.nome,
        email=dados.email,
        senha=generate_password_hash(dados.senha),
        tipo=dados.tipo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"Usuário cadastrado com sucesso: {user.id} - {user.email}")
    return user


@app.post("/api/auth/login")
def login_usuario(dados: LoginUsuario, request: Request, db: Session = Depends(get_session)):
    logger.info(f"Tentativa de login: {dados.email}")
    
    user = db.exec(select(User).where(User.email == dados.email)).first()

    if user and check_password_hash(user.senha, dados.senha):
        request.session["user_id"] = user.id
        request.session["user_nome"] = user.nome
        request.session["user_tipo"] = user.tipo
        logger.info(f"Login bem-sucedido: {user.id} - {user.email}")
        return {"ok": True, "nome": user.nome, "tipo": user.tipo}

    logger.warning(f"Tentativa de login falhou: {dados.email}")
    raise HTTPException(status_code=401, detail="Login inválido")


@app.post("/api/auth/logout")
def logout(request: Request):
    user_id = request.session.get("user_id")
    ong_id = request.session.get("ong_id")
    request.session.clear()
    logger.info(f"Logout realizado: user_id={user_id}, ong_id={ong_id}")
    return {"ok": True}


@app.get("/api/auth/me", response_model=MeResponse)
def me(request: Request):
    usuario = usuario_logado(request)
    if usuario:
        return MeResponse(
            autenticado=True,
            tipo_sessao="usuario",
            id=usuario["id"],
            nome=usuario["nome"],
            tipo_usuario=usuario["tipo"],
        )

    ong = ong_logada(request)
    if ong:
        return MeResponse(
            autenticado=True,
            tipo_sessao="ong",
            id=ong["id"],
            nome=ong["nome"],
        )

    return MeResponse(autenticado=False)


# ================= ONGS =================

@app.post("/api/ongs", response_model=OngRead, status_code=status.HTTP_201_CREATED)
def cadastrar_ong(dados: OngCreate, db: Session = Depends(get_session)):
    logger.info(f"Tentativa de cadastro de ONG: {dados.cnpj}")
    
    existente = db.exec(select(Ong).where(Ong.cnpj == dados.cnpj)).first()
    if existente:
        logger.warning(f"Tentativa de cadastro com CNPJ já existente: {dados.cnpj}")
        raise HTTPException(status_code=409, detail="CNPJ já cadastrado")

    ong = Ong(
        nome=dados.nome,
        cnpj=dados.cnpj,
        endereco=dados.endereco,
        contato=dados.contato,
        senha=generate_password_hash(dados.senha),
    )
    db.add(ong)
    db.commit()
    db.refresh(ong)
    
    logger.info(f"ONG cadastrada com sucesso: {ong.id} - {ong.cnpj}")
    return ong


@app.post("/api/ongs/login")
def login_ong(dados: LoginOng, request: Request, db: Session = Depends(get_session)):
    cnpj = limpar_cnpj(dados.cnpj)
    logger.info(f"Tentativa de login ONG: {cnpj}")
    
    ong = db.exec(select(Ong).where(Ong.cnpj == cnpj)).first()

    if ong and check_password_hash(ong.senha, dados.senha):
        request.session["ong_id"] = ong.id
        request.session["ong_nome"] = ong.nome
        logger.info(f"Login ONG bem-sucedido: {ong.id} - {ong.nome}")
        return {"ok": True, "nome": ong.nome}

    logger.warning(f"Tentativa de login ONG falhou: {cnpj}")
    raise HTTPException(status_code=401, detail="CNPJ ou senha inválidos")


# ================= ANIMAIS =================

@app.post("/api/animals", response_model=AnimalRead, status_code=status.HTTP_201_CREATED)
def cadastrar_animal(
    dados: AnimalCreate,
    request: Request,
    db: Session = Depends(get_session),
    ong: dict = Depends(exigir_ong),
):
    logger.info(f"Tentativa de cadastro de animal pela ONG: {ong['id']}")
    
    animal = Animal(
        nome=dados.nome,
        especie=dados.especie,
        raca=dados.raca,
        idade=dados.idade,
        sexo=dados.sexo,
        descricao=dados.descricao,
        status="Disponível",
        ong_id=ong["id"],
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)
    
    logger.info(f"Animal cadastrado com sucesso: {animal.id} - {animal.nome}")
    return animal


@app.get("/api/animals", response_model=List[AnimalRead])
def listar_animais(
    request: Request,
    status_filtro: Optional[str] = None,
    minha_ong: bool = False,
    db: Session = Depends(get_session),
):
    query = select(Animal)

    if minha_ong:
        ong = exigir_ong(request)
        query = query.where(Animal.ong_id == ong["id"])
        logger.info(f"Listando animais da ONG: {ong['id']}")

    if status_filtro:
        query = query.where(Animal.status == status_filtro)

    animais = db.exec(query).all()

    if not minha_ong:
        usuario = usuario_logado(request)
        if usuario:
            ids_pendentes = set(
                db.exec(
                    select(Adocao.animal_id).where(
                        Adocao.usuario_id == usuario["id"],
                        Adocao.status == "Pendente",
                    )
                ).all()
            )
            if ids_pendentes:
                animais = [a for a in animais if a.id not in ids_pendentes]

    return animais


@app.get("/api/animals/{animal_id}", response_model=AnimalRead)
def detalhes_animal(animal_id: int, db: Session = Depends(get_session)):
    animal = db.get(Animal, animal_id)
    if not animal:
        logger.warning(f"Animal não encontrado: {animal_id}")
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    return animal


@app.put("/api/animals/{animal_id}", response_model=AnimalRead)
def editar_animal(
    animal_id: int,
    dados: AnimalUpdate,
    db: Session = Depends(get_session),
    ong: dict = Depends(exigir_ong),
):
    logger.info(f"Tentativa de editar animal {animal_id} pela ONG: {ong['id']}")
    
    animal = db.get(Animal, animal_id)
    if not animal:
        logger.warning(f"Animal não encontrado para edição: {animal_id}")
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    if animal.ong_id != ong["id"]:
        logger.warning(f"Tentativa de editar animal de outra ONG: {animal_id}")
        raise HTTPException(status_code=403, detail="Animal não pertence à sua ONG")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(animal, campo, valor)

    db.add(animal)
    db.commit()
    db.refresh(animal)
    
    logger.info(f"Animal editado com sucesso: {animal_id}")
    return animal


@app.delete("/api/animals/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_animal(
    animal_id: int,
    db: Session = Depends(get_session),
    ong: dict = Depends(exigir_ong),
):
    logger.info(f"Tentativa de excluir animal {animal_id} pela ONG: {ong['id']}")
    
    animal = db.get(Animal, animal_id)
    if not animal:
        logger.warning(f"Animal não encontrado para exclusão: {animal_id}")
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    if animal.ong_id != ong["id"]:
        logger.warning(f"Tentativa de excluir animal de outra ONG: {animal_id}")
        raise HTTPException(status_code=403, detail="Animal não pertence à sua ONG")

    db.delete(animal)
    db.commit()
    logger.info(f"Animal excluído com sucesso: {animal_id}")
    return None


# ================= ADOÇÃO =================

@app.post("/api/animals/{animal_id}/adopt")
def solicitar_adocao(
    animal_id: int,
    dados: AdocaoSolicitar,
    db: Session = Depends(get_session),
    usuario: dict = Depends(exigir_usuario),
):
    logger.info(f"Tentativa de solicitar adoção do animal {animal_id} pelo usuário: {usuario['id']}")
    
    animal = db.get(Animal, animal_id)
    if not animal:
        logger.warning(f"Animal não encontrado para adoção: {animal_id}")
        raise HTTPException(status_code=404, detail="Animal não encontrado")
    
    if animal.status != "Disponível":
        logger.warning(f"Tentativa de adotar animal não disponível: {animal_id}")
        raise HTTPException(status_code=400, detail="Animal não está disponível para adoção")

    ja_pendente = db.exec(
        select(Adocao).where(
            Adocao.animal_id == animal_id,
            Adocao.usuario_id == usuario["id"],
            Adocao.status == "Pendente",
        )
    ).first()
    if ja_pendente:
        logger.warning(f"Usuário {usuario['id']} já tem solicitação pendente para o animal {animal_id}")
        raise HTTPException(status_code=400, detail="Você já tem uma solicitação pendente para este animal")

    nova_adocao = Adocao(
        usuario_id=usuario["id"],
        animal_id=animal_id,
        data=date.today(),
        status="Pendente",
    )
    db.add(nova_adocao)
    db.commit()
    db.refresh(nova_adocao)

    formulario = FormularioAdocao(
        adocao_id=nova_adocao.id,
        telefone=dados.telefone,
        endereco=dados.endereco,
        cpf=dados.cpf,
        rg=dados.rg,
        motivo=dados.motivo,
    )
    db.add(formulario)
    db.commit()

    logger.info(f"Solicitação de adoção criada: {nova_adocao.id}")
    return {"mensagem": "Solicitação enviada com sucesso!"}


@app.get("/api/adoptions/mine", response_model=List[AdocaoRead])
def minhas_adocoes(
    db: Session = Depends(get_session),
    usuario: dict = Depends(exigir_usuario),
):
    logger.info(f"Listando adoções do usuário: {usuario['id']}")
    
    # Buscar adoções com os animais em uma única query
    adocoes = db.exec(
        select(Adocao).where(Adocao.usuario_id == usuario["id"])
    ).all()

    resultado = []
    for adocao in adocoes:
        animal = db.get(Animal, adocao.animal_id)
        if animal:
            resultado.append(
                AdocaoRead(id=adocao.id, animal=animal, status=adocao.status, data=adocao.data)
            )
    
    return resultado


@app.get("/api/adoptions/requests", response_model=List[SolicitacaoRead])
def solicitacoes_da_ong(
    db: Session = Depends(get_session),
    ong: dict = Depends(exigir_ong),
):
    logger.info(f"Listando solicitações da ONG: {ong['id']}")
    
    # Buscar todas as adoções com animais e usuários
    solicitacoes = db.exec(select(Adocao)).all()

    resultado = []
    for s in solicitacoes:
        animal = db.get(Animal, s.animal_id)
        if not animal or animal.ong_id != ong["id"]:
            continue
        usuario = db.get(User, s.usuario_id)
        if usuario:
            formulario = db.exec(
                select(FormularioAdocao).where(FormularioAdocao.adocao_id == s.id)
            ).first()
            resultado.append(
                SolicitacaoRead(
                    id=s.id,
                    animal=animal,
                    usuario=usuario,
                    status=s.status,
                    formulario=formulario,
                )
            )
    
    return resultado


@app.post("/api/adoptions/{adocao_id}/approve")
def aprovar_adocao(
    adocao_id: int,
    db: Session = Depends(get_session),
    ong: dict = Depends(exigir_ong),
):
    logger.info(f"Tentativa de aprovar adoção {adocao_id} pela ONG: {ong['id']}")
    
    adocao = db.get(Adocao, adocao_id)
    if not adocao:
        logger.warning(f"Solicitação não encontrada: {adocao_id}")
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    animal = db.get(Animal, adocao.animal_id)
    if animal.ong_id != ong["id"]:
        logger.warning(f"Tentativa de aprovar solicitação de outra ONG: {adocao_id}")
        raise HTTPException(status_code=403, detail="Solicitação não pertence à sua ONG")

    if adocao.status != "Pendente":
        logger.warning(f"Tentativa de aprovar solicitação já processada: {adocao_id}")
        raise HTTPException(status_code=400, detail="Solicitação já foi processada")

    adocao.status = "Aprovada"
    animal.status = "Adotado"
    db.add(adocao)
    db.add(animal)

    outras_pendentes = db.exec(
        select(Adocao).where(
            Adocao.animal_id == animal.id,
            Adocao.id != adocao.id,
            Adocao.status == "Pendente",
        )
    ).all()
    for outra in outras_pendentes:
        outra.status = "Recusada"
        db.add(outra)
    if outras_pendentes:
        logger.info(
            f"{len(outras_pendentes)} outra(s) solicitação(ões) pendente(s) do animal {animal.id} "
            f"recusada(s) automaticamente após aprovação de {adocao.id}"
        )
    db.commit()

    logger.info(f"Adoção aprovada: {adocao_id}")
    return {"mensagem": "Solicitação aprovada"}


@app.post("/api/adoptions/{adocao_id}/reject")
def recusar_adocao(
    adocao_id: int,
    db: Session = Depends(get_session),
    ong: dict = Depends(exigir_ong),
):
    logger.info(f"Tentativa de recusar adoção {adocao_id} pela ONG: {ong['id']}")
    
    adocao = db.get(Adocao, adocao_id)
    if not adocao:
        logger.warning(f"Solicitação não encontrada: {adocao_id}")
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    animal = db.get(Animal, adocao.animal_id)
    if animal.ong_id != ong["id"]:
        logger.warning(f"Tentativa de recusar solicitação de outra ONG: {adocao_id}")
        raise HTTPException(status_code=403, detail="Solicitação não pertence à sua ONG")

    if adocao.status != "Pendente":
        logger.warning(f"Tentativa de recusar solicitação já processada: {adocao_id}")
        raise HTTPException(status_code=400, detail="Solicitação já foi processada")

    adocao.status = "Recusada"
    animal.status = "Disponível"
    db.add(adocao)
    db.add(animal)
    db.commit()

    logger.info(f"Adoção recusada: {adocao_id}")
    return {"mensagem": "Solicitação recusada"}