# Project Status and API/Data Inventory

Inspected and updated on: July 7, 2026  
Repository root: `/Users/carolinehoward/Documents/Qualtrics`

## Executive Status

The Patient Experience Survey Analytics project is now in a corrected first-build portfolio state. The repository contains a reproducible HCAHPS data preparation script, a cleaned Florida dashboard-ready CSV, documentation files, and an Excel dashboard workbook using favorable-response metric logic.

Important handoff note: the full raw CMS CSV exists in the local working copy at `data/raw/HCAHPS-Hospital.csv`, but it is ignored by Git and is not tracked. The committed data artifact is the processed Florida CSV at `data/processed/hcahps_patient_experience_fl_clean.csv`.

## Repository and Git Status

| Item | Current status |
| --- | --- |
| Active branch before PR work | `main` |
| Tracking branch | `origin/main` |
| Remote | `https://github.com/caroline-howard/patient-experience-survey-analytics.git` |
| Latest pre-change commit | `d2b60db` - `Add patient discharge experience Excel dashboard` |
| Ignored local files present | `.venv/`, `data/raw/HCAHPS-Hospital.csv`, `scripts/__pycache__/` |

Recent commits before this change set:

| Commit | Date | Message |
| --- | --- | --- |
| `d2b60db` | 2026-07-06 | Add patient discharge experience Excel dashboard |
| `3e1a2c2` | 2026-07-06 | Merge pull request #4 from `hcahps-data-workflow` |
| `6347fa7` | 2026-07-06 | Add HCAHPS data preparation workflow |
| `393c956` | 2026-07-06 | Use CMS API for HCAHPS data workflow |
| `6b8276f` | 2026-07-06 | Prepare CMS HCAHPS data workflow |

## Current Deliverables

| Path | Purpose |
| --- | --- |
| `README.md` | Project overview, data scope, dashboard logic, and portfolio framing |
| `scripts/prepare_hcahps_data.py` | CMS HCAHPS API/local CSV preparation workflow |
| `data/processed/hcahps_patient_experience_fl_clean.csv` | Tracked cleaned Florida dashboard-ready data |
| `excel_dashboard/patient_discharge_experience_dashboard.xlsx` | Tracked Excel reporting workbook |
| `docs/data_dictionary.md` | Current processed field dictionary |
| `docs/data_source_notes.md` | Current data source and API/local workflow notes |
| `docs/excel_dashboard_structure.md` | Current workbook and dashboard structure |
| `docs/project_overview.md` | Project summary and scope |
| `docs/survey_instrument.md` | Qualtrics follow-up survey design notes |
| `docs/survey_logic_map.md` | Qualtrics display/branching logic map |
| `docs/insights_brief_template.md` | Template for a written brief; still a separate Markdown template |
| `docs/project_status_and_api_inventory.md` | This handoff/status report |

## API / Source Data Inventory

### Source and Endpoint

| Item | Value |
| --- | --- |
| Data source | CMS Provider Data Catalog |
| Dataset | Patient survey (HCAHPS) - Hospital |
| Dataset ID | `dgck-syfz` |
| CMS landing page | `https://data.cms.gov/provider-data/dataset/dgck-syfz` |
| API endpoint in script | `https://data.cms.gov/provider-data/api/1/datastore/query/dgck-syfz/0` |
| API URL parameters currently used | `limit` and `offset` |
| Default API page size | `500` |
| Default state filter | `FL`, applied in pandas after source rows are loaded |

The current script does **not** request a Florida-only API response. It pages through source rows and applies the Florida filter locally in pandas. Local CSV mode reads the first CSV in `data/raw/`.

### Local Raw Source File

| Item | Value |
| --- | --- |
| Path | `data/raw/HCAHPS-Hospital.csv` |
| Git status | Ignored, not tracked |
| Rows | 325,856 data rows |
| Columns | 22 |
| Geographic scope | National CMS hospital data plus territories/state-like values; 56 distinct `State` values |
| Florida raw rows | 12,988 rows |
| Florida facilities | 191 unique `Facility ID` values |
| Reporting period | `Start Date` = `07/01/2024`; `End Date` = `06/30/2025` |
| Raw measure IDs | 68 unique `HCAHPS Measure ID` values |

Raw fields include facility identifiers and contact details, HCAHPS measure IDs, question text, answer descriptions, star ratings, answer percentages, linear mean values, survey counts, response rates, footnotes, and reporting dates.

### Processed Dashboard-Ready File

| Item | Value |
| --- | --- |
| Path | `data/processed/hcahps_patient_experience_fl_clean.csv` |
| Git status | Tracked |
| Rows | 11,460 data rows |
| Columns | 33 |
| Geographic scope | Florida only (`state = FL`) |
| Facilities represented | 191 unique `facility_id` values |
| Reporting period | `start_date = 07/01/2024`; `end_date = 06/30/2025` |

Processed category counts:

| Dashboard category | Rows |
| --- | ---: |
| Doctor Communication | 2,674 |
| Nurse Communication | 2,674 |
| Medicine Communication | 2,101 |
| Discharge Information | 1,528 |
| Overall Rating | 955 |
| Recommendation | 955 |
| Summary Rating | 573 |

## Data Transformation Summary

The workflow is implemented in `scripts/prepare_hcahps_data.py`.

