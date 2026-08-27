"""adiciona atividades e inscricoes de voluntariado

Revision ID: a223b618bcc7
Revises: a4b26240f225
Create Date: 2026-08-26 17:35:32.189363

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = 'a223b618bcc7'
down_revision: Union[str, Sequence[str], None] = 'a4b26240f225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cria as tabelas de atividades e inscrições."""
    op.create_table('atividade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('descricao', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dias', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('horario', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('detalhes', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('vagas', sa.Integer(), nullable=False),
    sa.Column('ong_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ong_id'], ['ong.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inscricaoatividade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('atividade_id', sa.Integer(), nullable=False),
    sa.Column('voluntario_id', sa.Integer(), nullable=False),
    sa.Column('telefone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('motivo', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('data_inscricao', sa.DateTime(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['atividade_id'], ['atividade.id'], ),
    sa.ForeignKeyConstraint(['voluntario_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Remove as tabelas de voluntariado."""
    op.drop_table('inscricaoatividade')
    op.drop_table('atividade')