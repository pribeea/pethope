"""Schemas Pydantic usados nos requests/responses da API FastAPI."""
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator

# ================= USUÁRIOS =================

class UserCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6)
    tipo: str  # "voluntario" | "adotante"
    
    @validator('tipo')
    def tipo_valido(cls, v):
        if v not in ["voluntario", "adotante"]:
            raise ValueError('Tipo deve ser "voluntario" ou "adotante"')
        return v


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    tipo: str


class LoginUsuario(BaseModel):
    email: EmailStr
    senha: str


# ================= ONGS =================

class OngCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=200)
    cnpj: str
    endereco: Optional[str] = None
    contato: Optional[str] = None
    senha: str = Field(min_length=6)
    
    @validator('cnpj')
    def cnpj_valido(cls, v):
        # Remove caracteres não numéricos
        cnpj_clean = ''.join(filter(str.isdigit, v))
        if len(cnpj_clean) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        return cnpj_clean


class OngRead(BaseModel):
    id: int
    nome: str
    cnpj: str
    endereco: Optional[str] = None
    contato: Optional[str] = None


class LoginOng(BaseModel):
    cnpj: str
    senha: str


# ================= SESSÃO / AUTENTICAÇÃO =================

class MeResponse(BaseModel):
    autenticado: bool
    tipo_sessao: Optional[str] = None  # "usuario" | "ong"
    id: Optional[int] = None
    nome: Optional[str] = None
    tipo_usuario: Optional[str] = None


# ================= ANIMAIS =================

class AnimalCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    especie: str = Field(min_length=1, max_length=50)
    raca: Optional[str] = Field(None, max_length=50)
    idade: Optional[int] = None
    sexo: Optional[str] = None
    descricao: Optional[str] = Field(None, max_length=500)
    
    @validator('idade')
    def idade_positiva(cls, v):
        if v is not None and v < 0:
            raise ValueError('Idade deve ser um número positivo')
        return v
    
    @validator('sexo')
    def sexo_valido(cls, v):
        if v is not None and v not in ['Macho', 'Fêmea', 'Outro']:
            raise ValueError('Sexo deve ser "Macho", "Fêmea" ou "Outro"')
        return v


class AnimalUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    especie: Optional[str] = Field(None, min_length=1, max_length=50)
    raca: Optional[str] = Field(None, max_length=50)
    idade: Optional[int] = None
    sexo: Optional[str] = None
    descricao: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = None
    
    @validator('idade')
    def idade_positiva(cls, v):
        if v is not None and v < 0:
            raise ValueError('Idade deve ser um número positivo')
        return v
    
    @validator('sexo')
    def sexo_valido(cls, v):
        if v is not None and v not in ['Macho', 'Fêmea', 'Outro']:
            raise ValueError('Sexo deve ser "Macho", "Fêmea" ou "Outro"')
        return v
    
    @validator('status')
    def status_valido(cls, v):
        if v is not None and v not in ['Disponível', 'Em processo de adoção', 'Adotado']:
            raise ValueError('Status inválido')
        return v


class AnimalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    especie: str
    raca: Optional[str] = None
    idade: Optional[int] = None
    sexo: Optional[str] = None
    descricao: Optional[str] = None
    status: str
    ong_id: int


# ================= ADOÇÃO =================

class AdocaoSolicitar(BaseModel):
    telefone: str = Field(min_length=10, max_length=20)
    endereco: str = Field(min_length=5, max_length=200)
    cpf: str
    rg: str
    motivo: str = Field(min_length=10, max_length=500)
    
    @validator('cpf')
    def cpf_valido(cls, v):
        cpf_clean = ''.join(filter(str.isdigit, v))
        if len(cpf_clean) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        return cpf_clean


class AdocaoRead(BaseModel):
    id: int
    animal: AnimalRead
    status: str
    data: date


class FormularioAdocaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    telefone: str
    endereco: str
    cpf: str
    rg: str
    motivo: str


class SolicitacaoRead(BaseModel):
    id: int
    animal: AnimalRead
    usuario: UserRead
    status: str
    formulario: Optional[FormularioAdocaoRead] = None