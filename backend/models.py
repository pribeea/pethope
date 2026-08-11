"""
Modelos de tabela (SQLModel) usados pelo backend FastAPI.

Tabelas: user, ong, animal, adocao, formularioadocao — mesma modelagem de
dados do protótipo original.
"""
from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    senha: str
    tipo: str  # "voluntario" ou "adotante"


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


class FormularioAdocao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    adocao_id: int = Field(foreign_key="adocao.id")
    telefone: str
    endereco: str
    cpf: str
    rg: str
    motivo: str
