"""Prepare CMS HCAHPS patient experience data for dashboard reporting.

The script expects a CMS HCAHPS CSV file in data/raw/. It standardizes column
names, keeps fields useful for patient experience reporting, assigns dashboard
categories, and exports a cleaned CSV to data/processed/.

No data is downloaded here, and no synthetic records are generated.
"""

from pathlib import Path
import re
import sys

import pandas as pd


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "hcahps_patient_experience_clean.csv"

MEASURE_KEYWORDS = {
    "Discharge & Care Transition": [
        "h_comp_6",
        "h_comp_7",
        "discharge",
        "care transition",
        "transition",
    ],
    "Communication": [
        "h_comp_1",
        "h_comp_2",
        "h_comp_5",
        "communication with nurses",
        "communication with doctors",
        "communication about medicines",
        "communicate with nurses",
        "communicate with doctors",
        "nurses communicated",
        "doctors communicated",
        "staff explained",
        "medicines",
        "medications",
    ],
    "Responsiveness": [
        "h_comp_3",
        "responsiveness",
        "responsive",
        "staff responded",
        "help as soon as",
        "call button",
    ],
    "Overall Experience": [
        "h_hsp_rating",
        "overall hospital rating",
        "overall rating",
        "rating of hospital",
    ],
    "Recommendation": [
        "h_recmnd",
        "recommend",
        "willingness to recommend",
    ],
}

COLUMN_CANDIDATES = {
    "provider_id": [
        "provider_id",
        "facility_id",
        "hospital_id",
        "cms_certification_number_ccn",
    ],
    "hospital_name": [
        "hospital_name",
        "facility_name",
        "provider_name",
    ],
    "state": [
        "state",
    ],
    "measure_id": [
        "measure_id",
        "hcahps_measure_id",
    ],
    "measure_name": [
        "measure_name",
        "hcahps_question",
        "hcahps_answer_description",
        "survey_question",
    ],
}

SCORE_COLUMN_KEYWORDS = [
    "star_rating",
    "score",
    "linear_mean",
    "top_box",
    "bottom_box",
    "middle_box",
    "percent",
    "rate",
]


def snake_case_column(column_name: str) -> str:
    """Convert a source column name to lowercase snake_case."""
    cleaned = column_name.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


def find_raw_csv() -> Path | None:
    """Return the first CSV file found in data/raw/."""
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))
    if not csv_files:
        return None

    if len(csv_files) > 1:
        print("Multiple CSV files found in data/raw/. Using the first file:")
        for csv_file in csv_files:
            print(f"- {csv_file}")

    return csv_files[0]


def first_existing_column(columns: list[str], candidates: list[str]) -> str | None:
    """Find the first expected column that exists in the loaded data."""
    for candidate in candidates:
        if candidate in columns:
            return candidate
    return None


def build_column_map(columns: list[str]) -> dict[str, str]:
    """Map standardized output fields to available CMS source columns."""
    column_map = {}
    missing_fields = []

    for output_field, candidates in COLUMN_CANDIDATES.items():
        source_column = first_existing_column(columns, candidates)
        if source_column:
            column_map[output_field] = source_column
        else:
            missing_fields.append(output_field)

    if missing_fields:
        print("Expected CMS HCAHPS columns were not found.")
        print("Missing standardized fields:")
        for field in missing_fields:
            print(f"- {field}")
        print("\nAvailable columns:")
        for column in columns:
            print(f"- {column}")
        return {}

    return column_map


def measure_category(row: pd.Series) -> str | None:
    """Assign dashboard category based on measure text."""
    measure_text = " ".join(
        str(row.get(column, ""))
        for column in ["measure_id", "measure_name", "source_measure_text"]
        if pd.notna(row.get(column, ""))
    ).lower()

    for category, keywords in MEASURE_KEYWORDS.items():
        if any(keyword in measure_text for keyword in keywords):
            return category

    return None


def relevant_measure_flag(row: pd.Series) -> bool:
    """Flag whether the row maps to a dashboard measure category."""
    return pd.notna(row.get("dashboard_category"))


def select_score_columns(columns: list[str]) -> list[str]:
    """Keep available rating, score, percentage, and rate fields."""
    selected = []
    for column in columns:
        if any(keyword in column for keyword in SCORE_COLUMN_KEYWORDS):
            selected.append(column)
    return selected


def select_footnote_columns(columns: list[str]) -> list[str]:
    """Keep footnote fields when CMS includes them."""
    return [column for column in columns if "footnote" in column]


def prepare_hcahps_data(raw_csv: Path) -> pd.DataFrame | None:
    """Load, standardize, filter, and prepare CMS HCAHPS data."""
    try:
        df = pd.read_csv(raw_csv, dtype=str)
    except Exception as exc:
        print(f"Could not read CSV file: {raw_csv}")
        print(f"Error: {exc}")
        return None

    df.columns = [snake_case_column(column) for column in df.columns]
    columns = list(df.columns)
    column_map = build_column_map(columns)
    if not column_map:
        return None

    # Preserve the original measure text before renaming, because some CMS files
    # separate measure IDs, questions, and answer descriptions.
    measure_text_columns = [
        column
        for column in ["measure_id", "hcahps_measure_id", "measure_name", "hcahps_question", "hcahps_answer_description"]
        if column in columns
    ]
    df["source_measure_text"] = df[measure_text_columns].fillna("").agg(" ".join, axis=1)

    rename_map = {source: output for output, source in column_map.items()}
    df = df.rename(columns=rename_map)

    score_columns = select_score_columns(list(df.columns))
    footnote_columns = select_footnote_columns(list(df.columns))

    output_columns = [
        "provider_id",
        "hospital_name",
        "state",
        "measure_id",
        "measure_name",
        "source_measure_text",
    ]
    output_columns.extend(column for column in score_columns if column not in output_columns)
    output_columns.extend(column for column in footnote_columns if column not in output_columns)

    cleaned = df[output_columns].copy()
    cleaned["dashboard_category"] = cleaned.apply(measure_category, axis=1)
    cleaned["is_dashboard_measure"] = cleaned.apply(relevant_measure_flag, axis=1)
    cleaned = cleaned[cleaned["is_dashboard_measure"]].copy()

    if cleaned.empty:
        print("No dashboard-relevant HCAHPS measures were found.")
        print("Check the measure columns and update MEASURE_KEYWORDS if needed.")
        return None

    cleaned = cleaned.sort_values(
        by=["state", "hospital_name", "dashboard_category", "measure_name"],
        na_position="last",
    )

    return cleaned


def main() -> None:
    """Run the CMS HCAHPS data preparation workflow."""
    raw_csv = find_raw_csv()
    if raw_csv is None:
        print("No CMS HCAHPS CSV file found in data/raw/.")
        print("Download the HCAHPS patient survey CSV from the CMS Provider Data Catalog.")
        print(f"Place the raw CSV in: {RAW_DATA_DIR}")
        sys.exit(0)

    print(f"Loading raw CMS HCAHPS file: {raw_csv}")
    cleaned = prepare_hcahps_data(raw_csv)
    if cleaned is None:
        sys.exit(0)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Exported cleaned dashboard-ready file: {OUTPUT_FILE}")
    print(f"Rows exported: {len(cleaned):,}")


if __name__ == "__main__":
    main()
