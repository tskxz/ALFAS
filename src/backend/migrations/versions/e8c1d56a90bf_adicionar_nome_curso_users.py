"""Adicionar o nome do curso ao perfil do utilizador."""

from alembic import op
import sqlalchemy as sa

revision = "e8c1d56a90bf"
down_revision = "c14e8a27b603"
branch_labels = None
depends_on = None


def upgrade():
    colunas = {coluna["name"] for coluna in sa.inspect(op.get_bind()).get_columns("users")}
    if "course_name" not in colunas:
        op.add_column("users", sa.Column("course_name", sa.String(length=255), nullable=True))


def downgrade():
    colunas = {coluna["name"] for coluna in sa.inspect(op.get_bind()).get_columns("users")}
    if "course_name" in colunas:
        op.drop_column("users", "course_name")
