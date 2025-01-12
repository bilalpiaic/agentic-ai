from sqlmodel import SQLModel, create_engine
import os

connection_string = os.getenv('DB_URI')
print(connection_string)
engine = create_engine(connection_string)

def create_tables():
    SQLModel.metadata.create_all(engine)