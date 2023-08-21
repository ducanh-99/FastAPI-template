# Lead management migration for python

- `cp .env.example .env`
- `alembic revision -m "this is a new model" --autogenerate`   # Create migration versions depend on changed in models
- `alembic upgrade head`   # Upgrade to last version migration
- `alembic downgrade -1`   # Downgrade to before version migration
