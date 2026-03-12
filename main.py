import json
import sys
from pathlib import Path

from anonymizer.csv_processor import CSVAnonymizer


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <config.json>")
        sys.exit(1)

    config_path = Path(sys.argv[1])

    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    anonymizer = CSVAnonymizer(config)
    anonymizer.run()

    print("Anonymization completed successfully.")
    print(f"Output CSV: {config['output_csv']}")

    mapping_output = config.get("mapping_output")
    if mapping_output:
        print(f"Person mapping JSON: {mapping_output}")


if __name__ == "__main__":
    main()