"""add example

Revision ID: 66889ad86072
Revises: 0.1
Create Date: 2023-07-11 17:02:43.659825

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0.2'
down_revision = '0.1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ex_simples',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('field_string', sa.String(length=32), nullable=False),
                    sa.Column('field_integer', sa.Integer(), nullable=True),
                    sa.Column('field_float', sa.Float(), nullable=True),
                    sa.Column('field_boolean', sa.Boolean(), nullable=True),
                    sa.Column('field_text', sa.Text(), nullable=True),
                    sa.Column('field_datetime', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('field_string')
                    )
    op.create_table('ex_departments',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=32), nullable=False),
                    sa.Column('parent_id', sa.Integer(), nullable=True),
                    sa.Column('default', sa.Boolean(), nullable=True),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['parent_id'], ['ex_departments.id'], ondelete='SET NULL'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('ex_employees',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=32), nullable=False),
                    sa.Column('age', sa.Integer(), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('department_id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.CheckConstraint('age > 0', name='age_positive'),
                    sa.ForeignKeyConstraint(['department_id'], ['ex_departments.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ex_employees')
    op.drop_table('ex_departments')
    op.drop_table('ex_simples')
    # ### end Alembic commands ###
