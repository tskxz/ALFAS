"""Adicionar campos de conclusão a resource_user

Revision ID: 91d04a2c6f8b
Revises: 0227eac53c32
Create Date: 2026-11-16

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "91d04a2c6f8b"
down_revision = "0227eac53c32"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("resource_user", sa.Column("started_at", sa.DateTime(), nullable=True))
    op.add_column(
        "resource_user",
        sa.Column("completed", sa.Boolean(), server_default=sa.text("0"), nullable=False),
    )
    op.add_column("resource_user", sa.Column("completed_at", sa.DateTime(), nullable=True))
    op.add_column("resource_user", sa.Column("certificate_code", sa.String(length=100), nullable=True))
    op.create_unique_constraint(
        op.f("uq_resource_user_certificate_code"),
        "resource_user",
        ["certificate_code"],
    )


def downgrade():
    op.drop_constraint(op.f("uq_resource_user_certificate_code"), "resource_user", type_="unique")
    op.drop_column("resource_user", "certificate_code")
    op.drop_column("resource_user", "completed_at")
    op.drop_column("resource_user", "completed")
    op.drop_column("resource_user", "started_at")
