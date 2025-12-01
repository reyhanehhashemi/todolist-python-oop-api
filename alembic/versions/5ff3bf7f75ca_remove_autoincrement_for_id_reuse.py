"""remove autoincrement for id reuse

Revision ID: 5ff3bf7f75ca
Revises: 95f7d501bc4b
Create Date: 2025-11-25 21:19:xx.xxxxxx

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5ff3bf7f75ca'
down_revision: Union[str, None] = '95f7d501bc4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove autoincrement from projects and tasks tables."""

    # Remove sequence from projects.id
    op.execute("ALTER TABLE projects ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE IF EXISTS projects_id_seq CASCADE")

    # Remove sequence from tasks.id
    op.execute("ALTER TABLE tasks ALTER COLUMN id DROP DEFAULT")
    op.execute("DROP SEQUENCE IF EXISTS tasks_id_seq CASCADE")


def downgrade() -> None:
    """Restore autoincrement to projects and tasks tables."""

    # Restore sequence for projects.id
    op.execute("CREATE SEQUENCE projects_id_seq")
    op.execute("ALTER TABLE projects ALTER COLUMN id SET DEFAULT nextval('projects_id_seq')")
    op.execute("SELECT setval('projects_id_seq', COALESCE(MAX(id), 1)) FROM projects")

    # Restore sequence for tasks.id
    op.execute("CREATE SEQUENCE tasks_id_seq")
    op.execute("ALTER TABLE tasks ALTER COLUMN id SET DEFAULT nextval('tasks_id_seq')")
    op.execute("SELECT setval('tasks_id_seq', COALESCE(MAX(id), 1)) FROM tasks")
