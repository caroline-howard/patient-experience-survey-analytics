# Data Dictionary

## CMS HCAHPS Data Fields

| Field | Description | Notes |
| --- | --- | --- |
| `provider_id` | Hospital or provider identifier | Source field name may vary by CMS file |
| `hospital_name` | Hospital name | Standardized during preparation |
| `state` | Hospital state | Used for filtering and grouping |
| `measure_id` | HCAHPS measure identifier | Used to filter relevant patient experience measures |
| `measure_name` | HCAHPS measure label | Human-readable measure name |
| `score` | Reported measure value | Numeric conversion handled during preparation |
| `reporting_period` | Reporting period label or date | Standardized when source data is added |

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
