"""Build dashboard-ready CSV source tables from validated HCAHPS summaries.

This Phase 2 script creates import-ready source tables only. It does not read,
open, write, or modify the Excel dashboard workbook.
"""

from __future__ import annotations

import csv
from math import isfinite
from pathlib import Path
from statistics import mean


CATEGORY_SOURCE = Path("data/processed/hcahps_favorable_category_summary.csv")
SUBMEASURE_SOURCE = Path("data/processed/hcahps_favorable_submeasure_summary.csv")
HOSPITAL_SOURCE = Path("data/processed/hcahps_favorable_hospital_summary.csv")
CLEAN_HCAHPS_SOURCE = Path("data/processed/hcahps_patient_experience_fl_clean.csv")

CATEGORY_CARDS_OUTPUT = Path("data/processed/dashboard_category_cards.csv")
CATEGORY_COMPARISON_OUTPUT = Path("data/processed/dashboard_category_comparison.csv")
SUBMEASURE_BREAKDOWN_OUTPUT = Path("data/processed/dashboard_submeasure_breakdown.csv")
PRIORITY_FINDINGS_OUTPUT = Path("data/processed/dashboard_priority_findings.csv")
HOSPITAL_COMPARISON_OUTPUT = Path("data/processed/dashboard_hospital_comparison.csv")
NOTES_OUTPUT = Path("docs/dashboard_source_tables_notes.md")

CATEGORY_ORDER = [
    "Discharge Information",
    "Nurse Communication",
    "Doctor Communication",
    "Medicine Communication",
    "Overall Rating",
    "Recommendation",
]

CSV_NULL = ""


def parse_number(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        number = float(str(value).strip())
    except ValueError:
        return None
    return number if isfinite(number) else None


def safe_subtract(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    result = left - right
    return result if isfinite(result) else None


def safe_mean(values: list[float]) -> float | None:
    valid_values = [value for value in values if isfinite(value)]
    if not valid_values:
        return None
    result = mean(valid_values)
    return result if isfinite(result) else None


def fmt(value: float | None, digits: int = 2) -> str:
    if value is None or not isfinite(value):
        return CSV_NULL
    return f"{value:.{digits}f}"


def fmt_display(value: float | None) -> str:
    if value is None or not isfinite(value):
        return CSV_NULL
    return f"{value:.1f}%"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, CSV_NULL) for field in fieldnames})


def interpretation_label(category: str, value: float | None) -> str:
    if value is None:
        return "Not available"
    if category == "Medicine Communication":
        return "Priority improvement area"
    if value >= 80:
        return "Strong performance"
    if value >= 70:
        return "Moderate performance"
    return "Needs attention"


def interpretation_note(category: str, value: float | None, rank: int | None = None) -> str:
    if value is None:
        return "Metric unavailable after validation filters."
    if category == "Medicine Communication":
        return "Lowest major category; prioritize medicine purpose and side-effect explanation follow-up."
    if category == "Discharge Information":
        return "Strongest major category and useful benchmark for clearer discharge follow-up practices."
    if category in {"Recommendation", "Overall Rating"}:
        return "Moderate overall experience signal; monitor alongside communication domains."
    if rank == 1:
        return "Top-ranked category by weighted favorable percent."
    return "Core communication domain for comparison across categories."


def row_by_category(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["dashboard_measure_group"]: row for row in rows}


def build_response_rate_lookup(clean_rows: list[dict[str, str]]) -> dict[str, float | None]:
    """Return one response-rate context value per facility when available."""
    values_by_facility: dict[str, set[float]] = {}
    for row in clean_rows:
        facility_id = row.get("facility_id", "")
        if not facility_id:
            continue
        value = parse_number(row.get("survey_response_rate_percent_numeric"))
        if value is None:
            values_by_facility.setdefault(facility_id, set())
            continue
        values_by_facility.setdefault(facility_id, set()).add(value)

    lookup: dict[str, float | None] = {}
    for facility_id, values in values_by_facility.items():
        lookup[facility_id] = next(iter(values)) if len(values) == 1 else None
    return lookup


