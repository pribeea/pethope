"""baseline inicial - user, ong, animal, adocao, formularioadocao
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


revision: str = 'a4b26240f225'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ong',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cnpj', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('endereco', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('contato', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('senha', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('senha', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('tipo', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('animal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('especie', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('raca', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('idade', sa.Integer(), nullable=True),
    sa.Column('sexo', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('descricao', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('ong_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ong_id'], ['ong.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('adocao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('animal_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['animal_id'], ['animal.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('formularioadocao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adocao_id', sa.Integer(), nullable=False),
    sa.Column('telefone', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('endereco', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cpf', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('rg', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('motivo', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['adocao_id'], ['adocao.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('formularioadocao')
    op.drop_table('adocao')
    op.drop_table('animal')
    op.drop_table('user')
    op.drop_table('ong')
