# Data Source Notes

## Primary Source

CMS HCAHPS patient experience data serves as the public data source for the reporting workflow. The project uses CMS hospital-level HCAHPS data and filters it to Florida for the current portfolio dashboard.

## Dataset Details

| Item | Value |
| --- | --- |
| Dataset | Patient survey (HCAHPS) - Hospital |
| Dataset ID | `dgck-syfz` |
| Source | CMS Provider Data Catalog |
| CMS landing page | `https://data.cms.gov/provider-data/dataset/dgck-syfz` |
| Current project scope | Florida hospitals |
| Current reporting period | 07/01/2024-06/30/2025 |
| Processed output | `data/processed/hcahps_patient_experience_fl_clean.csv` |
| Dashboard workbook | `excel_dashboard/patient_discharge_experience_dashboard.xlsx` |

## API and Local CSV Workflow

The preparation script is `scripts/prepare_hcahps_data.py`.

The default API workflow pages through the CMS Provider Data Catalog endpoint using `limit` and `offset`:

```bash
python scripts/prepare_hcahps_data.py
```

The script endpoint is:

```text
https://data.cms.gov/provider-data/api/1/datastore/query/dgck-syfz/0
```

Current API URL parameters used by the script:

| Parameter | Purpose |
| --- | --- |
| `limit` | API page size; default is `500` |
| `offset` | Pagination offset |

Important: the current script does **not** request a Florida-only API response. It loads source rows through API pagination, standardizes them in pandas, and then applies the state filter locally.

The local CSV workflow reads the first CSV found in `data/raw/`:

```bash
python scripts/prepare_hcahps_data.py --input-mode local
```

The current local raw file available in this working copy is:

```text
data/raw/HCAHPS-Hospital.csv
```

That raw CSV is intentionally ignored by Git because it is large. The tracked data artifact is the processed Florida extract:

```text
data/processed/hcahps_patient_experience_fl_clean.csv
```

## Configurable State Filter

The script supports a state filter:

```bash
python scripts/prepare_hcahps_data.py --state FL
```

To process another state, replace `FL` with another two-letter state code:

```bash
python scripts/prepare_hcahps_data.py --state GA
```

There is no `--all-states` argument in the current script.

## Data Handling Notes

- API extracts and local CSV inputs are processed through the same cleaning workflow.
- No synthetic records or placeholder results are included.
- The workflow does not invent findings or fill missing CMS values with artificial results.
- Facility IDs are preserved as text so leading zeroes are not lost.
- Numeric fields are converted where possible while original CMS text values are retained.
- CMS footnote fields are kept when available.
- Local CSV fields such as `City/Town` and `County/Parish` are normalized to `citytown` and `countyparish` so they align with API-style field names.
- Favorable-response fields are derived for dashboard scoring, while non-favorable response rows remain available for auditability.

## Favorable-Response Scoring Rules

The dashboard does not average all HCAHPS response buckets together. It uses top-box/favorable-response rows.

| Dashboard category | Favorable response rule |
| --- | --- |
| Discharge Information | Answer description starts with `Yes` |
| Nurse Communication | Answer description contains `Always` |
| Doctor Communication | Answer description contains `Always` |
| Medicine Communication | Answer description contains `Always` |
| Overall Rating | Measure ID is `H_HSP_RATING_9_10` |
| Recommendation | Measure ID is `H_RECMND_DY` |

The main dashboard metric is a survey-volume-weighted favorable-response percentage:

```text
sum(favorable_response_percent_numeric * number_of_completed_surveys_numeric)
/ sum(number_of_completed_surveys_numeric)
```

## Relevant Measure Areas

The current dashboard scope includes:

- Discharge information
- Communication with nurses
- Communication with doctors
- Communication about medicines
- Overall hospital rating
- Willingness to recommend
- Summary star rating context

Cleanliness and quietness non-star rows are not part of the current dashboard focus. Cleanliness and quietness star-rating rows are retained only where they appear as summary star-rating rows.
