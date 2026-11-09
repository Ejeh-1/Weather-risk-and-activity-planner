"""JSON-backed storage for weather searches, favourite locations and activity plans.

No third-party dependencies are required. Data is stored in the project's data/ folder.
"""
from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


class StorageError(Exception):
    """Raised when saved application data cannot be read or written."""


class StorageManager:
    """Manage persistent application data using three local JSON files."""

    def __init__(self, data_dir: Optional[str | Path] = None):
        # managers/storage.py -> project root -> data/
        project_root = Path(__file__).resolve().parent.parent
        self.data_dir = Path(data_dir) if data_dir else project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.data_dir / "search_history.json"
        self.favourites_file = self.data_dir / "favourites.json"
        self.plans_file = self.data_dir / "activity_plans.json"

    @staticmethod
    def _json_default(value: Any) -> Any:
        if is_dataclass(value):
            return asdict(value)
        if isinstance(value, (datetime, date, time)):
            return value.isoformat()
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, Path):
            return str(value)
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if hasattr(value, "__dict__"):
            return {k: v for k, v in vars(value).items() if not k.startswith("_")}
        raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")

    def _read(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError) as exc:
            raise StorageError(f"Could not read {path.name}: {exc}") from exc
        if not isinstance(data, list):
            raise StorageError(f"Invalid format in {path.name}: expected a JSON list.")
        return data

    def _write(self, path: Path, records: List[Dict[str, Any]]) -> None:
        """Write atomically so an interrupted save does not leave half a JSON file."""
        temporary_name = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.data_dir, delete=False
            ) as temporary:
                json.dump(records, temporary, indent=4, ensure_ascii=False, default=self._json_default)
                temporary.write("\n")
                temporary_name = temporary.name
            os.replace(temporary_name, path)
        except (OSError, TypeError, ValueError) as exc:
            if temporary_name and os.path.exists(temporary_name):
                os.remove(temporary_name)
            raise StorageError(f"Could not save {path.name}: {exc}") from exc

    @staticmethod
    def _required_text(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string.")
        return value.strip()

    def save_search(self, location: str, activity: str, search_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Save one completed weather search and return the saved record."""
        location = self._required_text(location, "Location")
        activity = self._required_text(activity, "Activity")
        record = {
            "id": str(uuid4()),
            "location": location,
            "activity": activity,
            "searched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "details": search_data or {},
        }
        records = self._read(self.history_file)
        records.append(record)
        self._write(self.history_file, records)
        return record

    def get_search_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        records = self._read(self.history_file)
        records.reverse()  # newest first
        return records[:limit] if limit is not None else records

    def clear_search_history(self) -> None:
        self._write(self.history_file, [])

    def add_favourite(self, location: str) -> bool:
        """Add a location. Returns False when it is already saved (case-insensitive)."""
        location = self._required_text(location, "Location")
        records = self._read(self.favourites_file)
        if any(item.get("location", "").casefold() == location.casefold() for item in records):
            return False
        records.append({"id": str(uuid4()), "location": location,
                        "added_at": datetime.now().astimezone().isoformat(timespec="seconds")})
        self._write(self.favourites_file, records)
        return True

    def get_favourites(self) -> List[Dict[str, Any]]:
        return self._read(self.favourites_file)

    def remove_favourite(self, location: str) -> bool:

        location = self._required_text(location, "Location")

        records = self._read(self.favourites_file)

        remaining = [

            item for item in records
            if item.get("location", "").casefold() != location.casefold()
        ]
        if len(remaining) == len(records):
            return False
        self._write(self.favourites_file, remaining)
        return True

    

    def save_activity_plan(self, plan: Any) -> Dict[str, Any]:
        """Save a plan dictionary or an ActivityPlan/dataclass instance."""
        if is_dataclass(plan):
            payload = asdict(plan)
        elif isinstance(plan, dict):
            payload = dict(plan)
        elif hasattr(plan, "__dict__"):
            payload = {k: v for k, v in vars(plan).items() if not k.startswith("_")}
        else:
            raise ValueError("Activity plan must be a dictionary or an object with attributes.")
        record = {"id": str(uuid4()),
                  "saved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                  "plan": payload}
        records = self._read(self.plans_file)
        records.append(record)
        self._write(self.plans_file, records)
        return record

    def get_activity_plans(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        records = self._read(self.plans_file)
        records.reverse()
        return records[:limit] if limit is not None else records

    def clear_activity_plans(self) -> None:
        """Clear all saved activity plans."""
        self._write(self.plans_file, [])
