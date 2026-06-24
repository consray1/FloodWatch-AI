"""Add AI analysis and additional tables

Revision ID: 002
Revises: 001
Create Date: 2026-06-24

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('report_media',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('report_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('media_url', sa.String(500), nullable=False),
        sa.Column('media_type', sa.String(20), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('mime_type', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['report_id'], ['reports.id'])
    )
    op.create_index('idx_report_media_report_id', 'report_media', ['report_id'])

    op.create_table('ai_analysis',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('report_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('hazard_type', sa.String(50), nullable=True),
        sa.Column('hazard_category', sa.String(50), nullable=True),
        sa.Column('severity', sa.String(10), nullable=True),
        sa.Column('confidence', sa.Numeric(5, 4), nullable=True),
        sa.Column('entities', postgresql.JSONB(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('model_version', sa.String(20), nullable=False),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('report_id'),
        sa.ForeignKeyConstraint(['report_id'], ['reports.id'])
    )
    op.create_index('idx_ai_analysis_report_id', 'ai_analysis', ['report_id'])
    op.create_index('idx_ai_analysis_hazard_type', 'ai_analysis', ['hazard_type'])

    op.create_table('trust_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('factors', postgresql.JSONB(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'])
    )
    op.create_index('idx_trust_scores_user_id', 'trust_scores', ['user_id'])

    op.create_table('risk_scores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('score', sa.Numeric(5, 2), nullable=False),
        sa.Column('factors', postgresql.JSONB(), nullable=True),
        sa.Column('model_version', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'])
    )
    op.create_index('idx_risk_scores_incident_id', 'risk_scores', ['incident_id'])

    op.create_table('shelters',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=False),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=False),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('occupancy', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(20), nullable=False, server_default='available'),
        sa.Column('facilities', postgresql.JSONB(), nullable=True),
        sa.Column('contact_phone', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_shelters_location', 'shelters', ['latitude', 'longitude'])

    op.create_table('hospitals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Numeric(10, 8), nullable=False),
        sa.Column('longitude', sa.Numeric(11, 8), nullable=False),
        sa.Column('address', sa.String(500), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('emergency_phone', sa.String(20), nullable=True),
        sa.Column('beds_total', sa.Integer(), nullable=True),
        sa.Column('beds_available', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='open'),
        sa.Column('services', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_hospitals_location', 'hospitals', ['latitude', 'longitude'])


def downgrade() -> None:
    op.drop_table('hospitals')
    op.drop_table('shelters')
    op.drop_table('risk_scores')
    op.drop_table('trust_scores')
    op.drop_table('ai_analysis')
    op.drop_table('report_media')