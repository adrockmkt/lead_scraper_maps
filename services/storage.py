import sqlite3
import os
from typing import Dict, Optional
from datetime import datetime
from config import OUTPUT_LEADS_QUALIFICADOS, OUTPUT_LEADS_SEM_EMAIL, OUTPUT_LEADS_DESCARTADOS

# ======================================================
# STORAGE / CACHE (SQLITE)
# ======================================================

class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    # --------------------------------------------------
    # INIT DB
    # --------------------------------------------------
    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabela principal de leads
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    place_id TEXT UNIQUE,
                    nome TEXT,
                    site TEXT,
                    email TEXT,
                    status TEXT,
                    score INTEGER,
                    nicho TEXT,
                    cidade TEXT,
                    bairro TEXT,
                    created_at TEXT
                )
            """)

            # Cache de sites já crawleados
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crawled_sites (
                    site TEXT PRIMARY KEY,
                    last_crawled TEXT
                )
            """)

            conn.commit()

    # --------------------------------------------------
    # CHECKS
    # --------------------------------------------------
    def lead_exists(self, place_id: Optional[str]) -> bool:
        if not place_id:
            return False

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM leads WHERE place_id = ? LIMIT 1",
                (place_id,)
            )
            return cursor.fetchone() is not None

    def site_crawled(self, site: Optional[str]) -> bool:
        if not site:
            return False

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM crawled_sites WHERE site = ? LIMIT 1",
                (site,)
            )
            return cursor.fetchone() is not None

    # --------------------------------------------------
    # SAVE CRAWLED SITE
    # --------------------------------------------------
    def mark_site_crawled(self, site: str):
        if not site:
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO crawled_sites (site, last_crawled)
                VALUES (?, ?)
                """,
                (site, datetime.utcnow().isoformat())
            )
            conn.commit()

    # --------------------------------------------------
    # SAVE LEAD
    # --------------------------------------------------
    def save_lead(self, lead: Dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR IGNORE INTO leads (
                    place_id,
                    nome,
                    site,
                    email,
                    status,
                    score,
                    nicho,
                    cidade,
                    bairro,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    lead.get("place_id"),
                    lead.get("nome"),
                    lead.get("email_site"),
                    lead.get("email_corporativo"),
                    lead.get("status"),
                    lead.get("score_valor"),
                    lead.get("nicho"),
                    lead.get("cidade"),
                    lead.get("bairro"),
                    datetime.utcnow().isoformat()
                )
            )
            conn.commit()

    # --------------------------------------------------
    # EXPORT CSV (APPEND SAFE)
    # --------------------------------------------------
    def export_csv(self, lead: Dict):
        status = lead.get("status")

        if status == "qualificado":
            path = OUTPUT_LEADS_QUALIFICADOS
        elif status == "sem_email":
            path = OUTPUT_LEADS_SEM_EMAIL
        else:
            path = OUTPUT_LEADS_DESCARTADOS

        header = [
            "nome",
            "site",
            "email",
            "telefone",
            "cidade",
            "bairro",
            "nicho",
            "score_valor",
            "status"
        ]

        exists = os.path.isfile(path)

        def sanitize(value):
            if value is None:
                return ""
            return str(value).replace('"', '').replace("\n", " ").strip()

        with open(path, "a", encoding="utf-8") as f:
            if not exists:
                f.write(",".join(header) + "\n")

            row = [
                sanitize(lead.get("nome")),
                sanitize(lead.get("site")),
                sanitize(lead.get("email_corporativo")),
                sanitize(lead.get("telefone")),
                sanitize(lead.get("cidade")),
                sanitize(lead.get("bairro")),
                sanitize(lead.get("nicho")),
                sanitize(lead.get("score_valor")),
                sanitize(lead.get("status"))
            ]

            f.write(",".join(f'"{v}"' for v in row) + "\n")