def hospital_values_by_category(
    hospital_rows: list[dict[str, str]]
) -> dict[str, list[float]]:
    values: dict[str, list[float]] = {category: [] for category in CATEGORY_ORDER}
    for row in hospital_rows:
        category = row.get("dashboard_measure_group", "")
        value = parse_number(row.get("favorable_percent"))
        if category in values and value is not None:
            values[category].append(value)
    return values


def build_category_cards(category_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    categories = row_by_category(category_rows)
    card_rows: list[dict[str, object]] = []
    for index, category in enumerate(CATEGORY_ORDER, start=1):
        value = parse_number(categories[category].get("favorable_percent"))
        card_rows.append(
            {
                "metric_name": category,
                "weighted_favorable_percent": fmt(value),
                "display_value": fmt_display(value),
                "interpretation_label": interpretation_label(category, value),
                "sort_order": index,
            }
        )
    return card_rows


def build_category_comparison(
    category_rows: list[dict[str, str]],
    hospital_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    category_map = row_by_category(category_rows)
    hospital_values = hospital_values_by_category(hospital_rows)
    ranked_categories = sorted(
        CATEGORY_ORDER,
        key=lambda category: parse_number(category_map[category].get("favorable_percent"))
        or -1,
        reverse=True,
    )
    ranks = {category: index for index, category in enumerate(ranked_categories, start=1)}
    rows: list[dict[str, object]] = []
    for category in CATEGORY_ORDER:
        source = category_map[category]
        value = parse_number(source.get("favorable_percent"))
        values = hospital_values[category]
        rows.append(
            {
                "category": category,
                "weighted_favorable_percent": fmt(value),
                "simple_average": fmt(safe_mean(values)),
                "favorable_row_count": source.get("included_rows", CSV_NULL),
                "facility_count": len(values),
                "total_survey_weight": fmt(parse_number(source.get("survey_weight")), 0),
                "rank": ranks[category],
                "interpretation_note": interpretation_note(category, value, ranks[category]),
            }
        )
    return rows


def submeasure_note(category: str, label: str, value: float | None) -> str:
    if value is None:
        return "Metric unavailable after validation filters."
    if category == "Medicine Communication" and label == "side effects":
        return "Lowest specific measure; directly supports side-effect explanation survey follow-up."
    if label == "courtesy/respect":
        return "Respect/courtesy outperforms explanation and listening items within communication domains."
    if "explained" in label or "listened" in label:
        return "Use as diagnostic detail for communication clarity and attentiveness."
    if category == "Discharge Information":
        return "Discharge process detail for follow-up education and written instruction design."
    return "Submeasure detail for dashboard drill-down."


def build_submeasure_breakdown(
    submeasure_rows: list[dict[str, str]]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in submeasure_rows:
        category = source.get("dashboard_measure_group", "")
        label = source.get("submeasure_label", "")
        value = parse_number(source.get("favorable_percent"))
        rows.append(
            {
                "category": category,
                "submeasure_label": label,
                "favorable_response_definition": source.get(
                    "favorable_response_definition", CSV_NULL
                ),
                "weighted_favorable_percent": fmt(value),
                "simple_average": fmt(value),
                "favorable_row_count": source.get("included_rows", CSV_NULL),
                "total_survey_weight": fmt(parse_number(source.get("survey_weight")), 0),
                "interpretation_note": submeasure_note(category, label, value),
            }
        )
    return rows


def find_submeasure(
    rows: list[dict[str, str]], category: str, label: str
) -> dict[str, str] | None:
    for row in rows:
        if (
            row.get("dashboard_measure_group") == category
            and row.get("submeasure_label") == label
        ):
            return row
    return None


def build_priority_findings(
    category_rows: list[dict[str, str]],
    submeasure_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    categories = row_by_category(category_rows)
    sub_rows = {
        (row.get("dashboard_measure_group", ""), row.get("submeasure_label", "")): row
        for row in submeasure_rows
    }
    medicine = parse_number(categories["Medicine Communication"].get("favorable_percent"))
    discharge = parse_number(categories["Discharge Information"].get("favorable_percent"))
    recommendation = parse_number(categories["Recommendation"].get("favorable_percent"))
    overall = parse_number(categories["Overall Rating"].get("favorable_percent"))
    side_effects = parse_number(
        sub_rows[("Medicine Communication", "side effects")].get("favorable_percent")
    )
    nurse_respect = parse_number(
        sub_rows[("Nurse Communication", "courtesy/respect")].get("favorable_percent")
    )
    doctor_respect = parse_number(
        sub_rows[("Doctor Communication", "courtesy/respect")].get("favorable_percent")
    )
    nurse_explain = parse_number(
        sub_rows[("Nurse Communication", "explained clearly")].get("favorable_percent")
    )
    doctor_explain = parse_number(
        sub_rows[("Doctor Communication", "explained clearly")].get("favorable_percent")
    )
    nurse_listen = parse_number(
        sub_rows[("Nurse Communication", "listened carefully")].get("favorable_percent")
    )
    doctor_listen = parse_number(
        sub_rows[("Doctor Communication", "listened carefully")].get("favorable_percent")
    )
    respect_average = safe_mean(
        [value for value in [nurse_respect, doctor_respect] if value is not None]
    )
    explain_average = safe_mean(
        [value for value in [nurse_explain, doctor_explain] if value is not None]
    )
    listening_average = safe_mean(
        [value for value in [nurse_listen, doctor_listen] if value is not None]
    )
    moderate_average = safe_mean(
        [value for value in [recommendation, overall] if value is not None]
    )

    return [
        {
            "finding_title": "Medicine Communication is the weakest major category",
            "metric_value": fmt(medicine),
            "evidence": f"Medicine Communication is {fmt_display(medicine)}, below every other major category.",
            "stakeholder_interpretation": "Medication discussions are the clearest experience gap in the Florida HCAHPS results.",
            "recommended_followup": "Prioritize Qualtrics follow-up questions about medicine purpose, side effects, and when explanations happen.",
        },
        {
            "finding_title": "Side-effect explanation is the lowest specific measure",
            "metric_value": fmt(side_effects),
            "evidence": f"Side-effect explanation is {fmt_display(side_effects)}, the lowest submeasure in the validated breakdown.",
            "stakeholder_interpretation": "Patients report notably weaker counseling on possible side effects than on medication purpose.",
            "recommended_followup": "Ask patients whether side effects were discussed, who discussed them, and what information was still unclear.",
        },
        {
            "finding_title": "Discharge Information is the strongest area",
            "metric_value": fmt(discharge),
            "evidence": f"Discharge Information is {fmt_display(discharge)}, the highest category result.",
            "stakeholder_interpretation": "Discharge education appears comparatively strong and can serve as a communication benchmark.",
            "recommended_followup": "Use discharge communication practices as examples when designing medicine-communication improvements.",
        },
        {
            "finding_title": "Respect/courtesy scores are stronger than explanation/listening scores",
            "metric_value": fmt(respect_average),
            "evidence": f"Nurse and doctor courtesy/respect average {fmt_display(respect_average)} versus explanation average {fmt_display(explain_average)} and listening average {fmt_display(listening_average)}.",
            "stakeholder_interpretation": "Interpersonal tone is stronger than clarity-oriented communication behaviors.",
            "recommended_followup": "Probe what patients need to hear in plain language, especially for medicines and side effects.",
        },
        {
            "finding_title": "Recommendation and Overall Rating are moderate",
            "metric_value": fmt(moderate_average),
            "evidence": f"Recommendation is {fmt_display(recommendation)} and Overall Rating is {fmt_display(overall)}.",
            "stakeholder_interpretation": "Global experience measures are neither the strongest nor weakest signals.",
            "recommended_followup": "Use these global measures as context while focusing action questions on communication gaps.",
        },
    ]


def build_hospital_comparison(
    hospital_rows: list[dict[str, str]],
    category_rows: list[dict[str, str]],
    response_rate_lookup: dict[str, float | None],
) -> list[dict[str, object]]:
    category_map = row_by_category(category_rows)
    rows: list[dict[str, object]] = []
    for source in hospital_rows:
        category = source.get("dashboard_measure_group", "")
        value = parse_number(source.get("favorable_percent"))
        florida_average = parse_number(category_map[category].get("favorable_percent"))
        facility_id = source.get("facility_id", CSV_NULL)
        response_rate = response_rate_lookup.get(facility_id)
        rows.append(
            {
                "facility_id": facility_id,
                "facility_name": source.get("facility_name", CSV_NULL),
                "category": category,
                "weighted_favorable_percent": fmt(value),
                "response_count": fmt(parse_number(source.get("survey_weight")), 0),
                "response_rate_context": fmt(response_rate),
                "florida_category_average": fmt(florida_average),
                "difference_from_florida_average": fmt(
                    safe_subtract(value, florida_average)
                ),
            }
        )
    return rows


def write_notes(row_counts: dict[str, int], category_cards: list[dict[str, object]]) -> None:
    metric_lines = [
        f"- {row['metric_name']}: {row['display_value']}"
        for row in category_cards
    ]
    lines = [
        "# Dashboard Source Tables Notes",
        "",
        "## Purpose",
        "These Phase 2 tables are dashboard-ready CSV sources derived from the validated Phase 1 favorable-response summaries. They are intended for later import or writing into the Excel workbook; this phase does not modify the workbook.",
        "",
        "## Source Inputs",
        f"- `{CATEGORY_SOURCE}`",
        f"- `{SUBMEASURE_SOURCE}`",
        f"- `{HOSPITAL_SOURCE}`",
        "",
        "## Table Uses",
        f"- `{CATEGORY_CARDS_OUTPUT}` feeds the top KPI cards. Row count: {row_counts['category_cards']}.",
        f"- `{CATEGORY_COMPARISON_OUTPUT}` feeds category comparison charts and ranked category views. Row count: {row_counts['category_comparison']}.",
        f"- `{SUBMEASURE_BREAKDOWN_OUTPUT}` feeds submeasure detail and drill-down views. Row count: {row_counts['submeasure_breakdown']}.",
        f"- `{PRIORITY_FINDINGS_OUTPUT}` feeds priority callouts and narrative findings. Row count: {row_counts['priority_findings']}.",
        f"- `{HOSPITAL_COMPARISON_OUTPUT}` feeds hospital comparison tables. Row count: {row_counts['hospital_comparison']}.",
        "",
        "## Final KPI Values",
        *metric_lines,
        "",
        "## Calculation Notes",
        "- Weighted favorable percentages come from the validated Phase 1 summaries.",
        "- Category simple averages are unweighted averages of hospital-level category favorable percentages from the validated hospital summary.",
        "- Submeasure simple averages are set equal to the validated weighted submeasure values because Phase 1 did not produce hospital-level submeasure rows.",
        "- Hospital response_count uses the validated hospital summary survey_weight denominator; for multi-submeasure categories this denominator can reflect repeated completed-survey counts across included favorable rows.",
        "- response_rate_context is deduplicated from the cleaned HCAHPS source by facility_id and used as context only.",
        "- Rank is descending, with 1 representing the strongest weighted favorable percent.",
        "",
        "## Future Workbook Style Guidance",
        "- Use the screenshots only as broad visual inspiration for a clean Excel dashboard style, not as a template to copy exactly.",
        "- A later workbook phase can use a polished header, KPI cards, simple selectors, structured tables, and clear charts.",
        "- Interactivity should be based on hospital/facility, category, and submeasure.",
        "- Do not introduce fake monthly trends because the validated HCAHPS data is a reporting-period extract, not a monthly time series.",
        "",
        "## Limitations",
        "- These files are source tables only; dashboard layout, charts, slicers, KPI cards, and formatting are intentionally out of scope for Phase 2.",
        "- CMS hospital-level percentages are rounded source values, so dashboard summaries inherit source rounding.",
        "- The hospital comparison table should be interpreted as category-level favorable performance, not patient-level microdata.",
        "- Blank numeric cells represent unavailable values and are used instead of invalid Excel values.",
    ]
    NOTES_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    category_rows = read_csv(CATEGORY_SOURCE)
    submeasure_rows = read_csv(SUBMEASURE_SOURCE)
    hospital_rows = read_csv(HOSPITAL_SOURCE)
    clean_rows = read_csv(CLEAN_HCAHPS_SOURCE)
    response_rate_lookup = build_response_rate_lookup(clean_rows)

    category_cards = build_category_cards(category_rows)
    category_comparison = build_category_comparison(category_rows, hospital_rows)
    submeasure_breakdown = build_submeasure_breakdown(submeasure_rows)
    priority_findings = build_priority_findings(category_rows, submeasure_rows)
    hospital_comparison = build_hospital_comparison(
        hospital_rows, category_rows, response_rate_lookup
    )

    write_csv(
        CATEGORY_CARDS_OUTPUT,
        [
            "metric_name",
            "weighted_favorable_percent",
            "display_value",
            "interpretation_label",
            "sort_order",
        ],
        category_cards,
    )
    write_csv(
        CATEGORY_COMPARISON_OUTPUT,
        [
            "category",
            "weighted_favorable_percent",
            "simple_average",
            "favorable_row_count",
            "facility_count",
            "total_survey_weight",
            "rank",
            "interpretation_note",
        ],
        category_comparison,
    )
    write_csv(
        SUBMEASURE_BREAKDOWN_OUTPUT,
        [
            "category",
            "submeasure_label",
            "favorable_response_definition",
            "weighted_favorable_percent",
            "simple_average",
            "favorable_row_count",
            "total_survey_weight",
            "interpretation_note",
        ],
        submeasure_breakdown,
    )
    write_csv(
        PRIORITY_FINDINGS_OUTPUT,
        [
            "finding_title",
            "metric_value",
            "evidence",
            "stakeholder_interpretation",
            "recommended_followup",
        ],
        priority_findings,
    )
    write_csv(
        HOSPITAL_COMPARISON_OUTPUT,
        [
            "facility_id",
            "facility_name",
            "category",
            "weighted_favorable_percent",
            "response_count",
            "response_rate_context",
            "florida_category_average",
            "difference_from_florida_average",
        ],
        hospital_comparison,
    )

    row_counts = {
        "category_cards": len(category_cards),
        "category_comparison": len(category_comparison),
        "submeasure_breakdown": len(submeasure_breakdown),
        "priority_findings": len(priority_findings),
        "hospital_comparison": len(hospital_comparison),
    }
    write_notes(row_counts, category_cards)

    for path, rows in [
        (CATEGORY_CARDS_OUTPUT, category_cards),
        (CATEGORY_COMPARISON_OUTPUT, category_comparison),
        (SUBMEASURE_BREAKDOWN_OUTPUT, submeasure_breakdown),
        (PRIORITY_FINDINGS_OUTPUT, priority_findings),
        (HOSPITAL_COMPARISON_OUTPUT, hospital_comparison),
        (NOTES_OUTPUT, []),
    ]:
        print(f"Wrote {path} ({len(rows) if rows else 'notes'} rows)")


if __name__ == "__main__":
    main()
