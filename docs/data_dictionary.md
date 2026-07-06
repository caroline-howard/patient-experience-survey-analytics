# Data Dictionary

## Cleaned CMS HCAHPS Output

Output file:

```text
data/processed/hcahps_patient_experience_clean.csv
```

| Field name | Source | Description | Dashboard use |
| --- | --- | --- | --- |
| `provider_id` | CMS HCAHPS raw CSV | Hospital or provider identifier, standardized from available CMS identifier fields | Hospital-level filtering and joins |
| `hospital_name` | CMS HCAHPS raw CSV | Hospital or facility name | Dashboard labels and hospital lookup |
| `state` | CMS HCAHPS raw CSV | Hospital state | State filter and geographic grouping |
| `measure_id` | CMS HCAHPS raw CSV | HCAHPS measure identifier when available | Measure tracking and validation |
| `measure_name` | CMS HCAHPS raw CSV | Patient experience measure label or question text | Measure labels in tables and visuals |
| `source_measure_text` | Script-derived from CMS fields | Combined measure ID, question, and answer text used for category assignment | Audit trail for measure grouping |
| `dashboard_category` | Script-derived | Portfolio dashboard category assigned from relevant HCAHPS measure text | Primary grouping for dashboard sections |
| `is_dashboard_measure` | Script-derived | Boolean flag identifying rows selected for the dashboard workflow | Filtering dashboard-ready records |
| `patient_survey_star_rating` | CMS HCAHPS raw CSV, if available | Patient survey star rating field from CMS | Rating comparison field |
| `score` | CMS HCAHPS raw CSV, if available | Reported score field from CMS | Measure comparison field |
| `linear_mean` | CMS HCAHPS raw CSV, if available | Linear mean value field from CMS | Supporting score field |
| `top_box_percent` | CMS HCAHPS raw CSV, if available | Top-box percentage field from CMS | Percentage-based dashboard measure |
| `bottom_box_percent` | CMS HCAHPS raw CSV, if available | Bottom-box percentage field from CMS | Supporting percentage field |
| `survey_response_rate_percent` | CMS HCAHPS raw CSV, if available | Survey response rate field from CMS | Context for survey coverage |
| `footnote` | CMS HCAHPS raw CSV, if available | CMS footnote or data quality note | Interpretation and data limitation notes |

Score and footnote column names depend on the CMS source file. The preparation script keeps available rating, score, percentage, rate, and footnote fields after standardizing column names.

## Dashboard Categories

| Category | Measure focus |
| --- | --- |
| `Discharge & Care Transition` | Discharge information and care transition measures |
| `Communication` | Communication with nurses, doctors, and about medicines |
| `Responsiveness` | Responsiveness of hospital staff |
| `Overall Experience` | Overall hospital rating |
| `Recommendation` | Willingness to recommend the hospital |

## Qualtrics Survey Fields

| Field | Description | Notes |
| --- | --- | --- |
| `respondent_id` | Unique survey respondent identifier | Embedded data |
| `hospital_id` | Hospital or facility context | Embedded data |
| `discharge_date` | Patient discharge date context | Embedded data |
| `service_line` | Care area or department | Embedded data |
| `discharge_understanding_score` | Likert-scale discharge understanding item | Survey response |
| `follow_up_support_score` | Likert-scale follow-up support item | Survey response |
| `open_text_feedback` | Free-text patient feedback | Open-text response |
