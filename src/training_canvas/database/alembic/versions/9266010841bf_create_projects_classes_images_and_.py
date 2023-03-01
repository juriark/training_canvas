"""create projects, classes, images and checkpoints table

Revision ID: 9266010841bf
Revises: 
Create Date: 2023-02-28 14:26:06.406735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9266010841bf"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create projects table
    op.create_table(
        "projects",
        sa.Column(name="id", type_=sa.Integer(), primary_key=True),
        sa.Column(name="project_name", type_=sa.String(), nullable=False, unique=True),
    )

    # Create checkpoints table
    op.create_table(
        "checkpoints",
        sa.Column(name="id", type_=sa.Integer(), primary_key=True),
        sa.Column(name="project_id", type_=sa.Integer(), nullable=False),
        sa.Column(name="checkpoint_blob_name", type_=sa.String(), nullable=False),
    )
    op.create_foreign_key(
        constraint_name="fk_projects_checkpoint",
        source_table="checkpoints",
        referent_table="projects",
        local_cols=["project_id"],
        remote_cols=["id"],
    )
    op.create_unique_constraint(
        constraint_name="uc_checkpoint_blob_name_project_id",
        table_name="checkpoints",
        columns=("checkpoint_blob_name", "project_id"),
    )

    # Create classes table
    op.create_table(
        "classes",
        sa.Column(name="id", type_=sa.Integer(), primary_key=True),
        sa.Column(name="label", type_=sa.String(), nullable=False),
        sa.Column(name="project_id", type_=sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        constraint_name="fk_projects_classes",
        source_table="classes",
        referent_table="projects",
        local_cols=["project_id"],
        remote_cols=["id"],
    )
    op.create_unique_constraint(
        constraint_name="uc_label_project_id",
        table_name="classes",
        columns=("label", "project_id"),
    )

    # Create images table
    op.create_table(
        "images",
        sa.Column(name="blob_name", type_=sa.String(), unique=True, nullable=False),
        sa.Column(name="classes_id", type_=sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        constraint_name="fk_classes_images",
        source_table="images",
        referent_table="classes",
        local_cols=["classes_id"],
        remote_cols=["id"],
    )


def downgrade() -> None:
    # Drop tables in correct order
    op.drop_table(table_name="images")
    op.drop_table(table_name="classes")
    op.drop_table(table_name="checkpoints")
    op.drop_table(table_name="projects")
