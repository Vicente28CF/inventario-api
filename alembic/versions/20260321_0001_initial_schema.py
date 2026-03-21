"""initial schema

Revision ID: 20260321_0001
Revises:
Create Date: 2026-03-21 14:05:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260321_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


tipo_movimiento = sa.Enum("entrada", "salida", name="tipomovimiento")


def upgrade() -> None:
    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_categorias_id"), "categorias", ["id"], unique=False)

    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("rol", sa.String(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=True)
    op.create_index(op.f("ix_usuarios_id"), "usuarios", ["id"], unique=False)

    op.create_table(
        "productos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("precio", sa.Float(), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column("stock_minimo", sa.Integer(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.Column("actualizado_en", sa.DateTime(timezone=True), nullable=True),
        sa.Column("categoria_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_productos_id"), "productos", ["id"], unique=False)
    op.create_index(op.f("ix_productos_nombre"), "productos", ["nombre"], unique=False)

    tipo_movimiento.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "movimientos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo", tipo_movimiento, nullable=False),
        sa.Column("cantidad", sa.Integer(), nullable=False),
        sa.Column("nota", sa.String(), nullable=True),
        sa.Column("creado_en", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
        sa.Column("producto_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["producto_id"], ["productos.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_movimientos_id"), "movimientos", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_movimientos_id"), table_name="movimientos")
    op.drop_table("movimientos")
    tipo_movimiento.drop(op.get_bind(), checkfirst=True)

    op.drop_index(op.f("ix_productos_nombre"), table_name="productos")
    op.drop_index(op.f("ix_productos_id"), table_name="productos")
    op.drop_table("productos")

    op.drop_index(op.f("ix_usuarios_id"), table_name="usuarios")
    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_table("usuarios")

    op.drop_index(op.f("ix_categorias_id"), table_name="categorias")
    op.drop_table("categorias")
