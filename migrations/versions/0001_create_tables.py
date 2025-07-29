from alembic import op
import sqlalchemy as sa

revision = '0001_create_tables'
down_revision = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('language', sa.String(2), nullable=False, server_default='en'),
        sa.Column('balance', sa.Numeric(18,6), nullable=False, server_default='0'),
        sa.Column('hashpower', sa.Numeric(18,6), nullable=False, server_default='0'),
        sa.Column('referrer_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('report_time', sa.JSON, nullable=True),
    )
    op.create_table(
        'purchases',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('ths', sa.Numeric(18,6), nullable=False),
        sa.Column('price', sa.Numeric(18,6), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'daily_payouts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('amount', sa.Numeric(18,6), nullable=False),
        sa.Column('date', sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table(
        'support_requests',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('message', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('support_requests')
    op.drop_table('daily_payouts')
    op.drop_table('purchases')
    op.drop_table('users')
