"""add favorite table

Revision ID: 0da103d7f95e
Revises: 3e561c865903
Create Date: 2024-04-03 18:22:48.287365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0da103d7f95e'
down_revision = '3e561c865903'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('applicant_id', sa.Integer(), nullable=True),
    sa.Column('Job_posting_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Job_posting_id'], ['job_postings.id'], name=op.f('fk_favorites_Job_posting_id_job_postings')),
    sa.ForeignKeyConstraint(['applicant_id'], ['applicants.id'], name=op.f('fk_favorites_applicant_id_applicants')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    # ### end Alembic commands ###
