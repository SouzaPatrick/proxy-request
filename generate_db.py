import os

from app.models import ExtractionMethod, Protocol
from database import create_db_and_tables, get_session

# Remove SQLite DB
sqlite_db: str = "database.db"
# If file exists, delete it.
if os.path.isfile(sqlite_db):
    print("Remove DB")
    os.remove(sqlite_db)

# Create DB
create_db_and_tables()

# Populate DB
with get_session() as session:
    Protocol._populate_db(session)
    ExtractionMethod._populate_db(session)

print("DB successfully reset")
