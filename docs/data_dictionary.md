# Data Dictionary

## Cleaned CMS HCAHPS Output

Output files:

```text
data/processed/hcahps_patient_experience_clean.csv
data/processed/hcahps_patient_experience_fl_clean.csv
```

| Field name | Source | Description | Dashboard use |
| --- | --- | --- | --- |
| `facility_id` | CMS API or local CMS extract | Hospital facility identifier stored as text | Hospital-level filtering and joins |
| `facility_name` | CMS API or local CMS extract | Hospital facility name | Dashboard labels and hospital lookup |
| `state` | CMS API or local CMS extract | Two-letter hospital state | State filter and geographic grouping |
| `hcahps_measure_id` | CMS API or local CMS extract | HCAHPS measure identifier | Measure tracking and category assignment |
| `hcahps_question` | CMS API or local CMS extract | HCAHPS question text | Measure labels and dashboard context |
| `hcahps_answer_description` | CMS API or local CMS extract | HCAHPS answer option or score description | Detail labels in pivot tables and visuals |
| `patient_survey_star_rating` | CMS API or local CMS extract | CMS star rating value as published text | Original rating display and audit trail |
| `patient_survey_star_rating_numeric` | Script-derived | Numeric version of star rating when available | Rating calculations and chart values |
| `patient_survey_star_rating_footnote` | CMS API or local CMS extract | Footnote for star rating suppression or interpretation | Data quality notes |
| `hcahps_answer_percent` | CMS API or local CMS extract | CMS answer percentage as published text | Original percentage display and audit trail |
| `hcahps_answer_percent_numeric` | Script-derived | Numeric answer percentage when available | Percentage-based dashboard metrics |
| `hcahps_answer_percent_footnote` | CMS API or local CMS extract | Footnote for answer percentage suppression or interpretation | Data quality notes |
| `hcahps_linear_mean_value` | CMS API or local CMS extract | CMS linear mean value as published text | Original linear mean display and audit trail |
| `hcahps_linear_mean_value_numeric` | Script-derived | Numeric linear mean value when available | Supporting score metric |
| `number_of_completed_surveys` | CMS API or local CMS extract | Completed survey count as published text | Survey volume context |
| `number_of_completed_surveys_numeric` | Script-derived | Numeric completed survey count when available | Pivot summaries and coverage context |
| `number_of_completed_surveys_footnote` | CMS API or local CMS extract | Footnote for completed survey count | Data quality notes |
| `survey_response_rate_percent` | CMS API or local CMS extract | Survey response rate as published text | Survey response context |
| `survey_response_rate_percent_numeric` | Script-derived | Numeric response rate when available | Dashboard context metric |
| `survey_response_rate_percent_footnote` | CMS API or local CMS extract | Footnote for response rate | Data quality notes |
| `start_date` | CMS API or local CMS extract | Reporting period start date | Reporting period label |
| `end_date` | CMS API or local CMS extract | Reporting period end date | Reporting period label |
| `dashboard_category` | Script-derived | Dashboard grouping assigned from HCAHPS measure text | Primary section grouping |
| `is_project_measure` | Script-derived | Boolean flag for measures directly aligned with the portfolio project focus | Filter for core dashboard views |
| `has_numeric_dashboard_value` | Script-derived | Boolean flag indicating whether at least one dashboard numeric field is available | Metric availability checks |

Original CMS text fields are retained so suppressed or not-applicable values remain visible for review. Numeric companion fields are used for dashboard calculations where conversion is valid.

## Dashboard Categories

| Category | Measure focus |
| --- | --- |
| `Discharge Information` | Discharge information measures |
| `Communication` | Communication with nurses, doctors, and about medicines |
| `Overall Experience` | Overall hospital rating |
| `Recommendation` | Willingness to recommend the hospital |
| `Summary Rating` | Summary star rating rows |
| `Other` | HCAHPS rows kept for context but outside the core dashboard focus |

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
