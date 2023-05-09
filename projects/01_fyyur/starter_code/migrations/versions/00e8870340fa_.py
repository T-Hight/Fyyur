"""empty message

Revision ID: 00e8870340fa
Revises: 3180c7b8df95
Create Date: 2023-05-02 13:36:21.869315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '00e8870340fa'
down_revision = '3180c7b8df95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=120)),
               nullable=False)

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    # ### end Alembic commands ###
