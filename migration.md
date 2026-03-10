# Database Migrations Guide (FastAPI + SQLAlchemy + Alembic)

This document explains **database migrations from scratch** and how to
use **Alembic** properly in a FastAPI project.

The goal is to help you:

-   Understand what migrations are
-   Understand why they are important
-   Set up Alembic correctly
-   Create and apply migrations safely
-   Avoid common mistakes

This guide assumes you are using:

-   FastAPI
-   SQLAlchemy
-   PostgreSQL
-   Virtual Environment (venv)

------------------------------------------------------------------------

# 1. What is a Database Migration?

A **migration** is a controlled way to update your database schema.

Example schema changes:

-   Adding a column
-   Removing a column
-   Creating a new table
-   Changing column types
-   Adding indexes
-   Adding constraints

Instead of manually editing the database, we create **migration
scripts** that modify the database safely.

Example:

Before:

    organizations
    id
    name
    created_at

After migration:

    organizations
    id
    name
    created_at
    deleted_at

------------------------------------------------------------------------

# 2. Why Migrations Are Important

Without migrations:

| Problem | Explanation |
|--------|--------|
| Schema mismatch differ | Code and DB structure may |
|  Team collaboration different | Everyone's DB becomes  |
| Production deployment   | Dangerous manual updates |
| Rollback impossible    | Hard to revert mistakes |

With migrations:

-   Database schema history is tracked
-   Changes are reproducible
-   Easy rollback
-   Safe deployments

------------------------------------------------------------------------

# 3. Tool Used: Alembic

Alembic is the **official migration tool for SQLAlchemy**.

It helps:

-   Track schema versions
-   Generate migration scripts
-   Apply schema changes safely

------------------------------------------------------------------------

# 4. Install Required Packages

Activate your virtual environment:

    .\venv\Scripts\Activate

Install dependencies:

    pip install alembic
    pip install sqlalchemy
    pip install psycopg2-binary

Verify installation:

    pip show alembic

------------------------------------------------------------------------

# 5. Initialize Alembic

Inside your project root folder:

    python -m alembic init alembic

This creates:

    project/
    │
    ├── alembic/
    │   ├── versions/
    │   ├── env.py
    │   └── script.py.mako
    │
    ├── alembic.ini

Explanation:

  File          Purpose
  ------------- -------------------------------
  alembic.ini   Alembic configuration
  env.py        migration environment setup
  versions/     migration scripts stored here

------------------------------------------------------------------------

# 6. Configure Database Connection

Open:

    alembic.ini

Find:

    sqlalchemy.url = driver://user:pass@localhost/dbname

Replace with your database:

Example:

    sqlalchemy.url = postgresql://postgres:password@localhost:5432/trackify

------------------------------------------------------------------------

# 7. Connect Alembic with SQLAlchemy Models

Open:

    alembic/env.py

Find:

    target_metadata = None

Replace with:

``` python
from app.db.base import Base

target_metadata = Base.metadata
```

This allows Alembic to **detect model changes automatically**.

------------------------------------------------------------------------

# 8. Create First Migration

Whenever models change, generate a migration.

Command:

    python -m alembic revision --autogenerate -m "description"

Example:

    python -m alembic revision --autogenerate -m "add deleted_at to organizations"

This creates a file:

    alembic/versions/xxxxxxxx_add_deleted_at.py

------------------------------------------------------------------------

# 9. Review Migration File (VERY IMPORTANT)

Example migration:

``` python
def upgrade():
    op.add_column(
        "organizations",
        sa.Column("deleted_at", sa.DateTime(), nullable=True)
    )

def downgrade():
    op.drop_column("organizations", "deleted_at")
```

Always review migrations before running them.

Sometimes Alembic generates incorrect operations.

------------------------------------------------------------------------

# 10. Apply Migration

Run:

    python -m alembic upgrade head

Explanation:

| Command | Meaning |
|--------|--------|
| upgrade | apply migrations |
| head | latest migration version |

------------------------------------------------------------------------

# 11. Check Migration History

View migration history:

    python -m alembic history

Check current DB version:

    python -m alembic current

------------------------------------------------------------------------

# 12. Rolling Back Migrations

If something goes wrong you can revert.

Rollback one step:

    python -m alembic downgrade -1

Rollback to base:

    python -m alembic downgrade base

------------------------------------------------------------------------

# 13. Migration Workflow (Best Practice)

Typical development flow:

### Step 1

Modify SQLAlchemy model

### Step 2

Generate migration

    python -m alembic revision --autogenerate -m "describe change"

### Step 3

Review migration script

### Step 4

Apply migration

    python -m alembic upgrade head

------------------------------------------------------------------------

# 14. Example: Adding Soft Delete

Model change:

``` python
deleted_at = Column(DateTime, nullable=True)
```

Generate migration:

    python -m alembic revision --autogenerate -m "add soft delete"

Migration script:

``` python
op.add_column(
    "organizations",
    sa.Column("deleted_at", sa.DateTime(), nullable=True)
)
```

Apply migration:

    python -m alembic upgrade head

------------------------------------------------------------------------

# 15. Common Errors and Fixes

### Error

    column does not exist

Fix:

Run migrations.

------------------------------------------------------------------------

### Error

    alembic not recognized

Fix:

Activate virtual environment.

------------------------------------------------------------------------

### Error

    No script_location key found

Fix:

Run:

    alembic init alembic

------------------------------------------------------------------------

### Error

    cannot drop table because other objects depend on it

Fix:

Review migration file. Remove incorrect `drop_table()` commands.

------------------------------------------------------------------------

# 16. Important Commands Summary

Initialize Alembic

    python -m alembic init alembic

Create migration

    python -m alembic revision --autogenerate -m "message"

Apply migrations

    python -m alembic upgrade head

Rollback migration

    python -m alembic downgrade -1

Check history

    python -m alembic history

Check current version

    python -m alembic current

------------------------------------------------------------------------

# 17. Best Practices

Always:

-   Review migration scripts before running
-   Commit migration files to Git
-   Run migrations in staging before production
-   Never manually change production DB schema

------------------------------------------------------------------------

# 18. Real Production Usage

In production systems:

-   Every schema change goes through migration
-   CI/CD runs migrations automatically
-   Migration files are version controlled

This ensures safe deployments.

------------------------------------------------------------------------

# 19. Final Takeaway

Migrations allow you to:

-   Safely evolve database schema
-   Track database changes
-   Maintain consistency across environments

For any professional backend system, **migration management is
mandatory**.
