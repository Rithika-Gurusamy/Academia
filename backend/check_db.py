from database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables: {tables}")

for table in tables:
    columns = inspector.get_columns(table)
    print(f"Table: {table}")
    for column in columns:
        print(f"  Column: {column['name']} ({column['type']})")
