"""empty message

Revision ID: 8662225e788d
Revises: f9397e52de9c
Create Date: 2023-06-06 22:25:46.357266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8662225e788d"
down_revision = "f9397e52de9c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("articles_description_key", "articles", type_="unique")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(
        "articles_description_key", "articles", ["description"]
    )
    # ### end Alembic commands ###
