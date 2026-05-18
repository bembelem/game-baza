"""fixing genres, platforms

Revision ID: 274a3f30e18b
Revises: 2c83d41a00b6
Create Date: 2026-05-05 00:40:41.202807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '274a3f30e18b'
down_revision: Union[str, Sequence[str], None] = '2c83d41a00b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('raw_offers', 'genres',
               existing_type=sa.TEXT(),
               type_=postgresql.ARRAY(sa.String()),
               postgresql_using='ARRAY[]::VARCHAR[]',
               existing_nullable=True)
    op.alter_column('raw_offers', 'platforms',
               existing_type=sa.TEXT(),
               type_=postgresql.ARRAY(sa.String()),
               postgresql_using='ARRAY[]::VARCHAR[]',
               existing_nullable=True)


def downgrade() -> None:
    op.alter_column('raw_offers', 'platforms',
               existing_type=postgresql.ARRAY(sa.String()),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('raw_offers', 'genres',
               existing_type=postgresql.ARRAY(sa.String()),
               type_=sa.TEXT(),
               existing_nullable=True)