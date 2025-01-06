"""cpt_codes to array

Revision ID: xxx
Revises: previous_revision_id
Create Date: 2024-xx-xx

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '17e7215db1ce'
down_revision: Union[str, None] = 'ad73f4be7a29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Convert to ARRAY type
    op.alter_column('case_records', 'cpt_codes',
        type_=postgresql.ARRAY(sa.String()),
        existing_type=sa.String(),
        postgresql_using='ARRAY[cpt_codes]'
    )

def downgrade() -> None:
    # Convert back to string
    op.alter_column('case_records', 'cpt_codes',
        type_=sa.String(),
        existing_type=postgresql.ARRAY(sa.String()),
        postgresql_using='cpt_codes[1]'  # Takes first element if converting back
    )
