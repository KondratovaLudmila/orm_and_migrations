"""remove students phone

Revision ID: 6402bffbe821
Revises: 906d04360a67
Create Date: 2023-12-09 17:22:54.789590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6402bffbe821'
down_revision: Union[str, None] = '906d04360a67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'phone')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('phone', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
