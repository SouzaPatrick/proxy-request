import os

from app.db_functions import populate_extraction_method, populate_protocol
from database import create_db_and_tables

# Remove SQLite DB
sqlite_db: str = "database.db"
# If file exists, delete it.
if os.path.isfile(sqlite_db):
    print("Remove DB")
    os.remove(sqlite_db)

# Create DB
create_db_and_tables()

# Populate DB
populate_protocol()
populate_extraction_method()

print("DB successfully reset")
