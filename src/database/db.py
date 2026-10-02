import os
import sqlite3
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from config.settings import (
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    MIN_FOLLOWERS,
    MAX_FOLLOWERS,
    MIN_ENGAGEMENT_RATE,
    DEFAULT_NICHE
)
from src.filtering.classifier import InfluencerClassifier
from src.enrichment.enricher import ProfileEnricher

DB_PATH = DATA_DIR / "edxso.db"

# Optional PostgreSQL driver for Neon database
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor, execute_values
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


def _get_database_url() -> Optional[str]:
    """Retrieves Neon / PostgreSQL connection string from environment if defined."""
    return os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL")


class DatabaseManager:
    """
    Manages connections and transactions for the influencer repository.
    Supports Neon PostgreSQL cloud database with seamless local SQLite fallback.
    """
    def __init__(self):
        self.db_url = _get_database_url()
        self.is_postgres = False
        self._check_connection()

    def _check_connection(self):
        if self.db_url and PSYCOPG2_AVAILABLE:
            url = self.db_url
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            try:
                conn = psycopg2.connect(url, connect_timeout=5)
                conn.close()
                self.is_postgres = True
                self.db_url = url
                print("DatabaseManager: Connected successfully to Neon PostgreSQL cluster.")
                return
            except Exception as e:
                print(f"DatabaseManager: Neon PostgreSQL connection failed ({e}). Falling back to local SQLite.")
                self.is_postgres = False
        else:
            self.is_postgres = False

    def get_connection(self):
        if self.is_postgres and self.db_url:
            return psycopg2.connect(self.db_url)
        else:
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            return conn

    def init_schema(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if self.is_postgres:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS influencers (
                    handle VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    platform VARCHAR(100) DEFAULT 'Instagram',
                    profile_url TEXT,
                    follower_str VARCHAR(50),
                    niche VARCHAR(100),
                    location VARCHAR(255),
                    price VARCHAR(50),
                    rating DOUBLE PRECISION DEFAULT 4.8,
                    content_themes TEXT,
                    contact_email VARCHAR(255),
                    bio TEXT,
                    instagram_url TEXT,
                    tiktok_url TEXT,
                    youtube_url TEXT,
                    follower_count INTEGER DEFAULT 0,
                    engagement_rate DOUBLE PRECISION DEFAULT 2.0,
                    audience_geography VARCHAR(255),
                    audience_age VARCHAR(50),
                    audience_gender VARCHAR(50),
                    qualification_status VARCHAR(50),
                    qualification_reason TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_inf_niche ON influencers (niche);
                CREATE INDEX IF NOT EXISTS idx_inf_platform ON influencers (platform);
                CREATE INDEX IF NOT EXISTS idx_inf_followers ON influencers (follower_count);
                CREATE INDEX IF NOT EXISTS idx_inf_engagement ON influencers (engagement_rate);
                CREATE INDEX IF NOT EXISTS idx_inf_geography ON influencers (audience_geography);
                CREATE INDEX IF NOT EXISTS idx_inf_location ON influencers (location);
                """
            else:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS influencers (
                    handle TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    platform TEXT DEFAULT 'Instagram',
                    profile_url TEXT,
                    follower_str TEXT,
                    niche TEXT,
                    location TEXT,
                    price TEXT,
                    rating REAL DEFAULT 4.8,
                    content_themes TEXT,
                    contact_email TEXT,
                    bio TEXT,
                    instagram_url TEXT,
                    tiktok_url TEXT,
                    youtube_url TEXT,
                    follower_count INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 2.0,
                    audience_geography TEXT,
                    audience_age TEXT,
                    audience_gender TEXT,
                    qualification_status TEXT,
                    qualification_reason TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_inf_niche ON influencers (niche);
                CREATE INDEX IF NOT EXISTS idx_inf_platform ON influencers (platform);
                CREATE INDEX IF NOT EXISTS idx_inf_followers ON influencers (follower_count);
                CREATE INDEX IF NOT EXISTS idx_inf_engagement ON influencers (engagement_rate);
                CREATE INDEX IF NOT EXISTS idx_inf_geography ON influencers (audience_geography);
                CREATE INDEX IF NOT EXISTS idx_inf_location ON influencers (location);
                """
            
            if self.is_postgres:
                cursor.execute(create_table_sql)
            else:
                cursor.executescript(create_table_sql)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def sync_from_csv(self, force: bool = False):
        """
        Seeds the database from CSV files if empty or force=True.
        Enriches records with audience demographics and classification.
        """
        count = self.get_count()
        if count > 0 and not force:
            return count

        base_dfs = []
        seed_path = DATA_DIR / "influencers_seed.csv"
        if seed_path.exists():
            try:
                base_dfs.append(pd.read_csv(seed_path))
            except Exception:
                pass
        if RAW_DATA_PATH.exists():
            try:
                base_dfs.append(pd.read_csv(RAW_DATA_PATH))
            except Exception:
                pass

        if not base_dfs:
            return 0

        raw_df = pd.concat(base_dfs).drop_duplicates(subset=["handle"], keep="first")
        enricher = ProfileEnricher()
        enriched_df = enricher.enrich_dataset(raw_df)

        classifier = InfluencerClassifier()
        processed_df = classifier.process_dataset(enriched_df).fillna("")

        records = processed_df.to_dict(orient="records")
        return self.upsert_many(records)

    def get_count(self) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM influencers;")
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            cursor.close()
            conn.close()

    def upsert_many(self, records: List[Dict[str, Any]]) -> int:
        if not records:
            return 0

        conn = self.get_connection()
        cursor = conn.cursor()
        cols = [
            "handle", "name", "platform", "profile_url", "follower_str",
            "niche", "location", "price", "rating", "content_themes",
            "contact_email", "bio", "instagram_url", "tiktok_url", "youtube_url",
            "follower_count", "engagement_rate", "audience_geography",
            "audience_age", "audience_gender", "qualification_status",
            "qualification_reason"
        ]

        try:
            if self.is_postgres:
                col_names = ", ".join(cols)
                update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in cols if col != "handle"])
                sql = f"""
                INSERT INTO influencers ({col_names})
                VALUES %s
                ON CONFLICT (handle) DO UPDATE SET {update_set}, updated_at = CURRENT_TIMESTAMP;
                """
                def _clean_val(c, val):
                    if c == "follower_count":
                        try:
                            return int(val) if val not in ("", None) and not pd.isna(val) else 0
                        except (ValueError, TypeError):
                            return 0
                    elif c in ("engagement_rate", "rating"):
                        try:
                            return float(val) if val not in ("", None) and not pd.isna(val) else (4.8 if c == "rating" else 2.0)
                        except (ValueError, TypeError):
                            return 4.8 if c == "rating" else 2.0
                    else:
                        if val is None or pd.isna(val):
                            return ""
                        return str(val)

                tuples = [
                    tuple(_clean_val(c, r.get(c)) for c in cols)
                    for r in records
                ]
                execute_values(cursor, sql, tuples, page_size=1000)
            else:
                col_names = ", ".join(cols)
                placeholders = ", ".join(["?"] * len(cols))
                update_set = ", ".join([f"{col} = excluded.{col}" for col in cols if col != "handle"])
                sql = f"""
                INSERT INTO influencers ({col_names})
                VALUES ({placeholders})
                ON CONFLICT(handle) DO UPDATE SET {update_set}, updated_at = CURRENT_TIMESTAMP;
                """
                def _clean_val(c, val):
                    if c == "follower_count":
                        try:
                            return int(val) if val not in ("", None) and not pd.isna(val) else 0
                        except (ValueError, TypeError):
                            return 0
                    elif c in ("engagement_rate", "rating"):
                        try:
                            return float(val) if val not in ("", None) and not pd.isna(val) else (4.8 if c == "rating" else 2.0)
                        except (ValueError, TypeError):
                            return 4.8 if c == "rating" else 2.0
                    else:
                        if val is None or pd.isna(val):
                            return ""
                        return str(val)

                tuples = [
                    tuple(_clean_val(c, r.get(c)) for c in cols)
                    for r in records
                ]
                cursor.executemany(sql, tuples)

            conn.commit()
            return len(records)
        finally:
            cursor.close()
            conn.close()

    def upsert_influencer(self, record: Dict[str, Any]) -> bool:
        return self.upsert_many([record]) > 0

    def get_status(self) -> Dict[str, Any]:
        count = self.get_count()
        return {
            "engine": "Neon PostgreSQL" if self.is_postgres else "SQLite (Local Indexed)",
            "is_postgres": self.is_postgres,
            "connected": True,
            "total_records": count,
            "database_url_configured": bool(self.db_url),
            "storage_target": "Neon Cloud Cluster" if self.is_postgres else str(DB_PATH)
        }

    def get_influencers(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sql = "SELECT * FROM influencers"
            params: List[Any] = []
            if search_query:
                q = f"%{search_query.strip().lower()}%"
                sql += " WHERE LOWER(name) LIKE ? OR LOWER(handle) LIKE ? OR LOWER(location) LIKE ? OR LOWER(niche) LIKE ?"
                params.extend([q, q, q, q])
                if self.is_postgres:
                    sql = sql.replace("?", "%s")
            
            sql += " ORDER BY follower_count DESC"
            if limit is not None:
                sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"

            if self.is_postgres:
                cursor.execute(sql, tuple(params))
                desc = [d[0] for d in cursor.description]
                rows = [dict(zip(desc, row)) for row in cursor.fetchall()]
            else:
                cursor.execute(sql, tuple(params))
                rows = [dict(row) for row in cursor.fetchall()]
            return rows
        finally:
            cursor.close()
            conn.close()


_DB_MANAGER: Optional[DatabaseManager] = None

def get_db() -> DatabaseManager:
    global _DB_MANAGER
    if _DB_MANAGER is None:
        _DB_MANAGER = DatabaseManager()
        _DB_MANAGER.init_schema()
        _DB_MANAGER.sync_from_csv()
    return _DB_MANAGER

def init_db() -> DatabaseManager:
    return get_db()

def get_db_status() -> Dict[str, Any]:
    return get_db().get_status()

def upsert_many(records: List[Dict[str, Any]]) -> int:
    return get_db().upsert_many(records)

def upsert_influencer(record: Dict[str, Any]) -> bool:
    return get_db().upsert_influencer(record)

def get_influencers_from_db(
    limit: Optional[int] = None,
    offset: int = 0,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    return get_db().get_influencers(limit=limit, offset=offset, search_query=search)

def filter_influencers_pipeline(
    min_followers: int = MIN_FOLLOWERS,
    max_followers: int = MAX_FOLLOWERS,
    min_engagement: float = MIN_ENGAGEMENT_RATE,
    target_niche: str = DEFAULT_NICHE,
    target_geography: str = "Global (All Regions)",
    target_platform: str = "All Platforms",
    search_query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes the multi-dimensional classification engine against all indexed influencers.
    Returns evaluated dataset, passed count, failed count, and separate subsets.
    """
    db = get_db()
    all_creators = db.get_influencers(limit=None, offset=0, search_query=search_query)
    
    if not all_creators:
        # Fallback to sync from CSV if empty
        db.sync_from_csv(force=True)
        all_creators = db.get_influencers(limit=None, offset=0, search_query=search_query)

    classifier = InfluencerClassifier(
        min_followers=min_followers,
        max_followers=max_followers,
        min_engagement=min_engagement,
        target_niche=target_niche,
        target_geography=target_geography,
        target_platform=target_platform
    )

    df = pd.DataFrame(all_creators)
    processed_df = classifier.process_dataset(df).fillna("")

    passed_df = processed_df[processed_df["qualification_status"] == "PASSED"]
    failed_df = processed_df[processed_df["qualification_status"] == "FAILED"]

    return {
        "total": len(processed_df),
        "total_evaluated": len(processed_df),
        "passed_count": len(passed_df),
        "failed_count": len(failed_df),
        "target_geography": target_geography,
        "target_platform": target_platform,
        "target_niche": target_niche,
        "results": processed_df.to_dict(orient="records"),
        "passed_influencers": passed_df.to_dict(orient="records"),
        "failed_influencers": failed_df.to_dict(orient="records")
    }
