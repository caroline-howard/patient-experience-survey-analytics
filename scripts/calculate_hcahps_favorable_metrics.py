"""Calculate survey-weighted favorable HCAHPS metrics for Florida hospitals.

This script reads the cleaned HCAHPS extract and writes three summary CSVs plus
an audit memo. It does not read or modify the Excel dashboard workbook.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from typing import Iterable


SOURCE_FILE = Path("data/processed/hcahps_patient_experience_fl_clean.csv")
CATEGORY_OUTPUT = Path("data/processed/hcahps_favorable_category_summary.csv")
SUBMEASURE_OUTPUT = Path("data/processed/hcahps_favorable_submeasure_summary.csv")
HOSPITAL_OUTPUT = Path("data/processed/hcahps_favorable_hospital_summary.csv")
VALIDATION_MEMO = Path("docs/hcahps_favorable_metric_validation.md")

REQUIRED_COLUMNS = [
    "facility_id",
    "facility_name",
    "state",
    "hcahps_measure_id",
    "hcahps_question",
    "hcahps_answer_description",
    "hcahps_answer_percent_numeric",
    "number_of_completed_surveys_numeric",
    "dashboard_category",
]

CATEGORY_ORDER = [
    "Discharge Information",
    "Nurse Communication",
    "Doctor Communication",
    "Recommendation",
    "Overall Rating",
    "Medicine Communication",
]

EXPECTED_CATEGORY_VALUES = {
    "Discharge Information": 84.27,
    "Nurse Communication": 76.39,
    "Doctor Communication": 74.82,
    "Recommendation": 70.01,
    "Overall Rating": 69.07,
    "Medicine Communication": 58.01,
}

EXPECTED_SUBMEASURE_VALUES = {
    ("Medicine Communication", "side effects"): 43.78,
}

FAVORABLE_MEASURES = {
    "H_COMP_6_Y_P": ("Discharge Information", "given recovery information", "Yes"),
    "H_DISCH_HELP_Y_P": (
        "Discharge Information",
        "staff discussed help after discharge",
        "Yes",
    ),
    "H_SYMPTOMS_Y_P": (
        "Discharge Information",
        "written symptoms to watch for",
        "Yes",
    ),
    "H_COMP_1_A_P": ("Nurse Communication", "overall nurse communication", "Always"),
    "H_NURSE_EXPLAIN_A_P": ("Nurse Communication", "explained clearly", "Always"),
    "H_NURSE_LISTEN_A_P": ("Nurse Communication", "listened carefully", "Always"),
    "H_NURSE_RESPECT_A_P": ("Nurse Communication", "courtesy/respect", "Always"),
    "H_COMP_2_A_P": ("Doctor Communication", "overall doctor communication", "Always"),
    "H_DOCTOR_EXPLAIN_A_P": ("Doctor Communication", "explained clearly", "Always"),
    "H_DOCTOR_LISTEN_A_P": ("Doctor Communication", "listened carefully", "Always"),
    "H_DOCTOR_RESPECT_A_P": ("Doctor Communication", "courtesy/respect", "Always"),
    "H_COMP_5_A_P": (
        "Medicine Communication",
        "overall medicine communication",
        "Always",
    ),
    "H_MED_FOR_A_P": ("Medicine Communication", "new medication purpose", "Always"),
    "H_SIDE_EFFECTS_A_P": ("Medicine Communication", "side effects", "Always"),
    "H_HSP_RATING_9_10": ("Overall Rating", "overall rating 9 or 10", "9 or 10"),
    "H_RECMND_DY": ("Recommendation", "definitely recommend", "Definitely yes"),
}

SUBMEASURE_ORDER = {
    (category, label): index
    for index, (category, label) in enumerate(
        [
            ("Discharge Information", "given recovery information"),
            ("Discharge Information", "staff discussed help after discharge"),
            ("Discharge Information", "written symptoms to watch for"),
            ("Nurse Communication", "overall nurse communication"),
            ("Nurse Communication", "explained clearly"),
            ("Nurse Communication", "listened carefully"),
            ("Nurse Communication", "courtesy/respect"),
            ("Doctor Communication", "overall doctor communication"),
            ("Doctor Communication", "explained clearly"),
            ("Doctor Communication", "listened carefully"),
            ("Doctor Communication", "courtesy/respect"),
            ("Medicine Communication", "overall medicine communication"),
            ("Medicine Communication", "new medication purpose"),
            ("Medicine Communication", "side effects"),
            ("Overall Rating", "overall rating 9 or 10"),
            ("Recommendation", "definitely recommend"),
        ]
    )
}


@dataclass
class WeightedAccumulator:
    weighted_sum: float = 0.0
    survey_weight: float = 0.0
    included_rows: int = 0
    excluded_rows: int = 0
    missing_percent_rows: int = 0
    invalid_percent_rows: int = 0
    missing_weight_rows: int = 0
    invalid_weight_rows: int = 0
    nonpositive_weight_rows: int = 0

    def add(
        self,
        favorable_percent: float | None,
        survey_weight: float | None,
        percent_error: str | None = None,
        weight_error: str | None = None,
    ) -> None:
        """Add one favorable row if both numeric inputs are valid."""
        exclusion_reason = exclusion_for(
            favorable_percent, survey_weight, percent_error, weight_error
        )
        if exclusion_reason:
            self.excluded_rows += 1
            counter_name = f"{exclusion_reason}_rows"
            setattr(self, counter_name, getattr(self, counter_name) + 1)
            return

        assert favorable_percent is not None
        assert survey_weight is not None
        self.weighted_sum += favorable_percent * survey_weight
        self.survey_weight += survey_weight
        self.included_rows += 1

    @property
    def favorable_percent(self) -> float | None:
        return safe_divide(self.weighted_sum, self.survey_weight)


def parse_number(value: str | None) -> tuple[float | None, str | None]:
    """Return a finite float and no reason, or None plus a reason."""
    if value is None or str(value).strip() == "":
        return None, "missing"
    try:
        number = float(str(value).strip())
    except ValueError:
        return None, "invalid"
    if not isfinite(number):
        return None, "invalid"
    return number, None


def exclusion_for(
    favorable_percent: float | None,
    survey_weight: float | None,
    percent_error: str | None = None,
    weight_error: str | None = None,
) -> str | None:
    """Return the exclusion counter stem for an invalid weighted-row input."""
    if percent_error == "missing":
        return "missing_percent"
    if percent_error == "invalid":
        return "invalid_percent"
    if favorable_percent is None:
        return "invalid_percent"
    if not isfinite(favorable_percent):
        return "invalid_percent"
    if weight_error == "missing":
        return "missing_weight"
    if weight_error == "invalid":
        return "invalid_weight"
    if survey_weight is None:
        return "invalid_weight"
    if not isfinite(survey_weight):
        return "invalid_weight"
    if survey_weight <= 0:
        return "nonpositive_weight"
    return None


def safe_divide(numerator: float, denominator: float) -> float | None:
    """Divide only when the denominator is positive and the result is finite."""
    if denominator <= 0 or not isfinite(numerator) or not isfinite(denominator):
        return None
    result = numerator / denominator
    if not isfinite(result):
        return None
    return result


def fmt_number(value: float | None, digits: int = 2) -> str:
    """Format finite numbers for CSV output, leaving invalid values blank."""
    if value is None or not isfinite(value):
        return ""
    return f"{value:.{digits}f}"


def read_source() -> tuple[list[dict[str, str]], list[str]]:
    with SOURCE_FILE.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return rows, fieldnames


def validate_source(rows: list[dict[str, str]], fieldnames: list[str]) -> dict[str, object]:
    states = Counter(row.get("state", "") for row in rows)
    periods = Counter((row.get("start_date", ""), row.get("end_date", "")) for row in rows)
    facilities = {row.get("facility_id", "") for row in rows if row.get("facility_id", "")}
    return {
        "row_count": len(rows),
        "column_count": len(fieldnames),
        "states": states,
        "periods": periods,
        "facility_count": len(facilities),
        "missing_required_columns": [
            column for column in REQUIRED_COLUMNS if column not in fieldnames
        ],
    }


def is_favorable_response(row: dict[str, str]) -> bool:
    measure_id = row.get("hcahps_measure_id", "").strip()
    expected = FAVORABLE_MEASURES.get(measure_id)
    if expected is None:
        return False
    expected_category, _, _ = expected
    return row.get("dashboard_category", "").strip() == expected_category


def accumulate_metrics(
    rows: Iterable[dict[str, str]]
) -> tuple[
    dict[str, WeightedAccumulator],
    dict[tuple[str, str], WeightedAccumulator],
    dict[tuple[str, str, str, str], WeightedAccumulator],
]:
    category_metrics: dict[str, WeightedAccumulator] = defaultdict(WeightedAccumulator)
    submeasure_metrics: dict[tuple[str, str], WeightedAccumulator] = defaultdict(
        WeightedAccumulator
    )
    hospital_metrics: dict[tuple[str, str, str, str], WeightedAccumulator] = defaultdict(
        WeightedAccumulator
    )

    for row in rows:
        if not is_favorable_response(row):
            continue

        measure_id = row["hcahps_measure_id"].strip()
        category, submeasure_label, _ = FAVORABLE_MEASURES[measure_id]
        favorable_percent, percent_error = parse_number(
            row.get("hcahps_answer_percent_numeric")
        )
        survey_weight, weight_error = parse_number(
            row.get("number_of_completed_surveys_numeric")
        )

        category_metrics[category].add(
            favorable_percent, survey_weight, percent_error, weight_error
        )
        submeasure_metrics[(category, submeasure_label)].add(
            favorable_percent, survey_weight, percent_error, weight_error
        )
        hospital_key = (
            row.get("facility_id", "").strip(),
            row.get("facility_name", "").strip(),
            row.get("state", "").strip(),
            category,
        )
        hospital_metrics[hospital_key].add(
            favorable_percent, survey_weight, percent_error, weight_error
        )

    return category_metrics, submeasure_metrics, hospital_metrics


def write_category_summary(metrics: dict[str, WeightedAccumulator]) -> None:
    fieldnames = [
        "dashboard_measure_group",
        "favorable_response_definition",
        "favorable_percent",
        "survey_weight",
        "included_rows",
        "excluded_rows",
        "expected_favorable_percent",
        "expected_difference_points",
        "matches_expected",
    ]
    definitions = {
        "Discharge Information": "Yes",
        "Nurse Communication": "Always",
        "Doctor Communication": "Always",
        "Medicine Communication": "Always",
        "Overall Rating": "9 or 10",
        "Recommendation": "Definitely yes",
    }
    with CATEGORY_OUTPUT.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for category in CATEGORY_ORDER:
            metric = metrics[category]
            actual = metric.favorable_percent
            expected = EXPECTED_CATEGORY_VALUES.get(category)
            difference = None if actual is None or expected is None else actual - expected
            writer.writerow(
                {
                    "dashboard_measure_group": category,
                    "favorable_response_definition": definitions[category],
                    "favorable_percent": fmt_number(actual),
                    "survey_weight": fmt_number(metric.survey_weight, 0),
                    "included_rows": metric.included_rows,
                    "excluded_rows": metric.excluded_rows,
                    "expected_favorable_percent": fmt_number(expected),
                    "expected_difference_points": fmt_number(difference),
                    "matches_expected": (
                        ""
                        if difference is None
                        else str(abs(difference) <= 0.05).upper()
                    ),
                }
            )


def write_submeasure_summary(metrics: dict[tuple[str, str], WeightedAccumulator]) -> None:
    fieldnames = [
        "dashboard_measure_group",
        "submeasure_label",
        "favorable_response_definition",
        "favorable_percent",
        "survey_weight",
        "included_rows",
        "excluded_rows",
        "expected_favorable_percent",
        "expected_difference_points",
        "matches_expected",
    ]
    keys = sorted(
        metrics,
        key=lambda key: SUBMEASURE_ORDER.get(key, 999),
    )
    with SUBMEASURE_OUTPUT.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for category, submeasure_label in keys:
            metric = metrics[(category, submeasure_label)]
            actual = metric.favorable_percent
            expected = EXPECTED_SUBMEASURE_VALUES.get((category, submeasure_label))
            difference = None if actual is None or expected is None else actual - expected
            definition = next(
                definition
                for measure_category, label, definition in FAVORABLE_MEASURES.values()
                if measure_category == category and label == submeasure_label
            )
            writer.writerow(
                {
                    "dashboard_measure_group": category,
                    "submeasure_label": submeasure_label,
                    "favorable_response_definition": definition,
                    "favorable_percent": fmt_number(actual),
                    "survey_weight": fmt_number(metric.survey_weight, 0),
                    "included_rows": metric.included_rows,
                    "excluded_rows": metric.excluded_rows,
                    "expected_favorable_percent": fmt_number(expected),
                    "expected_difference_points": fmt_number(difference),
                    "matches_expected": (
                        ""
                        if difference is None
                        else str(abs(difference) <= 0.05).upper()
                    ),
                }
            )


def write_hospital_summary(
    metrics: dict[tuple[str, str, str, str], WeightedAccumulator]
) -> None:
    fieldnames = [
        "facility_id",
        "facility_name",
        "state",
        "dashboard_measure_group",
        "favorable_percent",
        "survey_weight",
        "included_rows",
        "excluded_rows",
    ]
    keys = sorted(
        metrics,
        key=lambda key: (key[1], CATEGORY_ORDER.index(key[3]) if key[3] in CATEGORY_ORDER else 99),
    )
    with HOSPITAL_OUTPUT.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for facility_id, facility_name, state, category in keys:
            metric = metrics[(facility_id, facility_name, state, category)]
            writer.writerow(
                {
                    "facility_id": facility_id,
                    "facility_name": facility_name,
                    "state": state,
                    "dashboard_measure_group": category,
                    "favorable_percent": fmt_number(metric.favorable_percent),
                    "survey_weight": fmt_number(metric.survey_weight, 0),
                    "included_rows": metric.included_rows,
                    "excluded_rows": metric.excluded_rows,
                }
            )


def table_row(values: Iterable[object]) -> str:
    return "| " + " | ".join(str(value) for value in values) + " |"


def total_exclusions(metrics: Iterable[WeightedAccumulator]) -> dict[str, int]:
    totals = {
        "excluded_rows": 0,
        "missing_percent_rows": 0,
        "invalid_percent_rows": 0,
        "missing_weight_rows": 0,
        "invalid_weight_rows": 0,
        "nonpositive_weight_rows": 0,
    }
    for metric in metrics:
        for key in totals:
            totals[key] += getattr(metric, key)
    return totals


def write_validation_memo(
    validation: dict[str, object],
    category_metrics: dict[str, WeightedAccumulator],
    submeasure_metrics: dict[tuple[str, str], WeightedAccumulator],
) -> None:
    states = validation["states"]
    periods = validation["periods"]
    assert isinstance(states, Counter)
    assert isinstance(periods, Counter)

    category_exclusions = total_exclusions(category_metrics.values())
    submeasure_keys = sorted(
        submeasure_metrics,
        key=lambda key: SUBMEASURE_ORDER.get(key, 999),
    )
    category_matches = []
    for category in CATEGORY_ORDER:
        actual = category_metrics[category].favorable_percent
        expected = EXPECTED_CATEGORY_VALUES[category]
        category_matches.append(actual is not None and abs(actual - expected) <= 0.05)

    lines = [
        "# HCAHPS Favorable Metric Validation",
        "",
        "## Data Source",
        f"- Source file: `{SOURCE_FILE}`",
        "- Dataset: public CMS HCAHPS hospital-level patient survey data.",
        "",
        "## Scope",
        f"- Rows: {validation['row_count']:,}",
        f"- Columns: {validation['column_count']:,}",
        f"- Facilities: {validation['facility_count']:,}",
        f"- States present: {', '.join(f'{state} ({count:,})' for state, count in states.items())}",
        f"- Reporting periods: {', '.join(f'{start} to {end} ({count:,})' for (start, end), count in periods.items())}",
        "",
        "## Required Columns",
    ]
    missing_required = validation["missing_required_columns"]
    if missing_required:
        lines.append(
            "- Missing required columns: "
            + ", ".join(f"`{column}`" for column in missing_required)
        )
    else:
        lines.append("- All required columns are present.")

    lines.extend(
        [
            "",
            "## Favorable-Response Definitions",
            "- Discharge Information: `Yes`",
            "- Nurse Communication: `Always`",
            "- Doctor Communication: `Always`",
            "- Medicine Communication: `Always`",
            "- Overall Rating: `9 or 10`",
            "- Recommendation: `Definitely yes`",
            "",
            "## Weighting Method",
            "- `favorable_percent = hcahps_answer_percent_numeric`",
            "- `survey_weight = number_of_completed_surveys_numeric`",
            "- Weighted favorable percent = `sum(favorable_percent * survey_weight) / sum(survey_weight)`.",
            "- Included rows must be favorable-response rows with numeric favorable percent and numeric survey weight greater than zero.",
            "- If a denominator is zero, missing, or invalid, the result is left blank/null rather than emitting an invalid value.",
            "",
            "## Category Results",
            table_row(
                [
                    "Measure group",
                    "Favorable %",
                    "Expected %",
                    "Difference",
                    "Included rows",
                    "Excluded rows",
                    "Matches expected",
                ]
            ),
            table_row(["---", "---:", "---:", "---:", "---:", "---:", "---"]),
        ]
    )
    for category in CATEGORY_ORDER:
        metric = category_metrics[category]
        actual = metric.favorable_percent
        expected = EXPECTED_CATEGORY_VALUES[category]
        difference = None if actual is None else actual - expected
        lines.append(
            table_row(
                [
                    category,
                    fmt_number(actual),
                    fmt_number(expected),
                    fmt_number(difference),
                    metric.included_rows,
                    metric.excluded_rows,
                    "Yes" if difference is not None and abs(difference) <= 0.05 else "No",
                ]
            )
        )

    lines.extend(
        [
            "",
            "## Submeasure Results",
            table_row(
                [
                    "Measure group",
                    "Submeasure",
                    "Favorable %",
                    "Included rows",
                    "Excluded rows",
                ]
            ),
            table_row(["---", "---", "---:", "---:", "---:"]),
        ]
    )
    for category, submeasure_label in submeasure_keys:
        metric = submeasure_metrics[(category, submeasure_label)]
        lines.append(
            table_row(
                [
                    category,
                    submeasure_label,
                    fmt_number(metric.favorable_percent),
                    metric.included_rows,
                    metric.excluded_rows,
                ]
            )
        )

    side_effect_metric = submeasure_metrics[("Medicine Communication", "side effects")]
    side_effect_actual = side_effect_metric.favorable_percent
    side_effect_expected = EXPECTED_SUBMEASURE_VALUES[
        ("Medicine Communication", "side effects")
    ]

    lines.extend(
        [
            "",
            "## Excluded Rows And Missing Values",
            f"- Favorable rows excluded from category calculations: {category_exclusions['excluded_rows']:,}",
            f"- Missing favorable percent: {category_exclusions['missing_percent_rows']:,}",
            f"- Invalid favorable percent: {category_exclusions['invalid_percent_rows']:,}",
            f"- Missing survey weight: {category_exclusions['missing_weight_rows']:,}",
            f"- Invalid survey weight: {category_exclusions['invalid_weight_rows']:,}",
            f"- Nonpositive survey weight: {category_exclusions['nonpositive_weight_rows']:,}",
            "",
            "## Expected-Metric Check",
            f"- Category values match the provided expected metrics within 0.05 percentage points: {'Yes' if all(category_matches) else 'No'}.",
            f"- Side-effect explanation favorable percent: {fmt_number(side_effect_actual)}% versus expected about {fmt_number(side_effect_expected)}%.",
            "",
            "## Limitations",
            "- CMS hospital-level percentages are already rounded by the source data; weighted summaries therefore inherit that rounding.",
            "- Survey weights use the hospital-level completed survey count repeated across HCAHPS measure rows, not patient-level microdata.",
            "- Hospitals with missing percentages or missing/nonpositive completed-survey counts are excluded from the relevant weighted calculation.",
        ]
    )

    VALIDATION_MEMO.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows, fieldnames = read_source()
    validation = validate_source(rows, fieldnames)
    missing_required = validation["missing_required_columns"]
    if missing_required:
        missing = ", ".join(str(column) for column in missing_required)
        raise SystemExit(f"Missing required columns: {missing}")

    category_metrics, submeasure_metrics, hospital_metrics = accumulate_metrics(rows)
    write_category_summary(category_metrics)
    write_submeasure_summary(submeasure_metrics)
    write_hospital_summary(hospital_metrics)
    write_validation_memo(validation, category_metrics, submeasure_metrics)

    print(f"Wrote {CATEGORY_OUTPUT}")
    print(f"Wrote {SUBMEASURE_OUTPUT}")
    print(f"Wrote {HOSPITAL_OUTPUT}")
    print(f"Wrote {VALIDATION_MEMO}")


if __name__ == "__main__":
    main()
