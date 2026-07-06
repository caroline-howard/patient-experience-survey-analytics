"""Prepare CMS HCAHPS hospital patient experience data for reporting.

Default workflow:
    python scripts/prepare_hcahps_data.py

The default API mode pulls a filtered Florida extract from the CMS Provider Data
Catalog API for dataset dgck-syfz. A local CSV mode is also available for a
manually downloaded extract saved in data/raw/.

No synthetic data is generated.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd


DATASET_ID = "dgck-syfz"
DATASET_NAME = "Patient survey (HCAHPS) - Hospital"
API_URL = f"https://data.cms.gov/provider-data/api/1/datastore/query/{DATASET_ID}/0"
DEFAULT_STATE_FILTER = "FL"
DEFAULT_PAGE_SIZE = 5000

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "hcahps_patient_experience_clean.csv"

API_FIELDS = [
    "facility_id",
    "facility_name",
    "state",
    "hcahps_measure_id",
    "hcahps_question",
    "hcahps_answer_description",
    "patient_survey_star_rating",
    "patient_survey_star_rating_footnote",
    "hcahps_answer_percent",
    "hcahps_answer_percent_footnote",
    "hcahps_linear_mean_value",
    "number_of_completed_surveys",
    "number_of_completed_surveys_footnote",
    "survey_response_rate_percent",
    "survey_response_rate_percent_footnote",
    "start_date",
    "end_date",
]

REQUIRED_FIELDS = [
    "facility_id",
    "facility_name",
    "state",
    "hcahps_measure_id",
    "hcahps_question",
    "hcahps_answer_description",
]

NUMERIC_FIELDS = [
    "patient_survey_star_rating",
    "hcahps_answer_percent",
    "hcahps_linear_mean_value",
    "number_of_completed_surveys",
    "survey_response_rate_percent",
]

FOOTNOTE_FIELDS = [
    "patient_survey_star_rating_footnote",
    "hcahps_answer_percent_footnote",
    "number_of_completed_surveys_footnote",
    "survey_response_rate_percent_footnote",
]

SUPPRESSED_VALUES = {
    "",
    "not applicable",
    "not available",
    "not available results are not shown for this measure",
    "not enough data available",
}

CATEGORY_RULES = [
    (
        "Discharge Information",
        [
            "h_comp_6",
            "discharge",
        ],
    ),
    (
        "Communication",
        [
            "h_comp_1",
            "h_comp_2",
            "h_comp_5",
            "communication with nurses",
            "communication with doctors",
            "communication about medicines",
            "nurses communicated",
            "doctors communicated",
            "medicines",
            "medications",
        ],
    ),
    (
        "Overall Experience",
        [
            "h_hsp_rating",
            "overall hospital rating",
            "overall rating",
            "rating of hospital",
        ],
    ),
    (
        "Recommendation",
        [
            "h_recmnd",
            "recommend",
        ],
    ),
    (
        "Summary Rating",
        [
            "summary star",
            "overall star",
            "h_star_rating",
            "star rating",
        ],
    ),
]


def parse_args() -> argparse.Namespace:
    """Parse command-line options for API or local CSV mode."""
    parser = argparse.ArgumentParser(
        description=f"Prepare CMS {DATASET_NAME} data for dashboard reporting."
    )
    parser.add_argument(
        "--input-mode",
        choices=["api", "local"],
        default="api",
        help="Use the CMS API or a local CSV from data/raw/. Default: api.",
    )
    parser.add_argument(
        "--state",
        default=DEFAULT_STATE_FILTER,
        help=(
            "Two-letter state filter for API mode. Default: FL. "
            "Use --all-states to pull all states."
        ),
    )
    parser.add_argument(
        "--all-states",
        action="store_true",
        help="Pull all states in API mode. This may create a large output file.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=DEFAULT_PAGE_SIZE,
        help=f"API page size. Default: {DEFAULT_PAGE_SIZE}.",
    )
    return parser.parse_args()


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


def build_api_params(
    limit: int,
    offset: int,
    state_filter: str | None,
) -> list[tuple[str, str | int]]:
    """Build CMS Provider Data Catalog API parameters."""
    params: list[tuple[str, str | int]] = [
        ("limit", limit),
        ("offset", offset),
        ("schema", "false"),
        ("keys", "true"),
        ("rowIds", "false"),
    ]

    for index, field in enumerate(API_FIELDS):
        params.append((f"properties[{index}]", field))

    if state_filter:
        params.extend(
            [
                ("conditions[0][property]", "state"),
                ("conditions[0][value]", state_filter),
                ("conditions[0][operator]", "="),
            ]
        )

    return params


def fetch_api_page(
    limit: int,
    offset: int,
    state_filter: str | None,
) -> dict[str, Any] | list[dict[str, Any]] | None:
    """Fetch one page of HCAHPS records from the CMS API."""
    query = urlencode(build_api_params(limit, offset, state_filter))
    url = f"{API_URL}?{query}"

    try:
        with urlopen(url, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        print(f"CMS API request failed with HTTP status {exc.code}.")
    except URLError as exc:
        print(f"CMS API request failed: {exc.reason}")
    except json.JSONDecodeError as exc:
        print(f"Could not parse CMS API response as JSON: {exc}")

    return None


def load_from_api(state_filter: str | None, page_size: int) -> pd.DataFrame | None:
    """Load a filtered HCAHPS extract from the CMS Provider Data Catalog API."""
    if state_filter:
        print(f"Using CMS API mode with state filter: {state_filter}")
    else:
        print("Using CMS API mode with no state filter.")
        print("Warning: pulling all states may create a large output file.")

    records: list[dict[str, Any]] = []
    offset = 0
    total_count: int | None = None

    while True:
        page = fetch_api_page(page_size, offset, state_filter)
        if page is None:
            return None

        if isinstance(page, list):
            page_records = page
        else:
            page_records = page.get("results", [])

        if total_count is None:
            total_count = page.get("count") if isinstance(page, dict) else None
            if total_count is not None:
                print(f"CMS API records available for extract: {total_count:,}")

        if not page_records:
            break

        records.extend(page_records)
        print(f"Fetched {len(records):,} records...")

        if len(page_records) < page_size:
            break

        offset += page_size

    if not records:
        print("CMS API returned no records for the selected filter.")
        return None

    return pd.DataFrame(records)


def load_from_local_csv() -> pd.DataFrame | None:
    """Load a manually downloaded CMS HCAHPS CSV extract from data/raw/."""
    raw_csv = find_raw_csv()
    if raw_csv is None:
        print("No local CMS HCAHPS CSV file found in data/raw/.")
        print("Use API mode or place a downloaded HCAHPS extract in data/raw/.")
        return None

    print(f"Using local CSV mode with file: {raw_csv}")
    try:
        return pd.read_csv(raw_csv, dtype={"facility_id": str, "Facility ID": str})
    except Exception as exc:
        print(f"Could not read CSV file: {raw_csv}")
        print(f"Error: {exc}")
        return None


def check_required_columns(df: pd.DataFrame) -> bool:
    """Stop safely when expected HCAHPS fields are not available."""
    missing = [field for field in REQUIRED_FIELDS if field not in df.columns]
    if not missing:
        return True

    print("Expected CMS HCAHPS columns were not found.")
    print("Missing fields:")
    for field in missing:
        print(f"- {field}")

    print("\nAvailable columns:")
    for column in df.columns:
        print(f"- {column}")

    return False


def normalize_text(value: Any) -> str:
    """Return lowercased text for matching and suppressed-value checks."""
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def measure_text(row: pd.Series) -> str:
    """Combine HCAHPS measure fields for category assignment."""
    return " ".join(
        normalize_text(row.get(column, ""))
        for column in [
            "hcahps_measure_id",
            "hcahps_question",
            "hcahps_answer_description",
        ]
    )


def dashboard_category(row: pd.Series) -> str:
    """Assign the dashboard category for each HCAHPS measure row."""
    text = measure_text(row)
    measure_id = normalize_text(row.get("hcahps_measure_id", ""))

    for category, keywords in CATEGORY_RULES:
        if any(keyword in text for keyword in keywords):
            if category == "Summary Rating" and measure_id.startswith("h_comp_"):
                continue
            return category

    return "Other"


def is_suppressed(value: Any) -> bool:
    """Identify missing or suppressed CMS values without dropping the row."""
    return normalize_text(value) in SUPPRESSED_VALUES


def add_numeric_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Convert dashboard numeric fields while preserving original text fields."""
    for field in NUMERIC_FIELDS:
        if field not in df.columns:
            continue

        numeric_field = f"{field}_numeric"
        usable_values = df[field].where(~df[field].apply(is_suppressed))
        df[numeric_field] = pd.to_numeric(usable_values, errors="coerce")

    numeric_columns = [f"{field}_numeric" for field in NUMERIC_FIELDS if f"{field}_numeric" in df]
    if numeric_columns:
        df["has_numeric_dashboard_value"] = df[numeric_columns].notna().any(axis=1)
    else:
        df["has_numeric_dashboard_value"] = False

    return df


