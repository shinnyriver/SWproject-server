"""Initial migration

Revision ID: e7153efc39ff
Revises: 
Create Date: 2024-05-14 00:50:13.438353

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e7153efc39ff"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "message",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=True),
        sa.Column("receiver_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.String(length=1000), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["receiver_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sender_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "photo",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("image_path", sa.String(length=200), nullable=True),
        sa.Column("description", sa.String(length=200), nullable=True),
        sa.Column("keywords", sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("photo")
    op.drop_table("message")
    op.drop_table("user")
    # ### end Alembic commands ###
