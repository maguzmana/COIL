"""Inicial

Revision ID: a3024c55c12e
Revises: 
Create Date: 2024-11-15 13:13:18.396383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3024c55c12e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Convertir columna 'goal' a Enum
    op.alter_column('users', 'goal',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
                    existing_nullable=False,
                    postgresql_using='goal::text::goalenum')

    # Convertir columna 'physical_activity_level' a Enum
    op.alter_column('users', 'physical_activity_level',
                    existing_type=sa.INTEGER(),
                    type_=sa.Enum('low', 'medium', 'high', name='activitylevelenum'),
                    existing_nullable=False,
                    postgresql_using='physical_activity_level::text::activitylevelenum')

    # Convertir columna 'health_conditions' a Enum
    op.alter_column('users', 'health_conditions',
                    existing_type=sa.TEXT(),
                    type_=sa.Enum('diabetes', 'hypertension', 'kidney_disease', name='healthconditionenum'),
                    existing_nullable=True,
                    postgresql_using='health_conditions::text::healthconditionenum')


def downgrade() -> None:
    # Revertir columna 'health_conditions' a TEXT
    op.alter_column('users', 'health_conditions',
                    existing_type=sa.Enum('diabetes', 'hypertension', 'kidney_disease', name='healthconditionenum'),
                    type_=sa.TEXT(),
                    existing_nullable=True)

    # Revertir columna 'physical_activity_level' a INTEGER
    op.alter_column('users', 'physical_activity_level',
                    existing_type=sa.Enum('low', 'medium', 'high', name='activitylevelenum'),
                    type_=sa.INTEGER(),
                    existing_nullable=False)

    # Revertir columna 'goal' a VARCHAR(50)
    op.alter_column('users', 'goal',
                    existing_type=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
