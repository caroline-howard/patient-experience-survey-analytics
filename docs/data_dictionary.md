# Data Dictionary

## Cleaned CMS HCAHPS Output

Current processed output:

```text
data/processed/hcahps_patient_experience_fl_clean.csv
```

The processed file keeps original CMS text values for auditability and adds numeric companion fields for dashboard calculations. It also adds favorable-response fields used by the Excel dashboard.

## Processed Fields

| Field name | Source | Description | Dashboard use |
| --- | --- | --- | --- |
| `facility_id` | CMS API or local CMS extract | Hospital facility identifier stored as text | Hospital-level filtering and joins |
| `facility_name` | CMS API or local CMS extract | Hospital facility name | Dashboard labels and facility comparison |
| `address` | CMS API or local CMS extract | Hospital street address | Facility context |
| `citytown` | CMS API or normalized local CMS extract | Hospital city/town | Facility context and possible geography filters |
| `state` | CMS API or local CMS extract | Two-letter hospital state | State filter; current file is Florida |
| `zip_code` | CMS API or local CMS extract | Hospital ZIP code | Facility context |
| `countyparish` | CMS API or normalized local CMS extract | Hospital county/parish | Facility context and possible county grouping |
| `telephone_number` | CMS API or local CMS extract | Hospital telephone number | Facility context |
| `hcahps_measure_id` | CMS API or local CMS extract | HCAHPS measure identifier | Measure tracking and category assignment |
| `hcahps_question` | CMS API or local CMS extract | HCAHPS question text | Measure labels and dashboard context |
| `hcahps_answer_description` | CMS API or local CMS extract | HCAHPS answer option or score description | Detail labels in tables and visuals |
| `patient_survey_star_rating` | CMS API or local CMS extract | CMS star rating value as published text | Original rating display and audit trail |
| `patient_survey_star_rating_footnote` | CMS API or local CMS extract | Footnote for star rating suppression or interpretation | Data quality notes |
| `hcahps_answer_percent` | CMS API or local CMS extract | CMS answer percentage as published text | Original percentage display and audit trail |
| `hcahps_answer_percent_footnote` | CMS API or local CMS extract | Footnote for answer percentage suppression or interpretation | Data quality notes |
| `hcahps_linear_mean_value` | CMS API or local CMS extract | CMS linear mean value as published text | Original linear mean display and audit trail |
| `number_of_completed_surveys` | CMS API or local CMS extract | Completed survey count as published text | Survey volume context |
| `number_of_completed_surveys_footnote` | CMS API or local CMS extract | Footnote for completed survey count | Data quality notes |
| `survey_response_rate_percent` | CMS API or local CMS extract | Survey response rate as published text | Survey response context |
| `survey_response_rate_percent_footnote` | CMS API or local CMS extract | Footnote for response rate | Data quality notes |
| `start_date` | CMS API or local CMS extract | Reporting period start date | Reporting period label |
| `end_date` | CMS API or local CMS extract | Reporting period end date | Reporting period label |
| `dashboard_category` | Script-derived | Dashboard grouping assigned from HCAHPS measure text | Primary reporting section |
| `is_relevant_measure` | Script-derived | Boolean flag for rows retained in the current dashboard scope | Audit and filtering |
| `patient_survey_star_rating_numeric` | Script-derived | Numeric version of star rating when available | Rating calculations and chart values |
| `hcahps_answer_percent_numeric` | Script-derived | Numeric answer percentage when available | Answer-percentage audit and calculations |
| `hcahps_linear_mean_value_numeric` | Script-derived | Numeric linear mean value when available | Supporting score metric |
| `number_of_completed_surveys_numeric` | Script-derived | Numeric completed survey count when available | Weight for survey-weighted dashboard metrics |
| `survey_response_rate_percent_numeric` | Script-derived | Numeric response rate when available | Dashboard context metric |
| `favorable_response_type` | Script-derived | Favorable-response label: `Always`, `Yes`, `9 or 10`, or `Definitely yes` | Dashboard favorable-response filtering |
| `is_favorable_response` | Script-derived | Boolean flag identifying rows used in stakeholder-facing favorable-response metrics | Dashboard KPI filtering |
| `favorable_response_percent_numeric` | Script-derived | Numeric answer percent retained only for favorable rows | Dashboard numerator input |
| `favorable_response_weighted_numerator` | Script-derived | `favorable_response_percent_numeric * number_of_completed_surveys_numeric` | Survey-weighted KPI numerator |

## Favorable-Response Rules

| Dashboard category | Favorable-response rule |
| --- | --- |
| `Discharge Information` | Answer description starts with `Yes` |
| `Nurse Communication` | Answer description contains `Always` |
| `Doctor Communication` | Answer description contains `Always` |
| `Medicine Communication` | Answer description contains `Always` |
| `Overall Rating` | Measure ID is `H_HSP_RATING_9_10` |
| `Recommendation` | Measure ID is `H_RECMND_DY` |

Rows that do not meet these rules remain in the processed file but are not counted in the main favorable-response KPIs.

## Dashboard Categories

| Category | Measure focus |
| --- | --- |
| `Discharge Information` | Discharge and recovery information measures |
| `Nurse Communication` | Nurse communication, listening, explaining, courtesy, and respect |
| `Doctor Communication` | Doctor communication, listening, explaining, courtesy, and respect |
| `Medicine Communication` | Medicine explanations and side-effect communication |
| `Overall Rating` | High overall hospital rating |
| `Recommendation` | Definite willingness to recommend the hospital |
| `Summary Rating` | Summary star rating context |
| `Other` | HCAHPS rows outside the current dashboard focus |

## Qualtrics Survey Design Fields

These fields are part of the follow-up survey design documentation. No actual Qualtrics response export is currently included in the repository.

| Field | Description | Notes |
| --- | --- | --- |
| `respondent_id` | Unique survey respondent identifier | Embedded data |
| `hospital_id` | Hospital or facility context | Embedded data |
| `discharge_date` | Patient discharge date context | Embedded data |
| `service_line` | Care area or department | Embedded data |
| `language_preference` | Preferred survey language | Embedded data |
| `follow_up_channel` | Outreach channel used for follow-up | Embedded data |
| `discharge_understanding_score` | Likert-scale discharge understanding item | Survey response |
| `follow_up_support_score` | Likert-scale follow-up support item | Survey response |
| `open_text_feedback` | Free-text patient feedback | Open-text response |
