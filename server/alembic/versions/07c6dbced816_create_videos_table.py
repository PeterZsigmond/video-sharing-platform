from alembic import op
import sqlalchemy as sa


revision = '07c6dbced816'
down_revision = '23757accfb3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('uploader_id', sa.Integer(), nullable=False),
    sa.Column('uploaded_at', sa.DateTime(), nullable=False),
    sa.Column('private', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['uploader_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('videos')
