# Excel Dashboard Structure

Workbook:

```text
excel_dashboard/patient_discharge_experience_dashboard.xlsx
```

Input file:

```text
data/processed/hcahps_patient_experience_fl_clean.csv
```

## Workbook Tabs

| Tab | Purpose |
| --- | --- |
| `README` | Workbook notes, source details, metric logic, and refresh guidance |
| `Clean_Data` | Full cleaned CMS HCAHPS patient experience file exported from the Python workflow |
| `Data_Dictionary` | Field definitions, source notes, and dashboard use |
| `Pivot_Source` | Slimmed reporting source table with favorable-response fields |
| `Dashboard` | Stakeholder-facing reporting view |
| `Insights_Brief` | Concise narrative summary based on corrected dashboard metrics |

The workbook does not currently include a separate `Source_API_Extract` sheet. The auditable source rows used by the workbook are available in `Clean_Data`.

## Dashboard Metric Logic

The dashboard emphasizes favorable-response metrics. It does not average all HCAHPS answer buckets together.

Main KPI calculation:

```text
sum(favorable_response_percent_numeric * number_of_completed_surveys_numeric)
/ sum(number_of_completed_surveys_numeric)
```

This produces a survey-volume-weighted favorable-response percentage for Florida hospitals.

Favorable-response rules:

| Dashboard category | Favorable response |
| --- | --- |
| Discharge Information | `Yes` |
| Nurse Communication | `Always` |
| Doctor Communication | `Always` |
| Medicine Communication | `Always` |
| Overall Rating | `9 or 10` |
| Recommendation | `Definitely yes` |

## Dashboard Sections

| Section | Purpose |
| --- | --- |
| KPI summary | Reporting period, facilities represented, completed survey context, response rate, and metric logic |
| Category favorable-response summary | Survey-weighted and simple favorable-response results by dashboard category |
| Submeasure breakdown | More detailed favorable-response results within each category |
| Facility comparison | Top 25 facilities by simple favorable-response average for benchmarking |
| Interpretation note | Explains weighted KPI logic and auditability |

## Visuals

The workbook includes:

- A category bar chart for survey-weighted favorable-response percentages.
- A submeasure bar chart highlighting the lowest favorable-response submeasures.
- Formatted summary tables for category, submeasure, and facility views.

## Current Dashboard Findings to Highlight

| Finding | Survey-weighted favorable-response value |
| --- | ---: |
| Discharge Information | 84.27 |
| Nurse Communication | 76.39 |
| Doctor Communication | 74.82 |
| Medicine Communication | 58.01 |
| Overall Rating | 69.07 |
| Recommendation | 70.01 |

The clearest improvement opportunity is medicine communication, especially side-effect explanation.

## API Refresh Notes

Default command:

```bash
python scripts/prepare_hcahps_data.py
```

Local CSV command:

```bash
python scripts/prepare_hcahps_data.py --input-mode local
```

Current script behavior:

- API mode pages through CMS dataset `dgck-syfz` with `limit` and `offset`.
- The Florida state filter is applied in pandas after source rows are loaded.
- Local CSV mode reads the first CSV in `data/raw/`.
- The processed output is written to `data/processed/hcahps_patient_experience_fl_clean.csv`.
