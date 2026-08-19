from sqlalchemy.orm import sessionmaker

from backend.app.database.connection import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)