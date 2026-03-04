"""initial schema

Revision ID: 6b0d5036c48c
Revises: 
Create Date: 2026-02-28 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6b0d5036c48c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("sku", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False, server_default="0"),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_products_sku", "products", ["sku"], unique=True)

    op.create_table(
        "sales",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("invoice_number", sa.String(), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False, server_default="0"),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_sales_invoice_number", "sales", ["invoice_number"], unique=True)

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("transaction_type", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("reference", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sale_items",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("sale_id", sa.Integer(), sa.ForeignKey("sales.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("sale_items")
    op.drop_table("transactions")
    op.drop_index("ix_sales_invoice_number", table_name="sales")
    op.drop_table("sales")
    op.drop_index("ix_products_sku", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
