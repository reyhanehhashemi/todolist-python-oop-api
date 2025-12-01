"""add closed_at field to DBTask

Revision ID: d22d34063efa
Revises: 5ff3bf7f75ca
Create Date: 2025-11-26 19:59:26.252247
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd22d34063efa'
down_revision: Union[str, Sequence[str], None] = '5ff3bf7f75ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ---- Project fields ----
    op.alter_column('projects', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('projects', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('projects', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_constraint(op.f('projects_title_key'), 'projects', type_='unique')

    # ---- Add new column closed_at ----
    op.add_column('tasks', sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True))

    # ---- Task fields ----
    op.alter_column('tasks', 'description',
               existing_type=sa.TEXT(),
               nullable=False)

    # IMPORTANT: Fix enum conversion manually
    op.execute("ALTER TABLE tasks ALTER COLUMN status TYPE taskstatus USING status::taskstatus")

    op.alter_column('tasks', 'deadline',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('tasks', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('tasks', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

    op.create_index(op.f('ix_tasks_project_id'), 'tasks', ['project_id'], unique=False)
    op.create_index(op.f('ix_tasks_status'), 'tasks', ['status'], unique=False)
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_status'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_project_id'), table_name='tasks')

    op.alter_column('tasks', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('tasks', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('tasks', 'deadline',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)

    # Reverse ENUM conversion
    op.alter_column(
        'tasks', 'status',
        existing_type=sa.Enum('TODO', 'DOING', 'DONE', name='taskstatus'),
        type_=sa.VARCHAR(length=5),
        existing_nullable=False
    )

    op.alter_column('tasks', 'description',
               existing_type=sa.TEXT(),
               nullable=True)

    op.drop_column('tasks', 'closed_at')

    op.create_unique_constraint(
        op.f('projects_title_key'),
        'projects',
        ['title'],
        postgresql_nulls_not_distinct=False
    )

    op.alter_column('projects', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('projects', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('projects', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
