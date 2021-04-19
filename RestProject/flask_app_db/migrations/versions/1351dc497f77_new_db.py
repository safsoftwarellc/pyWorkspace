"""new db

Revision ID: 1351dc497f77
Revises: 
Create Date: 2021-04-17 09:21:12.848444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1351dc497f77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('excel_data',
    sa.Column('data_id', sa.Integer(), nullable=False),
    sa.Column('excel_file_name', sa.String(length=50), nullable=False),
    sa.Column('excel_file_data', sa.LargeBinary(), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('data_id'),
    sa.UniqueConstraint('excel_file_name')
    )
    op.create_table('queue_config',
    sa.Column('config_id', sa.Integer(), nullable=False),
    sa.Column('queue_name', sa.String(length=50), nullable=False),
    sa.Column('config_name', sa.String(length=80), nullable=False),
    sa.Column('config_value', sa.String(length=120), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('config_id')
    )
    op.create_table('xml_data',
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=50), nullable=False),
    sa.Column('file_data', sa.LargeBinary(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('file_id'),
    sa.UniqueConstraint('file_name')
    )
    op.create_table('xpath_data',
    sa.Column('xpath_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('xpath_string', sa.String(length=250), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['xml_data.file_id'], ),
    sa.PrimaryKeyConstraint('xpath_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('xpath_data')
    op.drop_table('xml_data')
    op.drop_table('queue_config')
    op.drop_table('excel_data')
    # ### end Alembic commands ###
