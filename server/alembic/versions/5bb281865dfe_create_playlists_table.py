from alembic import op
import sqlalchemy as sa


revision = '5bb281865dfe'
down_revision = '07c6dbced816'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('playlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('private', sa.Boolean(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_playlists_name'), 'playlists', ['name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_playlists_name'), table_name='playlists')
    op.drop_table('playlists')
