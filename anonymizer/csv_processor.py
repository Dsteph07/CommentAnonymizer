import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from .person_mapper import PersonMapper
from .pii_cleaner import PIICleaner


class CSVAnonymizer:
    ALLOWED_TYPES = {"person", "free_text"}

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.person_mapper = PersonMapper()
        self.pii_cleaner = PIICleaner()

    def _validate_config(self) -> None:
        required_keys = ["input_csv", "output_csv", "columns"]
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

        columns = self.config["columns"]
        if not isinstance(columns, dict):
            raise ValueError("'columns' must be a dictionary of column_name -> anonymization_type")

        for column_name, anonymization_type in columns.items():
            if anonymization_type not in self.ALLOWED_TYPES:
                raise ValueError(
                    f"Unsupported anonymization type for column '{column_name}': "
                    f"'{anonymization_type}'. Allowed: {sorted(self.ALLOWED_TYPES)}"
                )

    def _load_csv(self) -> pd.DataFrame:
        input_csv = self.config["input_csv"]
        encoding = self.config.get("encoding", "utf-8")
        delimiter = self.config.get("delimiter", ",")

        return pd.read_csv(input_csv, encoding=encoding, sep=delimiter, dtype=str, keep_default_na=False)

    def _save_csv(self, df: pd.DataFrame) -> None:
        output_csv = Path(self.config["output_csv"])
        output_csv.parent.mkdir(parents=True, exist_ok=True)

        encoding = self.config.get("encoding", "utf-8")
        delimiter = self.config.get("delimiter", ",")

        df.to_csv(output_csv, index=False, encoding=encoding, sep=delimiter)

    def _save_mapping(self) -> None:
        mapping_output = self.config.get("mapping_output")
        if not mapping_output:
            return

        mapping_path = Path(mapping_output)
        mapping_path.parent.mkdir(parents=True, exist_ok=True)

        with mapping_path.open("w", encoding="utf-8") as f:
            json.dump(self.person_mapper.export_mapping(), f, indent=2, ensure_ascii=False)

    def _apply_person_anonymization(self, series: pd.Series) -> pd.Series:
        return series.apply(self.person_mapper.pseudonymize)

    def _apply_free_text_anonymization(self, series: pd.Series) -> pd.Series:
        return series.apply(self.pii_cleaner.clean_pii)

    def run(self) -> None:
        self._validate_config()
        df = self._load_csv()

        configured_columns: Dict[str, str] = self.config["columns"]

        for column_name, anonymization_type in configured_columns.items():
            if column_name not in df.columns:
                print(f"Warning: column not found in CSV, skipping: {column_name}")
                continue

            if anonymization_type == "person":
                df[column_name] = self._apply_person_anonymization(df[column_name])
            elif anonymization_type == "free_text":
                df[column_name] = self._apply_free_text_anonymization(df[column_name])

        self._save_csv(df)
        self._save_mapping()