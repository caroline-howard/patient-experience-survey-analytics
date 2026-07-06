"""Prepare CMS HCAHPS patient experience data for reporting.

This placeholder script documents the intended preparation workflow without
downloading source files or generating synthetic data.
"""

from pathlib import Path


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "hcahps_discharge_measures_clean.csv"


def main() -> None:
    """Outline the CMS HCAHPS data preparation workflow."""
    # 1. Load CMS HCAHPS source files placed in data/raw/.
    # 2. Standardize column names for consistent analysis.
    # 3. Filter patient experience and discharge-related measures.
    # 4. Convert score fields to analysis-ready numeric values.
    # 5. Export the cleaned dataset to data/processed/.
    #
    # No data is downloaded here, and no fake records are generated.
    print("CMS HCAHPS preparation placeholder")
    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Processed output path: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
