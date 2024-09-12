from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

from .base_class import Base

engine = create_engine(
    settings.assemble_db_connection(),
    pool_pre_ping=True,
    pool_size=500,
    max_overflow=100,
    pool_recycle=60 * 60,
    pool_timeout=30,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)
