# Dashboard Source Tables Notes

## Purpose
These Phase 2 tables are dashboard-ready CSV sources derived from the validated Phase 1 favorable-response summaries. They are intended for later import or writing into the Excel workbook; this phase does not modify the workbook.

## Source Inputs
- `data/processed/hcahps_favorable_category_summary.csv`
- `data/processed/hcahps_favorable_submeasure_summary.csv`
- `data/processed/hcahps_favorable_hospital_summary.csv`

## Table Uses
- `data/processed/dashboard_category_cards.csv` feeds the top KPI cards. Row count: 6.
- `data/processed/dashboard_category_comparison.csv` feeds category comparison charts and ranked category views. Row count: 6.
- `data/processed/dashboard_submeasure_breakdown.csv` feeds submeasure detail and drill-down views. Row count: 16.
- `data/processed/dashboard_priority_findings.csv` feeds priority callouts and narrative findings. Row count: 5.
- `data/processed/dashboard_hospital_comparison.csv` feeds hospital comparison tables. Row count: 1146.

## Final KPI Values
- Discharge Information: 84.3%
- Nurse Communication: 76.4%
- Doctor Communication: 74.8%
- Medicine Communication: 58.0%
- Overall Rating: 69.1%
- Recommendation: 70.0%

## Calculation Notes
- Weighted favorable percentages come from the validated Phase 1 summaries.
- Category simple averages are unweighted averages of hospital-level category favorable percentages from the validated hospital summary.
- Submeasure simple averages are set equal to the validated weighted submeasure values because Phase 1 did not produce hospital-level submeasure rows.
- Hospital response_count uses the validated hospital summary survey_weight denominator; for multi-submeasure categories this denominator can reflect repeated completed-survey counts across included favorable rows.
- response_rate_context is deduplicated from the cleaned HCAHPS source by facility_id and used as context only.
- Rank is descending, with 1 representing the strongest weighted favorable percent.

## Future Workbook Style Guidance
- Use the screenshots only as broad visual inspiration for a clean Excel dashboard style, not as a template to copy exactly.
- A later workbook phase can use a polished header, KPI cards, simple selectors, structured tables, and clear charts.
- Interactivity should be based on hospital/facility, category, and submeasure.
- Do not introduce fake monthly trends because the validated HCAHPS data is a reporting-period extract, not a monthly time series.

## Limitations
- These files are source tables only; dashboard layout, charts, slicers, KPI cards, and formatting are intentionally out of scope for Phase 2.
- CMS hospital-level percentages are rounded source values, so dashboard summaries inherit source rounding.
- The hospital comparison table should be interpreted as category-level favorable performance, not patient-level microdata.
- Blank numeric cells represent unavailable values and are used instead of invalid Excel values.
