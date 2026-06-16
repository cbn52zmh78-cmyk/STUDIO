#!/usr/bin/env python3
"""
Visual Asset Catalog v1.1 — Director | Idea 2
Lightweight local SQLite catalog for images + prompts.
Search, tag, version, and export prompt packs for video sequences.
Upserts by normalized file_path to prevent duplicate rows.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

import sys

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from magazine_paths import CATALOG_DIR, MAGAZINE_ROOT, SHOT_LISTS_DIR

DB_PATH = CATALOG_DIR / "visual_assets.db"


class VisualAssetCatalog:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        print(f"✅ Catalog ready: {self.db_path}")

    @staticmethod
    def _normalize_path(file_path: str) -> str:
        if not file_path:
            return ""
        return str(Path(file_path).resolve())

    def _init_db(self):
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_type TEXT,
                model_name TEXT,
                scene TEXT,
                tags TEXT,
                version TEXT,
                file_path TEXT,
                prompt_text TEXT,
                metadata TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """
        )
        self._migrate(c)
        self.conn.commit()

    def _migrate(self, c: sqlite3.Cursor) -> None:
        cols = {row[1] for row in c.execute("PRAGMA table_info(assets)")}
        if "updated_at" not in cols:
            c.execute("ALTER TABLE assets ADD COLUMN updated_at TEXT")

        # Remove legacy duplicates (keep newest row per file_path)
        c.execute(
            """
            DELETE FROM assets
            WHERE file_path IS NOT NULL
              AND file_path != ''
              AND id NOT IN (
                SELECT MAX(id)
                FROM assets
                WHERE file_path IS NOT NULL AND file_path != ''
                GROUP BY file_path
              )
            """
        )
        c.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_assets_file_path
            ON assets(file_path)
            WHERE file_path IS NOT NULL AND file_path != ''
            """
        )

    def add_asset(
        self,
        asset_type: str,
        model_name: str,
        scene: str,
        tags: list,
        version: str,
        file_path: str,
        prompt_text: str = "",
        metadata: dict | None = None,
    ) -> str:
        """Insert or update by file_path. Returns: added | updated | skipped."""
        norm_path = self._normalize_path(file_path)
        if not norm_path:
            raise ValueError("file_path is required for catalog deduplication")

        now = datetime.now().isoformat()
        meta_json = json.dumps(metadata or {}, sort_keys=True)
        tags_csv = ",".join(tags)

        c = self.conn.cursor()
        existing = c.execute(
            "SELECT prompt_text, metadata, tags, version FROM assets WHERE file_path = ?",
            (norm_path,),
        ).fetchone()

        if existing:
            unchanged = (
                existing[0] == prompt_text
                and existing[1] == meta_json
                and existing[2] == tags_csv
                and existing[3] == version
            )
            if unchanged:
                return "skipped"

            c.execute(
                """
                UPDATE assets
                SET asset_type = ?, model_name = ?, scene = ?, tags = ?, version = ?,
                    prompt_text = ?, metadata = ?, updated_at = ?
                WHERE file_path = ?
                """,
                (
                    asset_type,
                    model_name,
                    scene,
                    tags_csv,
                    version,
                    prompt_text,
                    meta_json,
                    now,
                    norm_path,
                ),
            )
            self.conn.commit()
            return "updated"

        c.execute(
            """
            INSERT INTO assets (
                asset_type, model_name, scene, tags, version, file_path,
                prompt_text, metadata, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_type,
                model_name,
                scene,
                tags_csv,
                version,
                norm_path,
                prompt_text,
                meta_json,
                now,
                now,
            ),
        )
        self.conn.commit()
        return "added"

    def ingest_shotlist_dir(
        self,
        seq_path: Path,
        model_name: str,
        scene: str,
        tags: list[str],
        version: str = "1.0",
    ) -> dict[str, int]:
        """Ingest .txt shot prompts from a shot-list folder. Upserts by file path."""
        counts = {"added": 0, "updated": 0, "skipped": 0}
        for fname in sorted(seq_path.iterdir()):
            if fname.suffix != ".txt" or fname.name.startswith("_"):
                continue
            content = fname.read_text(encoding="utf-8")
            prompt = content.split("\n\n")[-1].strip()
            result = self.add_asset(
                asset_type="prompt",
                model_name=model_name,
                scene=scene,
                tags=tags,
                version=version,
                file_path=str(fname),
                prompt_text=prompt,
                metadata={"shot": fname.stem, "sequence": seq_path.name},
            )
            counts[result] += 1
        return counts

    def search(
        self,
        model_name: str | None = None,
        tags: list | None = None,
        scene: str | None = None,
    ):
        c = self.conn.cursor()
        query = "SELECT * FROM assets WHERE 1=1"
        params: list[str] = []
        if model_name:
            query += " AND model_name = ?"
            params.append(model_name)
        if scene:
            query += " AND scene LIKE ?"
            params.append(f"%{scene}%")
        if tags:
            for tag in tags:
                query += " AND tags LIKE ?"
                params.append(f"%{tag}%")
        query += " ORDER BY model_name, scene, file_path"
        c.execute(query, params)
        return c.fetchall()

    def count(self, model_name: str | None = None) -> int:
        c = self.conn.cursor()
        if model_name:
            return c.execute(
                "SELECT COUNT(*) FROM assets WHERE model_name = ?", (model_name,)
            ).fetchone()[0]
        return c.execute("SELECT COUNT(*) FROM assets").fetchone()[0]

    def export_prompt_pack(self, model_name: str, output_file: Path | str):
        results = self.search(model_name=model_name, tags=None, scene=None)
        pack = {
            "exported_at": datetime.now().isoformat(),
            "model": model_name,
            "count": len(results),
            "prompts": [],
        }
        for row in results:
            pack["prompts"].append(
                {
                    "id": row[0],
                    "scene": row[3],
                    "tags": row[4],
                    "version": row[5],
                    "file_path": row[6],
                    "prompt": row[7],
                }
            )
        out = Path(output_file)
        out.write_text(json.dumps(pack, indent=2), encoding="utf-8")
        print(f"✅ Exported {len(results)} prompts → {out}")

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    cat = VisualAssetCatalog()

    if SHOT_LISTS_DIR.exists():
        valentina_folders = sorted(
            f for f in SHOT_LISTS_DIR.iterdir() if f.is_dir() and "Valentina_Rossi" in f.name
        )
        if valentina_folders:
            latest = valentina_folders[-1]
            print(f"Ingesting demo sequence: {latest.name}")
            counts = cat.ingest_shotlist_dir(
                latest,
                model_name="Valentina Rossi",
                scene="Sculptural_Black_Coat_Editorial",
                tags=["supermodel", "editorial", "16:9", "single-subject", "avant-garde"],
            )
            print(
                f"   added={counts['added']} updated={counts['updated']} "
                f"skipped={counts['skipped']}"
            )

    total = cat.count(model_name="Valentina Rossi")
    print(f"\n--- Valentina assets in catalog: {total} ---")
    for row in cat.search(model_name="Valentina Rossi")[:3]:
        print(f"  {row[3]} | {row[4]} | {Path(row[6]).name}")

    cat.export_prompt_pack(
        "Valentina Rossi",
        CATALOG_DIR / "Valentina_Prompt_Pack.json",
    )
    cat.close()
    print("\nCatalog demo complete. Re-runs upsert — no duplicate rows.")