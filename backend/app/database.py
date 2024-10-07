from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#environment set up
postgres_path = "postgresql://user:password@localhost:5432/TetorDB"

#initialise postgreSQL connection
engine = create_engine(postgres_path)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def init_postgres():
    postgres_db = SessionLocal()
    try:
        yield postgres_db
    finally:
        postgres_db.close()
    
