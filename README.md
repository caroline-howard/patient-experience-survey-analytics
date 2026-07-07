# Patient Discharge Experience & Follow-Up Support Survey Insights Dashboard

## Overview

This project uses public CMS HCAHPS patient experience data and a Qualtrics follow-up survey design to demonstrate a survey-to-insights workflow focused on discharge experience and follow-up support needs.

The workflow combines public benchmark data, survey instrument design, Python data preparation, and Excel reporting. The repository includes documentation for the data source, survey logic, data dictionary, dashboard layout, and insights brief format.

## Purpose

This repository presents a clean portfolio foundation for evaluating patient discharge experience using structured survey data and practical reporting artifacts. It emphasizes the connection between respondent experience, survey design, and stakeholder-ready reporting.

## Current Data and Deliverables

| Item | Current project value |
| --- | --- |
| Dataset | CMS HCAHPS Hospital patient survey data |
| Source | CMS Provider Data Catalog dataset `dgck-syfz` |
| Scope | Florida hospitals |
| Reporting period | 07/01/2024-06/30/2025 |
| Processed data | `data/processed/hcahps_patient_experience_fl_clean.csv` |
| Dashboard | `excel_dashboard/patient_discharge_experience_dashboard.xlsx` |
| Qualtrics role | Follow-up survey design only; not the source of HCAHPS data |

## Data Source and Processing

The reporting workflow uses public CMS HCAHPS hospital-level patient experience data as the primary source for benchmark measures. The preparation script at `scripts/prepare_hcahps_data.py` can page through the CMS Provider Data Catalog API or read a manually downloaded CMS CSV from `data/raw/`.

The default project scope is Florida. The current workflow applies the Florida state filter in pandas after loading source rows; it does not currently request a Florida-only filtered API response.

The cleaned output keeps original CMS text values and footnotes for auditability, then adds numeric companion fields and favorable-response fields used by the dashboard.

## Dashboard Metric Logic

The Excel dashboard uses favorable-response metrics for stakeholder-facing scores. It does not average all HCAHPS response buckets together.

Favorable response rules:

| Category | Favorable response rows |
| --- | --- |
| Discharge Information | `Yes` |
| Nurse Communication | `Always` |
| Doctor Communication | `Always` |
| Medicine Communication | `Always` |
| Overall Rating | `9` or `10` |
| Recommendation | `Definitely yes` |

Main dashboard KPIs use survey-volume-weighted favorable-response percentages where numeric answer percentages and completed survey counts are available. Original source rows remain available in the workbook on `Clean_Data`.

## Qualtrics Follow-Up Survey Design

The Qualtrics follow-up survey design demonstrates survey logic for collecting additional discharge and post-discharge support information. It includes embedded respondent context fields, Likert-scale measures, branching and display logic, and open-text feedback prompts.

No actual Qualtrics response export is included in this repository. The Qualtrics component is a follow-up survey design informed by CMS HCAHPS findings, especially medication clarity and discharge support needs.

## Excel Reporting Workflow

The Excel reporting workbook organizes cleaned CMS HCAHPS data into an auditable source table, a pivot-ready table, a dashboard, and an insights brief. The dashboard highlights favorable-response performance by category and submeasure, including survey-weighted statewide metrics and facility comparison views.

## Repository Structure

```text
data/
  raw/                Source CMS HCAHPS files
  processed/          Cleaned analysis-ready files
docs/                 Project documentation and templates
scripts/              Python data preparation scripts
notebooks/            Exploratory analysis notebooks
excel_dashboard/      Excel workbook assets and dashboard files
reports/              Briefs and reporting outputs
assets/               Supporting images and portfolio assets
```

## Tools

- Python
- pandas
- Excel
- Qualtrics
- CMS HCAHPS

## Portfolio/Resume Framing

This project highlights applied survey analytics skills across public data use, survey instrument design, data preparation, dashboard structuring, and insights communication. It is framed for patient experience analytics, healthcare quality reporting, and survey-to-insights portfolio presentation.
