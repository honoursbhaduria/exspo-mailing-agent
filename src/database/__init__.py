"""
Database package for EDXSO Micro-Influencer Platform.
Supports Neon PostgreSQL with automatic fallback to high-performance local SQLite.
"""
from src.database.db import (
    get_db,
    init_db,
    get_db_status,
    upsert_many,
    upsert_influencer,
    get_influencers_from_db,
    filter_influencers_pipeline
)

__all__ = [
    "get_db",
    "init_db",
    "get_db_status",
    "upsert_many",
    "upsert_influencer",
    "get_influencers_from_db",
    "filter_influencers_pipeline"
]
