"""Initial migration: create projects and tasks tables

Revision ID: 95f7d501bc4b
Revises:
Create Date: 2025-11-22 23:06:37.546475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95f7d501bc4b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_projects_title'), 'projects', ['title'], unique=True)

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=5), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('deadline', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add foreign key with CASCADE explicitly using SQL
    op.execute(
        'ALTER TABLE tasks ADD CONSTRAINT fk_tasks_project_id '
        'FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tasks')
    op.drop_index(op.f('ix_projects_title'), table_name='projects')
    op.drop_table('projects')
