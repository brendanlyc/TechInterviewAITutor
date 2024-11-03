from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models.learning_path_content import LearningPathContent
from .models.diagnostic_test import DiagnosticTest
from .models.diagnostic_test_results import DiagnosticTestResult
from .models.user_concept_mastery import UserConceptMastery


#environment set up
postgres_path = "postgresql://user:password@postgres:5432/TetorDB"
mongodb_path = "mongodb://mongodb:27017/"

#initialise postgreSQL connection
engine = create_engine(postgres_path)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

PostgresBase = declarative_base()

def init_postgres():
    postgres_db = SessionLocal()
    try:
        yield postgres_db
    finally:
        postgres_db.close()
    
async def init_mongodb():
    client = AsyncIOMotorClient(mongodb_path)
    await init_beanie(database=client.tetordb,document_models=[LearningPathContent, DiagnosticTest, DiagnosticTestResult, UserConceptMastery])
