"""initial migration

Revision ID: 017dc17819fd
Revises: 
Create Date: 2025-01-05 18:50:03.138128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '017dc17819fd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('case_records',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('procedure_name', sa.String(), nullable=True),
    sa.Column('cpt_codes', sa.String(), nullable=True),
    sa.Column('steps', sa.JSON(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('is_met', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('case_records')
    # ### end Alembic commands ###
