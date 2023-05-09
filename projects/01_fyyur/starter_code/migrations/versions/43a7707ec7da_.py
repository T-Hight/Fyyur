"""empty message

Revision ID: 43a7707ec7da
Revises: 00e8870340fa
Create Date: 2023-05-04 07:08:52.243392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '43a7707ec7da'
down_revision = '00e8870340fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.alter_column('start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
        batch_op.drop_column('artist_image_link')
        batch_op.drop_column('venue_name')
        batch_op.drop_column('artist_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artist_name', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('venue_name', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('artist_image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
        batch_op.alter_column('start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    # ### end Alembic commands ###
