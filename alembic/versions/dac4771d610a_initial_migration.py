"""Initial migration

Revision ID: dac4771d610a
Revises: 
Create Date: 2024-11-07 23:01:34.124551
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dac4771d610a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear los tipos ENUM antes de usarlos en las columnas
    op.execute("CREATE TYPE goalenum AS ENUM ('lose_weight', 'gain_muscle', 'health_maintenance')")
    op.execute("CREATE TYPE activitylevelenum AS ENUM ('low', 'medium', 'high')")
    op.execute("CREATE TYPE healthconditionenum AS ENUM ('diabetes', 'hypertension', 'kidney_disease')")

    # Modificar las columnas para usar los tipos ENUM con la conversión explícita de los datos
    op.alter_column('users', 'goal',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
               existing_nullable=False,
               postgresql_using="goal::goalenum")
    op.alter_column('users', 'physical_activity_level',
               existing_type=sa.INTEGER(),
               type_=sa.Enum('low', 'medium', 'high', name='activitylevelenum'),
               existing_nullable=False)
    op.alter_column('users', 'health_conditions',
               existing_type=sa.TEXT(),
               type_=sa.Enum('diabetes', 'hypertension', 'kidney_disease', name='healthconditionenum'),
               existing_nullable=True)


def downgrade() -> None:
    # Eliminar los tipos ENUM si es necesario durante el downgrade
    op.execute("DROP TYPE goalenum")
    op.execute("DROP TYPE activitylevelenum")
    op.execute("DROP TYPE healthconditionenum")

    # Revertir las columnas a sus tipos anteriores
    op.alter_column('users', 'health_conditions',
               existing_type=sa.Enum('diabetes', 'hypertension', 'kidney_disease', name='healthconditionenum'),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('users', 'physical_activity_level',
               existing_type=sa.Enum('low', 'medium', 'high', name='activitylevelenum'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('users', 'goal',
               existing_type=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
