from typing import Sequence, Union  # Mover la importación aquí
from alembic import op
import sqlalchemy as sa

# Initial migration

# Revision identifiers, used by Alembic.
revision: str = 'dac4771d610a'
down_revision: Union[str, None] = None  # Ahora no dará error
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Eliminar los tipos ENUM si ya existen
    op.execute("DROP TYPE IF EXISTS goalenum")
    op.execute("DROP TYPE IF EXISTS activitylevelenum")
    op.execute("DROP TYPE IF EXISTS healthconditionenum") 

    # Crear los tipos ENUM
    op.execute("CREATE TYPE goalenum AS ENUM ('lose_weight', 'gain_muscle', 'health_maintenance')")
    op.execute("CREATE TYPE activitylevelenum AS ENUM ('sedentary', 'light_activity', 'moderate_activity', 'intense_activity')")
    op.execute("CREATE TYPE healthconditionenum AS ENUM ('diabetes', 'hypertension', 'kidney_disease')")

    # Modificar las columnas para usar los tipos ENUM con la conversión explícita de los datos
    op.execute("""
        UPDATE users 
        SET physical_activity_level = 
            CASE 
                WHEN physical_activity_level = 1 THEN 'sedentary'::activitylevelenum
                WHEN physical_activity_level = 2 THEN 'light_activity'::activitylevelenum
                WHEN physical_activity_level = 3 THEN 'moderate_activity'::activitylevelenum
                WHEN physical_activity_level = 4 THEN 'intense_activity'::activitylevelenum
                ELSE 'sedentary'::activitylevelenum -- Valor por defecto
            END
    """)

    # Luego, realizar el cambio de tipo
    op.alter_column('users', 'goal',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
                    existing_nullable=False,
                    postgresql_using="goal::goalenum")

    op.alter_column('users', 'physical_activity_level',
                    type_=sa.Enum('sedentary', 'light_activity', 'moderate_activity', 'intense_activity', name='activitylevelenum'),
                    existing_type=sa.Integer(),
                    nullable=False,
                    postgresql_using="physical_activity_level::activitylevelenum")

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
                    existing_type=sa.Enum('sedentary', 'light_activity', 'moderate_activity', 'intense_activity', name='activitylevelenum'),
                    type_=sa.INTEGER(),
                    existing_nullable=False)
    op.alter_column('users', 'goal',
                    existing_type=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
                    type_=sa.VARCHAR(length=50),
                    existing_nullable=False)
