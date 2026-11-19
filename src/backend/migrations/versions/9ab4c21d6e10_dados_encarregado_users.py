"""Adicionar os dados do encarregado de educação, se necessário."""

from alembic import op
import sqlalchemy as sa

revision = "9ab4c21d6e10"
down_revision = "0227eac53c32"
branch_labels = None
depends_on = None


def upgrade():
    colunas = {coluna["name"] for coluna in sa.inspect(op.get_bind()).get_columns("users")}
    if "guardian_name" not in colunas:
        op.add_column("users", sa.Column("guardian_name", sa.String(length=255), nullable=True))
    if "guardian_email" not in colunas:
        op.add_column("users", sa.Column("guardian_email", sa.String(length=255), nullable=True))


def downgrade():
    colunas = {coluna["name"] for coluna in sa.inspect(op.get_bind()).get_columns("users")}
    if "guardian_email" in colunas:
        op.drop_column("users", "guardian_email")
    if "guardian_name" in colunas:
        op.drop_column("users", "guardian_name")
