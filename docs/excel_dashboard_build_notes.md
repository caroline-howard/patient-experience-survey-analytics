# Excel Dashboard Build Notes

## Sheets Created/Updated
- Dashboard_Source
- Dashboard
- Category_Detail
- Hospital_Detail
- README
- Insights_Brief
- Validation_Lists (hidden selector support)

## Source Tables Used
- `data/processed/dashboard_category_cards.csv`
- `data/processed/dashboard_category_comparison.csv`
- `data/processed/dashboard_submeasure_breakdown.csv`
- `data/processed/dashboard_priority_findings.csv`
- `data/processed/dashboard_hospital_comparison.csv`

## Charts/Tables Added
- Dashboard_Source: Excel tables for KPI cards, category comparison, submeasure breakdown, priority findings, and hospital comparison.
- Dashboard: KPI cards, category comparison bar chart, priority callout, submeasure table, interpretation box, and Qualtrics next-step box.
- Category_Detail: submeasure table, conditional formatting, and bar chart.
- Hospital_Detail: hospital/facility comparison table, Florida average comparison, difference from average, and category/facility selectors.

## Final KPI Values
- Discharge Information: 84.27%
- Nurse Communication: 76.39%
- Doctor Communication: 74.82%
- Medicine Communication: 58.01%
- Overall Rating: 69.07%
- Recommendation: 70.01%

## Limitations
- No fake monthly trends were created because the HCAHPS data is a reporting-period extract.
- response_rate_context is now populated where the cleaned HCAHPS source includes a facility response rate; missing facility rates display as `Not available`.
- Facility-level differences use public hospital-level reporting data and should not be interpreted as patient-level microdata.
- Screenshot references were used only for broad clean healthcare dashboard styling inspiration.

## Validation Result
- openpyxl reopened workbook successfully: True.
- Invalid token/value scan count: 0.
- Required sheets present: True.
- Sheet dimensions: {'Clean_Data': 'A1:AG11461', 'README': 'A1:B9', 'Data_Dictionary': 'A1:B24', 'Pivot_Source': 'A1:P11461', 'Dashboard': 'A1:N47', 'Insights_Brief': 'A1:B7', 'Dashboard_Source': 'A1:N1191', 'Category_Detail': 'A1:H23', 'Hospital_Detail': 'A1:K1153'}.

## Hospital_Detail reset and filterable table fix
- Reset the sheet because the previous formula-driven selector version produced `#NAME?` errors and awkward formatting.
- Removed formula-driven selectors and all visible formulas from `Hospital_Detail`.
- Rebuilt the page as a static values-only Excel table sourced from `data/processed/dashboard_hospital_comparison.csv`.
- Added built-in Excel table filters for Facility name, Category, and Performance status.
- Added red/green above/below Florida average conditional formatting and subtle Medicine Communication emphasis.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=1; filter_enabled=True; medicine_rows=191.

## Hospital_Detail compatibility polish
- Simplified the top title and note area into cleaner callout boxes.
- Strengthened the Medicine Communication priority callout.
- Removed formula-based conditional formatting from `Hospital_Detail` and replaced it with static red/green cell styling to reduce Excel repair risk.
- Kept the static values-only Excel table and built-in filters.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=1; filter_enabled=True; conditional_format_rule_groups=0.

## Hospital_Detail top note cleanup
- Cleaned stray broken text from the `Hospital_Detail` top note area.
- Rebuilt rows 1-8 as compact static callout boxes.
- Left the values-only filterable table unchanged.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=1; filter_enabled=True.

## Category_Detail static submeasure drill-down update
- Rebuilt `Category_Detail` as a values-only, filterable submeasure drill-down table.
- Removed the cramped chart and formula-based conditional formatting.
- Added compact callout boxes matching the `Hospital_Detail` dashboard rhythm.
- Added a static Status column to flag Strong, Moderate, Priority area, and Priority follow-up rows.
- Emphasized Medicine Communication and side-effect explanation with static styling.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=1; filter_enabled=True; chart_count=0; conditional_format_rule_groups=0.

## README start-here page update
- Rebuilt `README` as a static start-here page instead of a raw metadata table.
- Added a dashboard-style title block, purpose callout, key findings, workbook navigation, metric definitions, and limitations.
- Removed the README Excel table/filter controls because this sheet is explanatory, not analytical source data.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=0; chart_count=0; conditional_format_rule_groups=0.

## README compact layout polish
- Tightened the `README` into a compact start-here page with no frozen split.
- Moved key findings, workbook navigation, metric definitions, and limitations into the first visible page area.
- Kept the sheet static and compatibility-focused: no formulas, charts, tables, or conditional formatting.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=0; chart_count=0; conditional_format_rule_groups=0.

## Dashboard static overview polish
- Rebuilt `Dashboard` as a static, table-driven overview page.
- Removed the overlapping chart object and replaced it with a ranked comparison table plus static visual bar cells.
- Tightened KPI cards and priority callouts while keeping Medicine Communication and side-effect explanation prominent.
- Kept the sheet compatibility-focused: no formulas, charts, Excel tables, or conditional-formatting rules.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=0; chart_count=0; conditional_format_rule_groups=0.

## Dashboard wide static layout polish
- Rebuilt `Dashboard` on a wider `A:R` canvas with equal-width KPI cards.
- Gave the category comparison table more room for status, interpretation, and static visual bars.
- Added a right-side dashboard-use panel and matching lower priority/submeasure panels.
- Kept the sheet static and compatibility-focused: no formulas, charts, Excel tables, or conditional-formatting rules.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=0; chart_count=0; conditional_format_rule_groups=0.

## Dashboard final layout polish
- Equalized the six KPI cards across `A:R` and adjusted column widths to reduce awkward wrapping.
- Shortened the top header, tightened category interpretation text, and moved lower panels upward.
- Balanced the priority callout and Medicine Communication spotlight so both are visible with less scrolling.
- Kept the sheet static and compatibility-focused: no formulas, charts, Excel tables, or conditional-formatting rules.
- Validation result: reopened=True; invalid_count=0; formula_count=0; table_count=0; chart_count=0; conditional_format_rule_groups=0.
