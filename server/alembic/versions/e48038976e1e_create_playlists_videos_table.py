from alembic import op
import sqlalchemy as sa


revision = 'e48038976e1e'
down_revision = '5bb281865dfe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('playlists_videos',
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlists.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('playlist_id', 'video_id')
    )
    

def downgrade() -> None:
    op.drop_table('playlists_videos')
