"""Prepare CMS HCAHPS hospital patient experience data for reporting.

Default workflow:
    python scripts/prepare_hcahps_data.py

The script pulls records from the CMS Provider Data Catalog API, filters the
data in pandas, and exports a Florida dashboard-ready extract. A local CSV mode
is available for manually downloaded CMS extracts in data/raw/.

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


API_BASE_URL = "https://data.cms.gov/provider-data/api/1/datastore/query/dgck-syfz/0"
DEFAULT_LIMIT = 500
DEFAULT_STATE_FILTER = "FL"

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DATA_DIR / "hcahps_patient_experience_fl_clean.csv"

API_FIELDS = [
    "facility_id",
    "facility_name",
    "address",
    "citytown",
    "state",
    "zip_code",
    "countyparish",
    "telephone_number",
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

CATEGORY_RULES = [
    ("Nurse Communication", ["h_comp_1", "nurses"]),
    ("Doctor Communication", ["h_comp_2", "doctors"]),
    ("Medicine Communication", ["h_comp_5", "medicine", "medicines", "medication"]),
    ("Discharge Information", ["h_comp_6", "discharge"]),
    ("Overall Rating", ["h_hsp_rating", "overall hospital rating", "rating of hospital"]),
    ("Recommendation", ["h_recmnd", "recommend"]),
    ("Summary Rating", ["summary star", "overall star", "h_star_rating", "star rating"]),
]


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Prepare CMS HCAHPS hospital data for dashboard reporting."
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
        help="Two-letter state filter applied in pandas. Default: FL.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"CMS API page size. Default: {DEFAULT_LIMIT}.",
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


def api_url(limit: int, offset: int) -> str:
    """Build the CMS API URL using the working limit/offset pattern."""
    return f"{API_BASE_URL}?{urlencode({'limit': limit, 'offset': offset})}"


def rows_from_response(payload: Any) -> list[dict[str, Any]]:
    """Return keyed records from a CMS API response payload."""
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    rows = payload.get("results", [])
    if not rows:
        return []

    if isinstance(rows[0], dict):
        return rows

    # Some API options can return rows as positional arrays. Map them back to
    # the documented field order if that response shape appears.
    return [dict(zip(API_FIELDS, row)) for row in rows]


def fetch_api_page(limit: int, offset: int) -> list[dict[str, Any]] | None:
    """Fetch one page from the CMS Provider Data Catalog API."""
    url = api_url(limit, offset)
    print(f"Requesting API URL: {url}")

    try:
        with urlopen(url, timeout=60) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        print(f"CMS API request failed with HTTP status {exc.code}.")
        try:
            print("Response body:")
            print(exc.read().decode("utf-8"))
        except Exception:
            print("Response body could not be read.")
        return None
    except URLError as exc:
        print(f"CMS API request failed: {exc.reason}")
        return None

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        print(f"Could not parse CMS API response as JSON: {exc}")
        print("Response body:")
        print(body)
        return None

    return rows_from_response(payload)


def load_from_api(limit: int) -> pd.DataFrame | None:
    """Load HCAHPS records from the CMS API before pandas filtering."""
    records: list[dict[str, Any]] = []
    offset = 0

    while True:
        page_rows = fetch_api_page(limit=limit, offset=offset)
        if page_rows is None:
            return None

        print(f"Rows retrieved this page: {len(page_rows):,}")
        if not page_rows:
            break

        records.extend(page_rows)
        offset += limit

        if len(page_rows) < limit:
            break

    print(f"Total rows retrieved: {len(records):,}")
    if not records:
        print("No records were retrieved from the CMS API.")
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
    """Return lowercased text for matching."""
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
    """Assign dashboard category from HCAHPS measure fields."""
    text = measure_text(row)
    for category, keywords in CATEGORY_RULES:
        if any(keyword in text for keyword in keywords):
            return category
    return "Other"


def add_numeric_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Convert selected CMS fields to numeric companion columns."""
    for field in NUMERIC_FIELDS:
        if field in df.columns:
            df[f"{field}_numeric"] = pd.to_numeric(df[field], errors="coerce")
    return df


def prepare_hcahps_data(df: pd.DataFrame, state_filter: str) -> pd.DataFrame | None:
    """Standardize, filter, categorize, and prepare HCAHPS data."""
    df = df.copy()
    df.columns = [snake_case_column(column) for column in df.columns]

    if not check_required_columns(df):
        return None

    df["facility_id"] = df["facility_id"].astype(str).str.strip()
    df["state"] = df["state"].astype(str).str.strip().str.upper()

    state_filter = state_filter.strip().upper()
    state_df = df[df["state"] == state_filter].copy()
    print(f"Rows after {state_filter} filter: {len(state_df):,}")

    keep_columns = [column for column in API_FIELDS if column in state_df.columns]
    keep_columns.extend(
        column
        for column in state_df.columns
        if "footnote" in column and column not in keep_columns
    )
    cleaned = state_df[keep_columns].copy()

    cleaned["dashboard_category"] = cleaned.apply(dashboard_category, axis=1)
    cleaned["is_relevant_measure"] = cleaned["dashboard_category"] != "Other"
    relevant_count = int(cleaned["is_relevant_measure"].sum())
    print(f"Rows after relevant-measures filter: {relevant_count:,}")

    cleaned = cleaned[cleaned["is_relevant_measure"]].copy()
    cleaned = add_numeric_fields(cleaned)

    sort_columns = [
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


def export_output(cleaned: pd.DataFrame) -> None:
    """Export the Florida dashboard-ready HCAHPS extract."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Output file path: {OUTPUT_FILE}")
    print(f"Rows exported: {len(cleaned):,}")


def main() -> None:
    """Run the CMS HCAHPS data preparation workflow."""
    args = parse_args()

    if args.input_mode == "api":
        df = load_from_api(limit=args.limit)
    else:
        df = load_from_local_csv()

    if df is None:
        sys.exit(0)

    cleaned = prepare_hcahps_data(df, state_filter=args.state)
    if cleaned is None:
        sys.exit(0)

    export_output(cleaned)


if __name__ == "__main__":
    main()