| Step | Behavior |
| --- | --- |
| Parse options | Accepts `--input-mode api/local`, `--state`, and `--limit` |
| Load source | API mode pages through CMS; local mode reads first CSV in `data/raw/` |
| Standardize names | Converts source columns to lowercase snake case |
| Normalize local CSV names | Maps `city_town` to `citytown` and `county_parish` to `countyparish` |
| Validate fields | Requires facility, state, measure ID, question, and answer-description fields |
| Filter geography | Filters rows where `state == FL` by default |
| Categorize measures | Adds `dashboard_category` using keyword rules |
| Filter relevant measures | Keeps rows where `dashboard_category != "Other"` |
| Numeric conversion | Adds numeric companion fields with `pd.to_numeric(..., errors="coerce")` |
| Favorable response logic | Adds `favorable_response_type`, `is_favorable_response`, `favorable_response_percent_numeric`, and `favorable_response_weighted_numerator` |
| Export | Writes `data/processed/hcahps_patient_experience_fl_clean.csv` |

## Favorable-Response Rules

| Dashboard category | Favorable response rule |
| --- | --- |
| Discharge Information | Answer description starts with `Yes` |
| Nurse Communication | Answer description contains `Always` |
| Doctor Communication | Answer description contains `Always` |
| Medicine Communication | Answer description contains `Always` |
| Overall Rating | Measure ID is `H_HSP_RATING_9_10` |
| Recommendation | Measure ID is `H_RECMND_DY` |

Rows that do not meet these rules remain in `Clean_Data` and the processed CSV for auditability, but they are not used in the main stakeholder-facing favorable-response KPIs.

## Measure Filtering

The Florida raw subset contains 12,988 rows. The processed dataset contains 11,460 rows, meaning 1,528 Florida rows are excluded from the current dashboard scope as `Other`.

Dropped non-core measure groups:

| Dropped measure ID | Measure area |
| --- | --- |
| `H_CLEAN_HSP_A_P` | Cleanliness |
| `H_CLEAN_HSP_SN_P` | Cleanliness |
| `H_CLEAN_HSP_U_P` | Cleanliness |
| `H_CLEAN_LINEAR_SCORE` | Cleanliness |
| `H_QUIET_HSP_A_P` | Quietness |
| `H_QUIET_HSP_SN_P` | Quietness |
| `H_QUIET_HSP_U_P` | Quietness |
| `H_QUIET_LINEAR_SCORE` | Quietness |

Cleanliness and quietness star-rating rows are retained where they appear as summary star-rating rows. Expanding the dashboard to full HCAHPS environmental experience would be a future scope decision.

## Dashboard Summary

Workbook:

```text
excel_dashboard/patient_discharge_experience_dashboard.xlsx
```

Input data:

```text
data/processed/hcahps_patient_experience_fl_clean.csv
```

### Workbook Sheets

| Sheet | Contents |
| --- | --- |
| `README` | Workbook purpose, source, scope, metric logic, and caveats |
| `Clean_Data` | Full cleaned CSV, 11,460 data rows plus header, in `CleanDataTable` |
| `Data_Dictionary` | Field-purpose dictionary |
| `Pivot_Source` | Slimmed reporting source table with favorable-response fields, in `PivotSourceTable` |
| `Dashboard` | KPI summary, category favorable-response summary, submeasure breakdown, facility comparison, and charts |
| `Insights_Brief` | Short narrative findings and Qualtrics follow-up focus |

### Dashboard Objects

| Object type | Status |
| --- | --- |
| Excel tables | `CleanDataTable`, `PivotSourceTable` |
| Category summary | Present |
| Submeasure breakdown | Present |
| Facility comparison | Present |
| Charts | Category favorable-response chart and lowest-submeasure chart |
| Slicers | Not included |
| Excel pivot tables | Not included |

### Corrected Dashboard Metrics

The dashboard now uses survey-volume-weighted favorable-response metrics.

| Category | Favorable rows used | Scored rows | Survey-weighted favorable % | Simple favorable % |
| --- | --- | ---: | ---: | ---: |
| Discharge Information | `Yes` rows | 521 | 84.27 | 83.19 |
| Nurse Communication | `Always` rows | 694 | 76.39 | 75.90 |
| Doctor Communication | `Always` rows | 694 | 74.82 | 74.97 |
| Medicine Communication | `Always` rows | 521 | 58.01 | 57.78 |
| Overall Rating | `9 or 10` rows | 175 | 69.07 | 67.61 |
| Recommendation | `Definitely yes` rows | 175 | 70.01 | 68.21 |

### Main Finding

Florida hospitals perform relatively well on discharge information and general nurse/doctor communication. The clearest improvement area is medicine communication, especially explaining possible side effects.

## Qualtrics Role

The Qualtrics component is a follow-up survey design, not a source of analyzed response data. No actual Qualtrics response export is present in the repository.

The CMS HCAHPS findings should inform Qualtrics follow-up questions about:

- Whether patients understood what new medications were for.
- Whether patients understood possible side effects.
- Whether patients knew who to contact after discharge with medication or recovery questions.
- What would have made discharge instructions clearer.

## Remaining Work

| Area | Recommended next step |
| --- | --- |
| Raw data provenance | Document whether `data/raw/HCAHPS-Hospital.csv` was manually downloaded or produced outside the script |
| Final portfolio packaging | Add screenshots or a final PDF under `reports/` or `assets/` |
| Optional scope expansion | Decide later whether to include full cleanliness and quietness HCAHPS measures |
| Qualtrics build | Build/export the actual Qualtrics survey if this project will include a live survey artifact |

## Bottom Line

The project now has a defensible data workflow and dashboard metric logic. The dashboard no longer presents misleading averages across all response buckets; it uses favorable-response rules and survey-volume weighting while preserving the original CMS rows for auditability.
