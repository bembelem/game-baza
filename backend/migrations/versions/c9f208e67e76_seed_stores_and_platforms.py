"""seed stores and platforms

Revision ID: c9f208e67e76
Revises: 076f4cd0d0a4
Create Date: 2026-05-05 14:34:08.187851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9f208e67e76'
down_revision: Union[str, Sequence[str], None] = '076f4cd0d0a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO stores (name) VALUES
        ('steam'), ('steambuy'), ('gabestore')
        ON CONFLICT (name) DO NOTHING
    """)

    op.execute("""
        INSERT INTO platforms (name) VALUES ('PC')
        ON CONFLICT (name) DO NOTHING
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM stores WHERE name IN ('steam', 'steambuy', 'gabestore')
    """)

    op.execute("""
        DELETE FROM platforms WHERE name = 'PC'
    """)