def prepare_hcahps_data(df: pd.DataFrame) -> pd.DataFrame | None:
    """Standardize and prepare HCAHPS data for dashboard use."""
    df = df.copy()
    df.columns = [snake_case_column(column) for column in df.columns]

    if not check_required_columns(df):
        return None

    # Facility IDs are identifiers, not numbers. Keep them as text to preserve
    # leading zeroes from CMS.
    df["facility_id"] = df["facility_id"].astype(str).str.strip()
    df["state"] = df["state"].astype(str).str.strip().str.upper()

    keep_columns = [column for column in API_FIELDS if column in df.columns]
    keep_columns.extend(column for column in df.columns if "footnote" in column and column not in keep_columns)
    cleaned = df[keep_columns].copy()

    cleaned["dashboard_category"] = cleaned.apply(dashboard_category, axis=1)
    cleaned["is_project_measure"] = cleaned["dashboard_category"] != "Other"
    cleaned = add_numeric_fields(cleaned)

    sort_columns = [
        "state",
        "facility_name",
        "dashboard_category",
        "hcahps_measure_id",
        "hcahps_answer_description",
    ]
    cleaned = cleaned.sort_values(
        by=[column for column in sort_columns if column in cleaned.columns],
        na_position="last",
    )

    return cleaned


def export_outputs(cleaned: pd.DataFrame, state_filter: str | None) -> None:
    """Export cleaned dashboard-ready HCAHPS data."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Exported cleaned dashboard-ready file: {OUTPUT_FILE}")

    if state_filter and state_filter.upper() == DEFAULT_STATE_FILTER:
        state_output = (
            PROCESSED_DATA_DIR
            / f"hcahps_patient_experience_{state_filter.lower()}_clean.csv"
        )
        cleaned.to_csv(state_output, index=False)
        print(f"Exported default state extract: {state_output}")

    print(f"Rows exported: {len(cleaned):,}")


def main() -> None:
    """Run the CMS HCAHPS data preparation workflow."""
    args = parse_args()
    state_filter = None if args.all_states else args.state.strip().upper()

    if args.input_mode == "api":
        df = load_from_api(state_filter=state_filter, page_size=args.page_size)
    else:
        df = load_from_local_csv()

    if df is None:
        sys.exit(0)

    cleaned = prepare_hcahps_data(df)
    if cleaned is None:
        sys.exit(0)

    export_outputs(cleaned, state_filter=state_filter)


if __name__ == "__main__":
    main()
