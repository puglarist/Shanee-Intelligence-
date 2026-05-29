"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-05-29 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create world type enum
    world_type_enum = postgresql.ENUM("normal", "stronghold", name="worldtype")
    world_type_enum.create(op.get_bind(), checkfirst=True)

    # Create government type enum
    govt_type_enum = postgresql.ENUM(
        "monarchy",
        "democracy",
        "theocracy",
        "oligarchy",
        "autocracy",
        "federation",
        "confederacy",
        "anarchy",
        name="governmenttype",
    )
    govt_type_enum.create(op.get_bind(), checkfirst=True)

    # Create worlds table
    op.create_table(
        "worlds",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("world_type", world_type_enum, nullable=False, server_default="normal"),
        sa.Column("seed", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("last_simulated", sa.DateTime(), nullable=True),
        sa.Column("generation_params", sa.JSON(), nullable=False),
        sa.Column("generation_status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("num_planets", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("num_civilizations", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("num_locations", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create planets table
    op.create_table(
        "planets",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("world_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("terrain_type", sa.String(length=50), nullable=False),
        sa.Column("radius", sa.Float(), nullable=False),
        sa.Column("gravity", sa.Float(), nullable=False),
        sa.Column("temperature_avg", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Float(), nullable=False),
        sa.Column("oxygen_level", sa.Float(), nullable=False),
        sa.Column("biomes", sa.JSON(), nullable=False),
        sa.Column("resources", sa.JSON(), nullable=False),
        sa.Column("habitable", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["world_id"], ["worlds.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_planets_world_id"), "planets", ["world_id"], unique=False)

    # Create civilizations table
    op.create_table(
        "civilizations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("world_id", sa.String(), nullable=False),
        sa.Column("planet_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("government_type", govt_type_enum, nullable=False),
        sa.Column("stability", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("population", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("population_growth_rate", sa.Float(), nullable=False, server_default="0.02"),
        sa.Column("wealth", sa.Float(), nullable=False, server_default="1000"),
        sa.Column("economic_output", sa.Float(), nullable=False, server_default="100"),
        sa.Column("trade_routes", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("culture_description", sa.Text(), nullable=True),
        sa.Column("values", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("technology_level", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("founding_year", sa.Integer(), nullable=True),
        sa.Column("history", sa.Text(), nullable=True),
        sa.Column("conflicts", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], ),
        sa.ForeignKeyConstraint(["world_id"], ["worlds.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_civilizations_planet_id"), "civilizations", ["planet_id"], unique=False)
    op.create_index(op.f("ix_civilizations_world_id"), "civilizations", ["world_id"], unique=False)

    # Create locations table
    op.create_table(
        "locations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("world_id", sa.String(), nullable=False),
        sa.Column("planet_id", sa.String(), nullable=True),
        sa.Column("civilization_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("location_type", sa.String(length=50), nullable=False),
        sa.Column("coordinates", sa.JSON(), nullable=False),
        sa.Column("elevation", sa.Float(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("districts", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("landmarks", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("population", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("governance", sa.String(length=50), nullable=True),
        sa.Column("discovered", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["civilization_id"], ["civilizations.id"], ),
        sa.ForeignKeyConstraint(["planet_id"], ["planets.id"], ),
        sa.ForeignKeyConstraint(["world_id"], ["worlds.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_locations_civilization_id"), "locations", ["civilization_id"], unique=False)
    op.create_index(op.f("ix_locations_planet_id"), "locations", ["planet_id"], unique=False)
    op.create_index(op.f("ix_locations_world_id"), "locations", ["world_id"], unique=False)

    # Create NPCs table
    op.create_table(
        "npcs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("civilization_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("personality_traits", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("motivations", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("beliefs", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("relationships", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("role", sa.String(length=100), nullable=True),
        sa.Column("faction", sa.String(length=100), nullable=True),
        sa.Column("dialogue_topics", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("known_locations", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["civilization_id"], ["civilizations.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_npcs_civilization_id"), "npcs", ["civilization_id"], unique=False)

    # Create events table
    op.create_table(
        "events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("world_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("severity", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("world_year", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("consequences", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("affected_entities", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("generated_by_agent", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(["world_id"], ["worlds.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_world_id"), "events", ["world_id"], unique=False)

    # Create agent_memories table
    op.create_table(
        "agent_memories",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("world_id", sa.String(), nullable=False),
        sa.Column("agent_id", sa.String(), nullable=False),
        sa.Column("memory_type", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", sa.JSON(), nullable=True),
        sa.Column("context", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("importance", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("accessed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["world_id"], ["worlds.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_memories_world_id"), "agent_memories", ["world_id"], unique=False)
    op.create_index(op.f("ix_agent_memories_agent_id"), "agent_memories", ["agent_id"], unique=False)

    # Create stronghold_state table
    op.create_table(
        "stronghold_state",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("world_id", sa.String(), nullable=False),
        sa.Column("defense_level", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("resource_reserves", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("healing_system_active", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("backup_system_active", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("ai_governance_policy", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("access_control", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("districts_status", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("last_backup", sa.DateTime(), nullable=True),
        sa.Column("last_integrity_check", sa.DateTime(), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["world_id"], ["worlds.id"], ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table("stronghold_state")
    op.drop_index(op.f("ix_agent_memories_agent_id"), table_name="agent_memories")
    op.drop_index(op.f("ix_agent_memories_world_id"), table_name="agent_memories")
    op.drop_table("agent_memories")
    op.drop_index(op.f("ix_events_world_id"), table_name="events")
    op.drop_table("events")
    op.drop_index(op.f("ix_npcs_civilization_id"), table_name="npcs")
    op.drop_table("npcs")
    op.drop_index(op.f("ix_locations_world_id"), table_name="locations")
    op.drop_index(op.f("ix_locations_planet_id"), table_name="locations")
    op.drop_index(op.f("ix_locations_civilization_id"), table_name="locations")
    op.drop_table("locations")
    op.drop_index(op.f("ix_civilizations_world_id"), table_name="civilizations")
    op.drop_index(op.f("ix_civilizations_planet_id"), table_name="civilizations")
    op.drop_table("civilizations")
    op.drop_index(op.f("ix_planets_world_id"), table_name="planets")
    op.drop_table("planets")
    op.drop_table("worlds")

    # Drop enums
    postgresql.ENUM("worldtype").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM("governmenttype").drop(op.get_bind(), checkfirst=True)
