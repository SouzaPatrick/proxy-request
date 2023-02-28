import os

from app.database import create_db_and_tables
from app.db_functions import populate_db

# Remove SQLite DB
sqlite_db: str = "database.db"
# If file exists, delete it.
if os.path.isfile(sqlite_db):
    os.remove(sqlite_db)

# Create DB
create_db_and_tables()

# Populate DB
populate_db()


print("DB successfully reset")
