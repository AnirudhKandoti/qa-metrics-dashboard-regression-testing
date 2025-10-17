from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='viewer')
    )
    op.create_table('pipelines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False, unique=True),
        sa.Column('description', sa.Text())
    )
    op.create_table('metrics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('pipeline_id', sa.Integer(), sa.ForeignKey('pipelines.id'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('ts', sa.DateTime(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False)
    )
    op.create_unique_constraint('uix_metric_point', 'metrics', ['pipeline_id', 'name', 'ts'])
    op.create_table('anomalies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('metric_id', sa.Integer(), sa.ForeignKey('metrics.id'), index=True),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('is_anomaly', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('detected_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('anomalies')
    op.drop_constraint('uix_metric_point', 'metrics', type_='unique')
    op.drop_table('metrics')
    op.drop_table('pipelines')
    op.drop_table('users')
