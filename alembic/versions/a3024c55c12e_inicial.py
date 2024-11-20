from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a3024c55c12e'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.alter_column('users', 'goal',
                    existing_type=sa.VARCHAR(length=50),
                    type_=sa.Enum('lose_weight', 'gain_muscle', 'health_maintenance', name='goalenum'),
                    existing_nullable=False,
                    postgresql_using='goal::text::goalenum')

    op.alter_column('users', 'physical_activity_level',
                    existing_type=sa.INTEGER(),
                    type_=sa.Enum('low', 'medium', 'high', name='activitylevelenum'),
                    existing_nullable=False,
                    postgresql_using='physical_activity_level::text::activitylevelenum')

    op.alter_column('users', 'health_conditions',
                    existing_type=sa.TEXT(),
                    type_=sa.Enum('diabetes', 'hypertension', 'kidney_disease', name='healthconditionenum'),
                    existing_nullable=True,
                    postgresql_using='health_conditions::text::healthconditionenum')

def downgrade() -> None:
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