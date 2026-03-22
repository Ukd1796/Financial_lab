# app/core/database.py

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    # fallback for local dev — override via .env in production
    "postgresql://postgres.wtvtoiecnqcgodjohrdc:179683%40KiranUday@aws-1-ap-south-1.pooler.supabase.com:5432/postgres",
)

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
