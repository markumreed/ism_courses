"""What happens when the app's code runs from the wrong folder (reference only)."""

import shutil
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "bayside_app"


def test_create_tables_from_another_folder_names_schema_sql(tmp_path, monkeypatch):
    shutil.copy(APP / "database.py", tmp_path / "database.py")
    monkeypatch.syspath_prepend(str(tmp_path))
    sys.modules.pop("database", None)
    import database

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    try:
        database.create_tables("bayside.db")
    except FileNotFoundError as error:
        assert "schema.sql" in str(error)
    else:
        raise AssertionError("create_tables should fail without schema.sql")
